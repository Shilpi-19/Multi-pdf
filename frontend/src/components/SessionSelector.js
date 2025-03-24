// import React from 'react';

// function SessionSelector({ sessions, currentSession, onSelect, onCreate, onDelete }) {
//   return (
//     <div>
//       <select
//         value={currentSession || ''}
//         onChange={(e) => onSelect(e.target.value)}
//         disabled={!sessions.length}
//       >
//         <option value="">Select a session</option>
//         {sessions.map((session) => (
//           <option key={session} value={session}>
//             {session}
//           </option>
//         ))}
//       </select>
//       <button onClick={onCreate}>Create New Session</button>
//       {currentSession && <button onClick={onDelete}>Delete Session</button>}
//     </div>
//   );
// }

// export default SessionSelector;


import React, { useState } from 'react';

function SessionSelector({ sessions, currentSession, onSelect, onCreate, onDelete, onRename }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedName, setEditedName] = useState('');

  const handleRenameClick = () => {
    setEditedName(currentSession);
    setIsEditing(true);
  };

  const handleSaveRename = async () => {
    if (editedName && editedName !== currentSession) {
      await onRename(currentSession, editedName);
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
              <option key={session} value={session}>
                {session}
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
            placeholder="Enter new name"
          />
          <button onClick={handleSaveRename}>Save</button>
          <button onClick={() => setIsEditing(false)}>Cancel</button>
        </div>
      )}
      <button onClick={onCreate}>Create New Session</button>
      {currentSession && <button onClick={onDelete}>Delete Session</button>}
    </div>
  );
}

export default SessionSelector;