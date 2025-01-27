import React from 'react';

function VideoFeed() {
  return (
    <div className="video-feed">
      <h2>Live Feed</h2>
      <img src="http://localhost:5000/api/video_feed" alt="Video Feed" style={{height: '1000px', width: 'auto'}} />
    </div>
  );
}

export default VideoFeed;
