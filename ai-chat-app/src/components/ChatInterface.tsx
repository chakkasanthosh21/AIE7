'use client';

import { useState, useRef } from 'react';

export default function ChatInterface() {
  const [answer, setAnswer] = useState('');
  const [context, setContext] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [domain, setDomain] = useState('General');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAnswer('');
    setContext([]);
    setUploading(true);

    const formData = new FormData();
    const file = fileInputRef.current?.files?.[0];
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const question = (e.target as any).question.value;
    if (!file || !question || !apiKey) {
      setUploading(false);
      return;
    }
    formData.append('pdf', file);
    formData.append('question', question);
    formData.append('apiKey', apiKey);
    formData.append('domain', domain);

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
        <label className="font-semibold text-black">OpenAI API Key
          <input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)} required className="border p-2 rounded w-full mt-1 text-black bg-white" placeholder="sk-..." />
        </label>
        <label className="font-semibold text-black">Domain
          <select value={domain} onChange={e => setDomain(e.target.value)} className="border p-2 rounded w-full mt-1 text-black bg-white font-semibold">
            <option value="General">General</option>
            <option value="Legal">Legal</option>
            <option value="Academic">Academic</option>
            <option value="Healthcare">Healthcare</option>
            <option value="Business">Business</option>
            <option value="Education">Education</option>
            <option value="Finance">Finance</option>
          </select>
        </label>
        <label className="font-semibold text-black">Upload File (PDF or TXT)
          <input type="file" accept=".pdf,.txt" ref={fileInputRef} required className="border p-2 rounded w-full mt-1 text-black bg-white" />
        </label>
        <label className="font-semibold text-black">Question
          <input type="text" name="question" placeholder="Ask a question about the file..." required className="border p-2 rounded w-full mt-1 text-black bg-white" />
        </label>
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