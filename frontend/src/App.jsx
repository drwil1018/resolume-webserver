import { useState, useEffect } from "react";
import DeckSelection from "./DeckSelection";
import Slider from "./Slider";

function App() {
  const [isEditing, setIsEditing] = useState(false);
  const [effect, setEffect] = useState("exposure")
  
  useEffect(() => {
    postEditing();
  }, [isEditing]);

  async function postEditing() {
    const response = await fetch('http://localhost:5000/edit_clip', {
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
      <DeckSelection isEditing={isEditing} setIsEditing={setIsEditing} />
      {isEditing ? <Slider isEditing={isEditing} setIsEditing={setIsEditing} effect={effect} setEffect={setEffect} /> : null}
    </>
  );
}

export default App;
