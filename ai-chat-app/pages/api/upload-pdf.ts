import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import pdfParse from 'pdf-parse';
import { v4 as uuidv4 } from 'uuid';
import OpenAI from 'openai';

export const config = {
  api: {
    bodyParser: false,
  },
};

// In-memory store for demo (doc_id -> { chunks, embeddings })
const pdfStore: Record<string, { chunks: string[]; embeddings: number[][] }> = {};

function isFormidableFile(file: any): file is { filepath: string } {
  return file && typeof file === 'object' && 'filepath' in file;
}

function chunkText(text: string, chunkSize = 1000, chunkOverlap = 200): string[] {
  const chunks: string[] = [];
  for (let i = 0; i < text.length; i += chunkSize - chunkOverlap) {
    chunks.push(text.slice(i, i + chunkSize));
  }
  return chunks;
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
    let pdfFile: any;
    if (Array.isArray(files.pdf)) {
      pdfFile = files.pdf[0];
    } else if (files.pdf && isFormidableFile(files.pdf)) {
      pdfFile = files.pdf;
    }
    if (!pdfFile || !isFormidableFile(pdfFile)) {
      return res.status(400).json({ error: 'No PDF file uploaded.' });
    }
    try {
      const dataBuffer = fs.readFileSync(pdfFile.filepath);
      const pdfData = await pdfParse(dataBuffer);
      const text = pdfData.text;
      fs.unlinkSync(pdfFile.filepath);
      const chunks = chunkText(text);

      // Generate embeddings for each chunk
      const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
      const embeddings: number[][] = [];
      for (const chunk of chunks) {
        const response = await openai.embeddings.create({
          model: 'text-embedding-3-small',
          input: chunk,
        });
        embeddings.push(response.data[0].embedding as number[]);
      }

      // Store in memory with a doc_id
      const doc_id = uuidv4();
      pdfStore[doc_id] = { chunks, embeddings };

      return res.status(200).json({ doc_id, num_chunks: chunks.length });
    } catch (error) {
      return res.status(500).json({ error: 'Failed to process PDF.', details: String(error) });
    }
  });
} 