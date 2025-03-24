import React, { useState } from 'react';

function SessionSelector({ sessions, currentSession, onSelect, onCreate, onDelete, onRename }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedName, setEditedName] = useState('');

  const handleRenameClick = () => {
    const currentSessionData = sessions.find(s => s.id === currentSession);
    setEditedName(currentSessionData ? currentSessionData.name : '');
    setIsEditing(true);
  };

  const handleRenameSubmit = () => {
    if (editedName.trim()) {
      onRename(currentSession, editedName.trim());
      setIsEditing(false);
    }
  };

  return (
    <div className="session-selector">
      {!isEditing ? (
        <div className="session-dropdown-container">
          <select
            value={currentSession || ''}
            onChange={(e) => onSelect(e.target.value)}
            disabled={!sessions.length}
          >
            <option value="">Select a session</option>
            {sessions.map((session) => (
              <option key={session.id} value={session.id}>
                {session.name}
              </option>
            ))}
          </select>
          {currentSession && (
            <button 
              className="edit-button"
              onClick={handleRenameClick}
              title="Rename session"
            >
              ✎
            </button>
          )}
        </div>
      ) : (
        <div className="session-rename-container">
          <input
            type="text"
            value={editedName}
            onChange={(e) => setEditedName(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleRenameSubmit()}
            placeholder="Enter new name"
          />
          <button onClick={handleRenameSubmit}>Save</button>
          <button onClick={() => setIsEditing(false)}>Cancel</button>
        </div>
      )}
      <div className="session-buttons">
        <button onClick={onCreate}>Create New Session</button>
        {currentSession && (
          <button onClick={() => onDelete(currentSession)}>Delete Session</button>
        )}
      </div>
    </div>
  );
}

export default SessionSelector;
