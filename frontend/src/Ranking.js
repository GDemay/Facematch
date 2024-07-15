import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Ranking.css';

const ConfirmDelete = ({ show, onClose, onConfirm }) => {
  if (!show) {
    return null;
  }

  return (
    <div className="confirm-delete">
      <div className="confirm-delete-content">
        <h3>Are you sure you want to delete this image?</h3>
        <button onClick={onConfirm}>Yes</button>
        <button onClick={onClose}>No</button>
      </div>
    </div>
  );
};

function Ranking() {
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    fetchRankings();
  }, []);

  const fetchRankings = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('http://127.0.0.1:8000/images');
      const sortedRankings = response.data.sort((a, b) => b.score - a.score);
      setRankings(sortedRankings);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching rankings:', error);
      setError('Error fetching rankings: ' + (error.response?.data?.detail || error.message));
      setLoading(false);
    }
  };

  const handleImageClick = (image) => {
    setSelectedImage(image);
    setShowConfirm(true);
  };

  const handleClose = () => {
    setShowConfirm(false);
    setSelectedImage(null);
  };

  const handleConfirm = async () => {
    if (selectedImage) {
      try {
        await axios.delete(`http://127.0.0.1:8000/images/${selectedImage.id}`);
        setRankings(rankings.filter(image => image.id !== selectedImage.id));
        setShowConfirm(false);
        setSelectedImage(null);
      } catch (error) {
        console.error('Error deleting image:', error);
        setError('Error deleting image: ' + (error.response?.data?.detail || error.message));
        setShowConfirm(false);
        setSelectedImage(null);
      }
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="Ranking">
      <h2>Image Rankings</h2>
      <div className="ranking-list">
        {rankings.map((image, index) => (
          <div key={image.id} className="ranking-item" onClick={() => handleImageClick(image)}>
            <img src={`http://127.0.0.1:8000${image.path}`} alt={`Image ${index + 1}`} />
            <div className="ranking-info">
              <p>Rank: {index + 1}</p>
              <p>ELO Score: {image.score.toFixed(2)}</p>
            </div>
          </div>
        ))}
      </div>
      <ConfirmDelete show={showConfirm} onClose={handleClose} onConfirm={handleConfirm} />
    </div>
  );
}

export default Ranking;
