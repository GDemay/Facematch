import React from 'react';

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

export default ConfirmDelete;
