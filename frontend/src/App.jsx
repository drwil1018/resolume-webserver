import { useState, useEffect } from "react";
import DeckSelection from "./DeckSelection";
import Slider from "./Slider";
import { API_URL } from "./api";

function App() {
  const [isEditing, setIsEditing] = useState(false);
  const [effect, setEffect] = useState("exposure");
  const [selectedLayer, setSelectedLayer] = useState("1"); // Default to layer 1
  
  useEffect(() => {
    postEditing();
  }, [isEditing]);

  async function postEditing() {
    const response = await fetch(`${API_URL}/edit_clip`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({isEditing: isEditing}),
  })
  }

  return (
    <>
      <h1>Resolume Webserver</h1>
      <DeckSelection 
        isEditing={isEditing} 
        setIsEditing={setIsEditing} 
        selectedLayer={selectedLayer}
        setSelectedLayer={setSelectedLayer} 
      />
      {isEditing ? <Slider isEditing={isEditing} setIsEditing={setIsEditing} effect={effect} setEffect={setEffect} /> : null}
    </>
  );
}

export default App;
