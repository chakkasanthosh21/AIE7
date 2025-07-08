'use client';

import { useState, useRef } from 'react';

export default function ChatInterface() {
  const [answer, setAnswer] = useState('');
  const [context, setContext] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAnswer('');
    setContext([]);
    setUploading(true);

    const formData = new FormData();
    const file = fileInputRef.current?.files?.[0];
    const question = (e.target as any).question.value;
    if (!file || !question) {
      setUploading(false);
      return;
    }
    formData.append('pdf', file);
    formData.append('question', question);

    const res = await fetch('/api/pdf-rag-chat', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    setAnswer(data.answer || 'No answer returned.');
    setContext(data.context || []);
    setUploading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md flex flex-col gap-4 w-full max-w-xl">
        <input type="file" accept="application/pdf" ref={fileInputRef} required className="border p-2 rounded" />
        <input type="text" name="question" placeholder="Ask a question about the PDF..." required className="border p-2 rounded" />
        <button type="submit" disabled={uploading} className="bg-blue-600 text-white px-4 py-2 rounded-lg">
          {uploading ? 'Processing...' : 'Ask'}
        </button>
      </form>
      {answer && (
        <div className="mt-6 bg-white p-4 rounded-lg shadow-md w-full max-w-xl">
          <h3 className="font-semibold mb-2">Answer:</h3>
          <p className="text-black">{answer}</p>
        </div>
      )}
      {context.length > 0 && (
        <div className="mt-4 bg-gray-100 p-4 rounded-lg w-full max-w-xl">
          <h4 className="font-semibold mb-2">Context used:</h4>
          <pre className="text-black" style={{ whiteSpace: 'pre-wrap' }}>{context.join('\n\n')}</pre>
        </div>
      )}
      {answer && context.length === 0 && (
        <div className="mt-4 text-red-600 font-semibold">PDF could not be read or parsed. Please try a different file.</div>
      )}
    </div>
  );
} 