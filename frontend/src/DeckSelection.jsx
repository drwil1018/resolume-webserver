import React, { useState, useEffect } from 'react';
import ThumbnailGrid from './ThumbnailGrid';
import BottomButtons from './BottomButtons';

// Get API URL from environment variables with fallback
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function DeckSelection({ isEditing, setIsEditing, selectedLayer, setSelectedLayer }) {
    const [deck, setDeck] = useState();
    const [loading, setLoading] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);

    useEffect(() => {
        if (deck) {
            postDeck();
        }
    }, [deck]);

    async function postDeck() {
        const response = await fetch(`${API_URL}/deck_selection`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({deck: deck}),
        })
    }

  return (<>
    <div className="button-container">
        <button className="button" onClick={() => setDeck(2)}>Halle</button>
        <button className="button" onClick={() => setDeck(3)}>Deck 2</button>
        <button className="button" onClick={() => setDeck(4)}>Deck 3</button>
    </div>
    {deck && <ThumbnailGrid 
      deck={deck} 
      isEditing={isEditing} 
      loading={loading} 
      setLoading={setLoading}
      selectedLayer={selectedLayer}
      isDeleting={isDeleting}
    />}
    {deck && <BottomButtons 
      isEditing={isEditing} 
      setIsEditing={setIsEditing} 
      selectedLayer={selectedLayer}
      setSelectedLayer={setSelectedLayer}
      setIsDeleting={setIsDeleting}
    />}
  </>
  );
}

export default DeckSelection;