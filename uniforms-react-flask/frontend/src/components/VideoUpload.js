import React, { useState } from 'react';

function VideoUpload() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('video', file);

    try {
      const response = await fetch('http://localhost:5000/api/upload_video', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while uploading the video');
    }
  };

  return (
    <div className="widget">
      <h2>Upload Video</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <input type="file" onChange={handleFileChange} accept="video/*" />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}

export default VideoUpload;
