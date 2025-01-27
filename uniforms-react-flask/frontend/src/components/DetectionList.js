import React, { useState, useEffect } from 'react';

function DetectionList() {
  const [detections, setDetections] = useState([]);

  useEffect(() => {
    const fetchDetections = async () => {
      const response = await fetch('http://localhost:5000/api/get_detections');
      const data = await response.json();
      setDetections(data);
    };

    fetchDetections();
    const interval = setInterval(fetchDetections, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="widget">
      <h2>Detections</h2>
      <ul className="detection-list">
        {detections.map((detection, index) => (
          <li key={index}>
            <span className="detection-label">{detection.label}</span>
            <span className="detection-confidence">{detection.confidence.toFixed(2)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DetectionList;
