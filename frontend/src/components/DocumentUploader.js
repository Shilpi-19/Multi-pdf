import React, { useState } from 'react';
import axios from 'axios';

function DocumentUploader({ sessionId, onUploadSuccess }) {
  const [files, setFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (e) => {
    setFiles(e.target.files);
    setUploadStatus('');
  };

  const handleUpload = async () => {
    setIsUploading(true);
    setUploadStatus('Uploading documents...');
    
    const formData = new FormData();
    for (let file of files) {
      formData.append('pdfs', file);
    }

    try {
      setUploadStatus('Processing documents... This may take a few moments.');
      const response = await axios.post(`/sessions/${sessionId}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      setUploadStatus('Documents processed successfully!');
      setFiles([]);
      onUploadSuccess();

      // Clear success message after 3 seconds
      setTimeout(() => {
        setUploadStatus('');
      }, 3000);
    } catch (error) {
      setUploadStatus(error.response?.data.error || 'Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="document-uploader">
      <h3>Upload Documents</h3>
      <div className="upload-container">
        <input 
          type="file" 
          multiple 
          accept=".pdf" 
          onChange={handleFileChange}
          disabled={isUploading}
          className="file-input"
        />
        <button 
          onClick={handleUpload} 
          disabled={!files.length || isUploading}
          className={`upload-button ${isUploading ? 'uploading' : ''}`}
        >
          {isUploading ? 'Processing...' : 'Process Documents'}
        </button>
      </div>
      
      {files.length > 0 && !isUploading && (
        <div className="selected-files">
          <p>{files.length} file(s) selected</p>
        </div>
      )}
      
      {uploadStatus && (
        <div className={`upload-status ${isUploading ? 'loading' : 'success'}`}>
          {isUploading && <div className="spinner"></div>}
          <p>{uploadStatus}</p>
        </div>
      )}
    </div>
  );
}

export default DocumentUploader;
