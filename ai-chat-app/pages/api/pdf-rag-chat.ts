import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import pdfParse from 'pdf-parse';
import OpenAI from 'openai';

export const config = {
  api: {
    bodyParser: false,
  },
};

function chunkText(text: string, chunkSize = 1000, chunkOverlap = 200): string[] {
  const chunks: string[] = [];
  for (let i = 0; i < text.length; i += chunkSize - chunkOverlap) {
    chunks.push(text.slice(i, i + chunkSize));
  }
  return chunks;
}

function cosineSimilarity(a: number[], b: number[]): number {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const formidable = await import('formidable');
  const form = new formidable.IncomingForm();

  form.parse(req, async (err, fields, files) => {
    if (err) {
      return res.status(500).json({ error: 'Error parsing form data', details: String(err) });
    }
    const question = Array.isArray(fields.question) ? fields.question[0] : fields.question;
    if (!question || typeof question !== 'string') {
      return res.status(400).json({ error: 'No question provided.' });
    }
    let pdfFile: any;
    if (Array.isArray(files.pdf)) {
      pdfFile = files.pdf[0];
    } else if (files.pdf && typeof files.pdf === 'object' && 'filepath' in files.pdf) {
      pdfFile = files.pdf;
    }
    if (!pdfFile || typeof pdfFile !== 'object' || !('filepath' in pdfFile)) {
      return res.status(400).json({ error: 'No PDF file uploaded.' });
    }
    try {
      const dataBuffer = fs.readFileSync(pdfFile.filepath);
      const pdfData = await pdfParse(dataBuffer);
      const text = pdfData.text;
      fs.unlinkSync(pdfFile.filepath);
      if (!text || !text.trim()) {
        return res.status(400).json({ error: 'The PDF could not be read or contains no extractable text.' });
      }
      const chunks = chunkText(text);
      const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
      // Get embeddings for all chunks
      const chunkEmbeddings: number[][] = [];
      for (const chunk of chunks) {
        const response = await openai.embeddings.create({
          model: 'text-embedding-3-small',
          input: chunk,
        });
        chunkEmbeddings.push(response.data[0].embedding as number[]);
      }
      // Get embedding for the question
      const queryEmbeddingResp = await openai.embeddings.create({
        model: 'text-embedding-3-small',
        input: question,
      });
      const queryEmbedding = queryEmbeddingResp.data[0].embedding as number[];
      // Find top-3 most similar chunks
      const similarities = chunkEmbeddings.map((emb, idx) => ({
        idx,
        score: cosineSimilarity(queryEmbedding, emb),
      }));
      similarities.sort((a, b) => b.score - a.score);
      const topChunks = similarities.slice(0, 3).map(({ idx }) => chunks[idx]);
      const context = topChunks.join('\n');
      // Use OpenAI chat API to answer
      const prompt = `You are a helpful assistant. ONLY use the following context to answer the user's question. If the answer is not in the context, say you don't know.\n\nContext:\n${context}\n\nQuestion: ${question}\n\nAnswer:`;
      const chatResponse = await openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages: [
          { role: 'system', content: 'You are a helpful assistant.' },
          { role: 'user', content: prompt },
        ],
        max_tokens: 512,
      });
      const answer = chatResponse.choices[0].message.content;
      return res.status(200).json({ answer, context: topChunks });
    } catch (error) {
      return res.status(500).json({ error: 'Failed to process PDF and answer.', details: String(error) });
    }
  });
} 