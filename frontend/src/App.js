import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import Ranking from './Ranking';
import Upload from './Upload';
import Toast from './Toast';

function Battle() {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toastVisible, setToastVisible] = useState(false);
  const [eloChanges, setEloChanges] = useState({ winner: 0, loser: 0 });

  useEffect(() => {
    fetchImages();
  }, []);

  const fetchImages = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('http://127.0.0.1:8000/images/get_two_images');
      setImages(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching images:', error);
      setError('Error fetching images: ' + (error.response?.data?.detail || error.message));
      setLoading(false);
    }
  };

  const handleBattle = async (winnerId, loserId) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/images/battle/', null, {
        params: { winner_id: winnerId, loser_id: loserId },
      });

      const [winner, loser] = response.data;
      setEloChanges({
        winner: winner.score - images.find(img => img.id === winnerId).score,
        loser: images.find(img => img.id === loserId).score - loser.score,
      });

      setToastVisible(true);
      setTimeout(() => setToastVisible(false), 3000); // Hide toast after 3 seconds
      fetchImages(); // Fetch new images after the battle
    } catch (error) {
      console.error('Error updating battle:', error);
      setError('Error updating battle: ' + (error.response?.data?.detail || error.message));
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (images.length < 2) {
    return <div>Not enough images available for a battle.</div>;
  }

  return (
    <div className="Battle">
      <h1>Image Battle</h1>
      <p>Which one is more attractive?</p>
      <div className="images">
        {images.map((image, index) => (
          <div key={image.id} className="image-container">
            <img src={`http://127.0.0.1:8000${image.path}`} alt={`Image ${index + 1}`} />
            <p>ELO Score: {image.score.toFixed(2)}</p> {/* Display ELO score */}
            <button onClick={() => handleBattle(image.id, images[1 - index].id)}>
              Vote for this image
            </button>
          </div>
        ))}
      </div>
      {toastVisible && (
        <Toast winnerChange={eloChanges.winner} loserChange={eloChanges.loser} />
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li>
              <Link to="/">Battle</Link>
            </li>
            <li>
              <Link to="/ranking">Ranking</Link>
            </li>
            <li>
              <Link to="/upload">Upload</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<Battle />} />
          <Route path="/ranking" element={<Ranking />} />
          <Route path="/upload" element={<Upload />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
