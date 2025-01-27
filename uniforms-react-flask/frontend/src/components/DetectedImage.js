import React, { useState, useEffect } from 'react';

function DetectedImage() {
  const [lastDetectedFrame, setLastDetectedFrame] = useState(null);

  useEffect(() => {
    const fetchLastDetectedFrame = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/get_detection_frames');
        const data = await response.json();
        if (data.frames && data.frames.length > 0) {
          setLastDetectedFrame(data.frames[data.frames.length - 1]);
        }
      } catch (error) {
        console.error('Error fetching last detected frame:', error);
      }
    };

    fetchLastDetectedFrame();
    const interval = setInterval(fetchLastDetectedFrame, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="detected-image">
      <h2>Last Detected Frame</h2>
      {lastDetectedFrame && (
        <img 
          src={`http://localhost:5000/static/detection_frames/${lastDetectedFrame}`} 
          alt="Last Detected Frame" 
          style={{height: '1000px', width: 'auto'}}
        />
      )}
    </div>
  );
}

export default DetectedImage;
