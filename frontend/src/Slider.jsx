import { useState, useEffect } from "react";

function Slider({ isEditing, setIsEditing, effect, setEffect }) {
  const [value, setValue] = useState(0.5);

  // Config for the slider
  const sliderConfig = {
    exposure: {
      min: 0,
      max: 1,
      step: 0.01,
    },
    zoom: {
      min: 0,
      max: 250,
      step: 1,
    },
    shiftX: {
      min: -750,
      max: 750,
      step: 1,
    },
    shiftY: {
      min: -750,
      max: 750,
      step: 1,
    },
    saturation: {
      min: 0,
      max: 1,
      step: 0.01,
    },
    hue: {
      min: 0,
      max: 1,
      step: 0.01,
    },
  };

  const currentConfig = sliderConfig[effect];

  const handleSliderChange = async (e) => {
    const newValue = e.target.value;
    setValue(newValue);

    await fetch(`http://localhost:5000/update_${effect}`, {
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
    await fetch(`http://localhost:5000/reset_effects`, {
      method: "POST",
    });
  };

  const selectEffect = async (e) => {
    const selectedEffect = e.target.value;
    setEffect(selectedEffect);

    const response = await fetch(`http://localhost:5000/get_effects`);

    const data = await response.json();
    const effectValue = data[selectedEffect];

    setValue(effectValue);
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