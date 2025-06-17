import { useState, useEffect } from "react";

// Get API URL from environment variables with fallback
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function Slider({ isEditing, setIsEditing, effect, setEffect }) {
  const [value, setValue] = useState(0.5);
  
  // Fetch effect values when component mounts or effect changes
  useEffect(() => {
    const fetchEffectValues = async () => {
      try {
        const response = await fetch(`${API_URL}/get_effects`);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update the slider with the current value from Resolume
        if (data && data[effect] !== undefined) {
          setValue(data[effect]);
          console.log(`Using ${effect} value from Resolume: ${data[effect]}`);
        } else {
          // Fallback to default if the value isn't found
          const defaultValue = sliderConfig[effect]?.defaultValue || 0.5;
          setValue(defaultValue);
          console.log(`Using default value for ${effect}: ${defaultValue}`);
        }
      } catch (error) {
        console.error('Error fetching effect values:', error);
        // Fallback to default on error
        setValue(0.5);
      }
    };
    
    fetchEffectValues();
  }, [effect]); // Runs on mount and whenever effect changes

  // Config for the slider
  const sliderConfig = {
    exposure: {
      min: 0,
      max: 1,
      step: 0.01,
      defaultValue: 0.5
    },
    zoom: {
      min: 0,
      max: 250,
      step: 1,
      defaultValue: 100
    },
    shiftX: {
      min: -750,
      max: 750,
      step: 1,
      defaultValue: 0
    },
    shiftY: {
      min: -750,
      max: 750,
      step: 1,
      defaultValue: 0
    },
    saturation: {
      min: 0,
      max: 1,
      step: 0.01,
      defaultValue: 1
    },
    hue: {
      min: 0,
      max: 1,
      step: 0.01,
      defaultValue: 0
    },
  };

  const currentConfig = sliderConfig[effect];

  const handleSliderChange = async (e) => {
    const newValue = e.target.value;
    setValue(newValue);

    await fetch(`${API_URL}/update_${effect}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ value: newValue }),
    });
  };

  const handleDone = () => {
    setIsEditing(false);
  };

  const handleCancel = async () => {
    setIsEditing(false);
    await fetch(`${API_URL}/reset_effects`, {
      method: "POST",
    });
  };

  const selectEffect = (e) => {
    const selectedEffect = e.target.value;
    setEffect(selectedEffect);
    // No need to fetch or setValue here - the useEffect will handle it
  };

  return (
    <>
      <select
        id="effectSelect"
        className="effectSelect"
        onChange={selectEffect}
        value={effect}
      >
        <option value="" disabled>
          Select an effect
        </option>
        <option value="exposure">Exposure</option>
        <option value="zoom">Zoom</option>
        <option value="shiftX">Shift X</option>
        <option value="shiftY">Shift Y</option>
        <option value="saturation">Saturation</option>
        <option value="hue">Hue</option>
      </select>

      <div className="slider-container">
        <form id="effectForm">
          <input
            type="range"
            id={effect}
            min={currentConfig.min}
            max={currentConfig.max}
            step={currentConfig.step}
            value={value}
            onChange={handleSliderChange}
          />
          <span id={`${effect}Value`}>
            {effect === "zoom"
              ? `${value}%`
              : effect === "shiftX" || effect === "shiftY"
              ? `${value}px`
              : value}
          </span>
        </form>
      </div>
      <div className="button-container">
        <button className="button" onClick={handleDone}>
          Done
        </button>
        <button className="button" onClick={handleCancel}>
          Default
        </button>
      </div>
    </>
  );
}

export default Slider;