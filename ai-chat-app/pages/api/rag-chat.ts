import type { NextApiRequest, NextApiResponse } from 'next';
import OpenAI from 'openai';

// Import or redefine the in-memory store from upload-pdf.ts
// In a real app, use a shared module or persistent DB
const globalAny: any = global;
if (!globalAny.pdfStore) {
  globalAny.pdfStore = {};
}
const pdfStore: Record<string, { chunks: string[]; embeddings: number[][] }> = globalAny.pdfStore;

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
  const { doc_id, query, k = 3 } = req.body;
  if (!doc_id || !query) {
    return res.status(400).json({ error: 'doc_id and query are required' });
  }
  const doc = pdfStore[doc_id];
  if (!doc) {
    return res.status(404).json({ error: 'Document not found' });
  }
  try {
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    // Embed the query
    const embeddingResponse = await openai.embeddings.create({
      model: 'text-embedding-3-small',
      input: query,
    });
    const queryEmbedding = embeddingResponse.data[0].embedding as number[];
    // Find top-k most similar chunks
    const similarities = doc.embeddings.map((emb, idx) => ({
      idx,
      score: cosineSimilarity(queryEmbedding, emb),
    }));
    similarities.sort((a, b) => b.score - a.score);
    const topChunks = similarities.slice(0, k).map(({ idx }) => doc.chunks[idx]);
    const context = topChunks.join('\n');
    // Use OpenAI chat API to answer
    const prompt = `You are a helpful assistant. Use the following context to answer the user's question.\n\nContext:\n${context}\n\nQuestion: ${query}\n\nAnswer:`;
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
    return res.status(500).json({ error: 'Failed to answer query.', details: String(error) });
  }
} 