// src/App.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [response, setResponse] = useState('');
  const [selectedMessageId, setSelectedMessageId] = useState(null);

  useEffect(() => {
    const fetchMessages = async () => {
      const res = await axios.get('http://localhost:5000/api/messages');
      setMessages(res.data);
    };
    fetchMessages();
  }, []);

  const handleResponse = async () => {
    if (selectedMessageId) {
      await axios.post(`http://localhost:5000/api/messages/${selectedMessageId}/respond`, { response });
      setResponse('');
      setSelectedMessageId(null);
      const res = await axios.get('http://localhost:5000/api/messages');
      setMessages(res.data);
    }
  };

  const importMessages = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    await axios.post('http://localhost:5000/api/import', formData);
    const res = await axios.get('http://localhost:5000/api/messages');
    setMessages(res.data);
  };

  return (
    <div>
      <h1>Customer Messages</h1>
      <input type="file" onChange={importMessages} accept=".csv" />
      {messages.map((msg) => (
        <div key={msg._id}>
          <p><strong>{msg.customerName}</strong>: {msg.message}</p>
          <textarea
            placeholder="Type your response"
            value={selectedMessageId === msg._id ? response : ''}
            onChange={(e) => {
              setResponse(e.target.value);
              setSelectedMessageId(msg._id);
            }}
          />
          <button onClick={handleResponse}>Send Response</button>
          <hr />
        </div>
      ))}
    </div>
  );
};

export default App;
