import React from 'react';
import './Modal.css';

function Modal({ winnerChange, loserChange, onClose }) {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Battle Result</h2>
        <p>Winner gained: {winnerChange.toFixed(2)} ELO points</p>
        <p>Loser lost: {loserChange.toFixed(2)} ELO points</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default Modal;
