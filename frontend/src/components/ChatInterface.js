
import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

function ChatInterface({ sessionId, chatHistory, onNewMessage }) {
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleAsk = async () => {
    if (!question.trim() || isLoading) return;
    
    const userMessage = question;
    setQuestion('');
    
    try {
      // First API call - Save user's message
      await axios.post(`/sessions/${sessionId}/message`, { 
        content: userMessage,
        sender: 'user'
      });
      onNewMessage('user', userMessage);
      
      // Then start loading and get bot's response
      setIsLoading(true);
      const response = await axios.post(`/sessions/${sessionId}/ask`, { 
        question: userMessage 
      });
      
      // Save and display bot's response
      await axios.post(`/sessions/${sessionId}/message`, {
        content: response.data.answer,
        sender: 'assistant'
      });
      onNewMessage('assistant', response.data.answer);
      
    } catch (error) {
      alert(error.response?.data.error || 'Error processing question');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}-message`}>
            <div className="message-header">
              {msg.sender === 'assistant' ? '🤖 AI Assistant' : '👤 You'}
            </div>
            <div className="message-content">
              {msg.sender === 'assistant' ? (
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              ) : (
                msg.content
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant-message loading">
            <div className="message-header">
              🤖 AI Assistant
            </div>
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about your documents... 📚"
          disabled={isLoading}
        />
        <button 
          onClick={handleAsk} 
          disabled={!question.trim() || isLoading}
          className={isLoading ? 'loading' : ''}
        >
          {isLoading ? '🤔' : '✨'} {isLoading ? 'Processing...' : 'Send'}
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;
