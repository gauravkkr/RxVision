import React, { useState } from 'react';
import axios from 'axios';

function ImageUpload() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8080'
      const res = await axios.post(`${API_URL}/api/imageupload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResponse(res.data);
    } catch (error) {
        console.error('Error uploading file:', error);
        setResponse({ error: 'Failed to upload file' });
      }
    };
  
    return (
      <div>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Upload</button>
        </form>
  
        {response && (
          <div>
            {response.error ? (
              <p>{response.error}</p>
            ) : (
              <div>
                <p>{response.message}</p>
                <a href={`${API_URL}/download/${response.hdf5_file}`}>
                  Download HDF5 File
                </a>
              </div>
            )}
          </div>
        )}
      </div>
    );
  }
  
export default ImageUpload;