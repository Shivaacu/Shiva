import React, { useState, useEffect } from 'react';

function DetectionFrames() {
  const [frames, setFrames] = useState([]);

  useEffect(() => {
    const fetchFrames = async () => {
      try {
        const response = await fetch('/api/get_detection_frames');
        const data = await response.json();
        setFrames(data.frames.slice(0, 5)); // Display last 5 frames
      } catch (error) {
        console.error('Error fetching detection frames:', error);
      }
    };

    fetchFrames();
    const interval = setInterval(fetchFrames, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="detection-frames">
      <h2>Recent Detections</h2>
      <div className="frames-container">
        {frames.map((frame, index) => (
          <img key={index} src={`/static/detection_frames/${frame}`} alt={`Detection ${index + 1}`} />
        ))}
      </div>
    </div>
  );
}

export default DetectionFrames;
