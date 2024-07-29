import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [response, setResponse] = useState([]);
  const [showResponse, setShowResponse] = useState(false);
  const [warningMessage, setWarningMessage] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      alert(res.data.message || 'Upload successful');
    } catch (err) {
      console.error(err);
      alert('Error uploading file');
    }
  };

  const handleQuery = async () => {
    if (!jobDescription.trim()) {
      setWarningMessage('Please enter a job description.');
      return;
    }

    setWarningMessage('');

    try {
      const res = await axios.post('http://localhost:5000/query', { query: jobDescription });
      setResponse(res.data);
      setShowResponse(true);
    } catch (err) {
      console.error(err);
      alert('Error querying');
    }
  };

  const handleClear = async () => {
    try {
      await axios.post('http://localhost:5000/clear');
      setResponse([]);
      setShowResponse(false);
      alert('Data cleared successfully');
    } catch (err) {
      console.error(err);
      alert('Error clearing data');
    }
  };

  const closeOverlay = () => {
    setShowResponse(false);
  };

  const renderCandidateInfo = (info) => {
    return info.split(', ').map((detail, index) => (
      <div key={index} style={{ marginBottom: '5px' }}>
        <strong>{detail.split(': ')[0]}:</strong> {detail.split(': ')[1]}
      </div>
    ));
  };

  return (
    <div style={{
      backgroundImage: 'url(bg.jpg)',
      backgroundSize: 'cover',
      width: '100vw',
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      boxSizing: 'border-box'
    }}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '15px',
        boxShadow: 'rgba(0, 0, 0, 0.2) 0px 10px 20px',
        width: '100%',
        maxWidth: '900px',
        padding: '20px',
        boxSizing: 'border-box',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '20px'
      }}>
        <h1 style={{ textDecoration:'underline',textAlign: 'center', color: '#333', margin: '0' }}>Job Matching System</h1>
        
        <div style={{ width: '100%', textAlign: 'center' }}>
          <h2 style={{ fontWeight: 'normal', marginBottom: '10px' }}>Upload Candidates Data</h2>
          <input
            type="file"
            onChange={handleFileChange}
            style={{ marginBottom: '10px' }}
          />
          <button
            onClick={handleUpload}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              border: 'none',
              borderRadius: '5px',
              backgroundColor: '#4CAF50',
              color: 'white',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease',
              marginBottom: '20px'
            }}
            onMouseOver={(e) => e.target.style.backgroundColor = '#45a049'}
            onMouseOut={(e) => e.target.style.backgroundColor = '#4CAF50'}
          >
            Upload
          </button>
        </div>

        <div style={{ width: '100%', textAlign: 'center' ,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center'}}>
          <h2 style={{ fontWeight: 'normal', marginBottom: '10px' }}>Enter Job Description</h2>
          <textarea
            style={{
              width: '100%',
              maxWidth: '600px',
              height: '200px',
              padding: '10px',
              borderRadius: '5px',
              border: '1px solid #ddd',
              boxSizing: 'border-box'
            }}
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          ></textarea>
          <button
            onClick={handleQuery}
            style={{
              marginTop: '20px',
              padding: '10px 20px',
              fontSize: '16px',
              border: 'none',
              borderRadius: '5px',
              backgroundColor: '#008CBA',
              color: 'white',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease',
            }}
            onMouseOver={(e) => e.target.style.backgroundColor = '#007bb5'}
            onMouseOut={(e) => e.target.style.backgroundColor = '#008CBA'}
          >
            Query
          </button>
          {warningMessage && (
            <p style={{ color: 'red', marginTop: '10px' }}>{warningMessage}</p>
          )}
        </div>

        <button
          onClick={handleClear}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            border: 'none',
            borderRadius: '5px',
            backgroundColor: '#f44336',
            color: 'white',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#e53935'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#f44336'}
        >
          Clear Data
        </button>

        {showResponse && (
          <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 9999
          }}>
            <div style={{
              backgroundColor: 'white',
              border: '1px solid #ddd',
              borderRadius: '15px',
              boxShadow: 'rgba(0, 0, 0, 0.2) 0px 10px 20px',
              width: '90vw',
              maxWidth: '800px',
              maxHeight: '80vh',
              overflowY: 'auto',
              padding: '20px',
              position: 'relative',
              textAlign: 'left'
            }}>
              <button
                onClick={closeOverlay}
                style={{
                  position: 'absolute',
                  top: '10px',
                  right: '10px',
                  padding: '10px 20px',
                  fontSize: '16px',
                  border: 'none',
                  borderRadius: '5px',
                  backgroundColor: '#f44336',
                  color: 'white',
                  cursor: 'pointer',
                  transition: 'background-color 0.3s ease'
                }}
                onMouseOver={(e) => e.target.style.backgroundColor = '#e53935'}
                onMouseOut={(e) => e.target.style.backgroundColor = '#f44336'}
              >
                Close
              </button>
              <h2 style={{ marginBottom: '20px' }}>Suitable Candidates</h2>
              {response.length > 0 ? (
                response.map((item, index) => (
                  <div key={index} style={{
                    marginBottom: '20px',
                    border: '1px solid #ddd',
                    borderRadius: '10px',
                    padding: '15px',
                    backgroundColor: '#f9f9f9'
                  }}>
                    <h3 style={{ marginBottom: '10px' }}>Candidate {index + 1}</h3>
                    <div style={{ marginBottom: '15px' }}>
                      <strong>Candidate Info:</strong>
                      <div style={{ marginLeft: '10px' }}>{renderCandidateInfo(item['Candidate Info'])}</div>
                    </div>
                    <p><strong>Similarity Score:</strong> {item['Similarity Score'].toFixed(2)}</p>
                  </div>
                ))
              ) : (
                <p>No results found.</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
