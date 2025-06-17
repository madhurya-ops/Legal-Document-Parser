import React, { useState } from 'react';
import { sendQuery } from './api';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const handleAsk = async () => {
    if (!input.trim()) return;

    const userMessage = { type: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await sendQuery(input);
      const botMessage = { type: 'bot', text: response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMsg = { type: 'bot', text: 'Sorry, something went wrong.' };
      setMessages((prev) => [...prev, errorMsg]);
    }

    setInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleAsk();
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <header className="p-4 bg-white shadow-md">
        <h1 className="text-2xl font-semibold text-center text-blue-600">
          Ask your PDF
        </h1>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-xl px-4 py-2 rounded-lg ${
              msg.type === 'user'
                ? 'ml-auto bg-blue-500 text-white'
                : 'mr-auto bg-white text-gray-800 border'
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="p-4 bg-white border-t">
        <div className="flex items-center gap-2 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            className="flex-1 p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="Type your question and hit Enter..."
          />
          <button
            onClick={handleAsk}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Ask
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;