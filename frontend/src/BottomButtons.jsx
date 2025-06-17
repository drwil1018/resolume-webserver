import { useState, useEffect } from "react";

// Get API URL from environment variables with fallback
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function BottomButtons({ isEditing, setIsEditing, selectedLayer, setSelectedLayer, setIsDeleting}) {
    const [isOutputSelected, setIsOutputSelected] = useState(false);

    function handleEdit() {
        setIsEditing(true);
    }

    function handleLayerToggle() {
        // Toggle between layer 1 and 2
        setSelectedLayer(selectedLayer === "1" ? "8" : "1");
    }

    async function handleDeleteAll() {
        setIsDeleting(true);
        const response = await fetch(`${API_URL}/clear_all`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ selectedLayer: selectedLayer }),
        });

        const data = await response.json();
        console.log('Success:', data);
        if (data.error) {
            console.error('Error:', data.error);
        }
        setIsDeleting(false);
    }

    function handleOutputSelection() {
        if (isOutputSelected) {
            setIsOutputSelected(false);
        }
        else {
            setIsOutputSelected(true);
        }
    }

    async function postOutput() {
    const response = await fetch(`${API_URL}/select_output`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({isOutputSelected: isOutputSelected}),
    })
    }
    useEffect(() => {
        postOutput();
    }, [isOutputSelected]);


    return (
        <div className="button-container">
            <button className="button" onClick={handleEdit}>Edit</button>
            <button className="button" onClick={handleLayerToggle}>{selectedLayer === "8" ? "Center Layer" : "Side Layer"}</button>
            <button className="button" onClick={handleOutputSelection}>{isOutputSelected ? "Center Output" : "Side Output"}</button>
            <button className="button" onClick={handleDeleteAll}>Delete All</button>
        </div>
    );
}

export default BottomButtons;