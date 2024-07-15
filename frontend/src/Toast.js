import React from 'react';
import './Toast.css';

function Toast({ winnerChange, loserChange }) {
  return (
    <div className="toast">
      <p>Winner gained: {winnerChange.toFixed(2)} ELO points</p>
      <p>Loser lost: {loserChange.toFixed(2)} ELO points</p>
    </div>
  );
}

export default Toast;
