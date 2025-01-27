import React from 'react';
import './App.css';
import VideoFeed from './components/VideoFeed';
import DetectionList from './components/DetectionList';
import MissingItems from './components/MissingItems';
import VideoUpload from './components/VideoUpload';
import DetectedImage from './components/DetectedImage';

function App() {
  return (
    <div className="App">
      <header>
        <h1>Video Detection Dashboard</h1>
      </header>
      <div className="dashboard">
        <aside className="sidebar video-sidebar">
          <VideoUpload />
          <MissingItems />
          <DetectionList />
        </aside>
        <main className="main-content">
          <div className="video-container">
            <VideoFeed />
            <DetectedImage />
          </div>
          
        </main>
      </div>
    </div>
  );
}

export default App;
