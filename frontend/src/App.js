import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SessionSelector from './components/SessionSelector';
import DocumentUploader from './components/DocumentUploader';
import ChatInterface from './components/ChatInterface';
import './App.css';

axios.defaults.baseURL = 'http://localhost:5001';

function App() {
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [uploadedPdfs, setUploadedPdfs] = useState([]);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await axios.get('/sessions');
      setSessions(response.data);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const createNewSession = async () => {
    const response = await axios.post('/sessions');
    const newSessionId = response.data.session_id;
    setCurrentSession(newSessionId);
    setSessions([...sessions, newSessionId]);
    setChatHistory([]);
    setUploadedPdfs([]);
  };

  const selectSession = async (sessionId) => {
    setCurrentSession(sessionId);
    const messagesResponse = await axios.get(`/sessions/${sessionId}/messages`);
    setChatHistory(messagesResponse.data);
    const pdfsResponse = await axios.get(`/sessions/${sessionId}/pdfs`);
    setUploadedPdfs(pdfsResponse.data);
  };

  const deleteSession = async () => {
    if (currentSession) {
      await axios.delete(`/sessions/${currentSession}`);
      setCurrentSession(null);
      setChatHistory([]);
      setUploadedPdfs([]);
      fetchSessions();
    }
  };

  const renameSession = async (sessionId, newName) => {
    try {
      await axios.post(`/sessions/${sessionId}/rename`, { new_name: newName });
      // Refresh the sessions list to get the updated names
      fetchSessions();
    } catch (error) {
      console.error('Error renaming session:', error);
      alert('Failed to rename session');
    }
  };

  const fetchChatHistory = async () => {
    if (currentSession) {
      const response = await axios.get(`/sessions/${currentSession}/messages`);
      setChatHistory(response.data);
    }
  };

  const fetchUploadedPdfs = async () => {
    if (currentSession) {
      const response = await axios.get(`/sessions/${currentSession}/pdfs`);
      setUploadedPdfs(response.data);
    }
  };

  return (
    <div className="app">
      <h1>📚 PDF Chat Assistant</h1>
      <div className="container">
        <div className="sidebar">
          <h2>Session Management</h2>
          <SessionSelector
            sessions={sessions}
            currentSession={currentSession}
            onSelect={selectSession}
            onCreate={createNewSession}
            onDelete={deleteSession}
            onRename={renameSession}
          />
          {currentSession && (
            <>
              <DocumentUploader sessionId={currentSession} onUploadSuccess={fetchUploadedPdfs} />
              <div className="uploaded-docs">
                <h3>Uploaded Documents</h3>
                {uploadedPdfs.length > 0 ? (
                  uploadedPdfs.map((pdf, index) => (
                    <p key={index}>
                      <span>📄</span>
                      <span>{pdf}</span>
                    </p>
                  ))
                ) : (
                  <p>No documents uploaded yet</p>
                )}
              </div>
            </>
          )}
        </div>
        <div className="main">
          <h2>Chat with Your Documents</h2>
          {currentSession ? (
            <ChatInterface 
              sessionId={currentSession} 
              chatHistory={chatHistory} 
              onNewMessage={fetchChatHistory} 
            />
          ) : (
            <div className="empty-state">
              <p>👈 Please select or create a session to start chatting</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
