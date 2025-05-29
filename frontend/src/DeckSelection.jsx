import React, { useState, useEffect } from 'react';
import ThumbnailGrid from './ThumbnailGrid';
import BottomButtons from './BottomButtons';

function DeckSelection({ isEditing, setIsEditing }) {
    const [deck, setDeck] = useState();
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (deck) {
            postDeck();
        }
    }, [deck]);

    async function postDeck() {
        const response = await fetch('http://localhost:5000/deck_selection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({deck: deck}),
        })
    }

  return (<>
    <div className="button-container">
        <button className="button" onClick={() => setDeck(1)}>Deck 1</button>
        <button className="button" onClick={() => setDeck(2)}>Deck 2</button>
        <button className="button" onClick={() => setDeck(3)}>Deck 3</button>
    </div>
    {deck && <ThumbnailGrid deck={deck} isEditing={isEditing} loading={loading} setLoading={setLoading} />}
    {deck && <BottomButtons isEditing={isEditing} setIsEditing={setIsEditing} />}
  </>
  );
}

export default DeckSelection;