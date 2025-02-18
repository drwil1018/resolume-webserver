document.addEventListener('DOMContentLoaded', function() {
    // Message fade out
    const messages = document.querySelectorAll('.message');
    if (messages) {
        messages.forEach(message => {
            setTimeout(() => {
                message.classList.add('fade-out');
                setTimeout(() => {
                    message.remove();
                }, 500);
            }, 3000);
        });
    }

    // Handle initial and click selection
    let selectedThumbnail = null;
    const currentPath = window.location.pathname;
    const storedPath = sessionStorage.getItem('currentPath');
    
    // Clear selection if path changed (switching screens)
    if (storedPath !== currentPath) {
        sessionStorage.removeItem('selectedClipIndex');
        sessionStorage.setItem('currentPath', currentPath);
    } else {
        const storedIndex = sessionStorage.getItem('selectedClipIndex');
        const initialSelection = document.getElementById('selection-index')?.value;
        const selectionIndex = storedIndex || initialSelection;
        
        if (selectionIndex) {
            const imgs = document.querySelectorAll('.thumbnail-grid img');
            if (imgs[selectionIndex - 1]) {
                selectedThumbnail = imgs[selectionIndex - 1];
                selectedThumbnail.classList.add('selected');
            }
        }
    }

    // Update click handling
    document.querySelectorAll('.thumbnail-grid img').forEach((img, index) => {
        img.addEventListener('click', function() {
            if (selectedThumbnail) {
                selectedThumbnail.classList.remove('selected');
            }
            this.classList.add('selected');
            selectedThumbnail = this;
            sessionStorage.setItem('selectedClipIndex', index + 1);
        });
    });

    // Exposure slider
    const exposureslider = document.getElementById('exposure');
    const exposuredisplay = document.getElementById('exposureValue');
    
    if (exposureslider && exposuredisplay) {
        exposureslider.addEventListener('input', async (e) => {
            const value = e.target.value;
            exposuredisplay.textContent = value;

            try {
                const response = await fetch('/update_exposure', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ value: value })
                });

                if (!response.ok) {
                    throw new Error('Failed to set effect');
                }
            } catch (error) {
                console.error('Error', error);
            }
        });
    }

    // Hue slider
    const hueslider = document.getElementById('hue');
    const huedisplay = document.getElementById('hueValue');
    
    if (hueslider && huedisplay) {
        hueslider.addEventListener('input', async (e) => {
            const value = e.target.value;
            huedisplay.textContent = value;

            try {
                const response = await fetch('/update_hue', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ value: value })
                });

                if (!response.ok) {
                    throw new Error('Failed to set effect');
                }
            } catch (error) {
                console.error('Error', error);
            }
        });
    }

    // Saturation slider
    const satslider = document.getElementById('sat');
    const satdisplay = document.getElementById('satValue');
    
    if (satslider && satdisplay) {
        satslider.addEventListener('input', async (e) => {
            const value = e.target.value;
            satdisplay.textContent = value;

            try {
                const response = await fetch('/update_sat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ value: value })
                });

                if (!response.ok) {
                    throw new Error('Failed to set effect');
                }
            } catch (error) {
                console.error('Error', error);
            }
        });
    }

        // Scale slider
        const scaleslider = document.getElementById('scale');
        const scaledisplay = document.getElementById('scaleValue');
        
        if (scaleslider && scaledisplay) {
            scaleslider.addEventListener('input', async (e) => {
                const value = e.target.value;
                scaledisplay.textContent = value;
    
                try {
                    const response = await fetch('/update_scale', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ value: value })
                    });
    
                    if (!response.ok) {
                        throw new Error('Failed to set effect');
                    }
                } catch (error) {
                    console.error('Error', error);
                }
            });
        }

        // Shift X slider
        const shiftxslider = document.getElementById('shiftx');
        const shiftxdisplay = document.getElementById('shiftxValue');
        
        if (shiftxslider && shiftxdisplay) {
            shiftxslider.addEventListener('input', async (e) => {
                const value = e.target.value;
                shiftxdisplay.textContent = value;
    
                try {
                    const response = await fetch('/update_shiftx', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ value: value })
                    });
    
                    if (!response.ok) {
                        throw new Error('Failed to set effect');
                    }
                } catch (error) {
                    console.error('Error', error);
                }
            });
        }

        // Shift Y slider
        const shiftyslider = document.getElementById('shifty');
        const shiftydisplay = document.getElementById('shiftyValue');
        
        if (shiftyslider && shiftydisplay) {
            shiftyslider.addEventListener('input', async (e) => {
                const value = e.target.value;
                shiftydisplay.textContent = value;
    
                try {
                    const response = await fetch('/update_shifty', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ value: value })
                    });
    
                    if (!response.ok) {
                        throw new Error('Failed to set effect');
                    }
                } catch (error) {
                    console.error('Error', error);
                }
            });
        }

// Add right-click handler for sliders
    document.querySelectorAll('input[type="range"]').forEach(slider => {
        slider.addEventListener('contextmenu', async function(e) {
            e.preventDefault();
            const sliderId = this.id;
            const defaultValue = getDefaultValue(sliderId);
            
            try {
                const response = await fetch(`/reset_effect/${sliderId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ value: defaultValue })
                });
                
                if (response.ok) {
                    this.value = defaultValue;
                    document.getElementById(`${sliderId}Value`).textContent = defaultValue;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });

    function getDefaultValue(sliderId) {
        switch(sliderId) {
            case 'exposure':
                return 0.5;
            case 'hue':
                return 0;
            case 'sat':
                return 0.5;
            case 'scale':
                return 100;
            case 'shiftx':
            case 'shifty':
                return 0;
            default:
                return 0;
        }
    }

    // Upload message
    document.getElementById('file').addEventListener('change', function(e) {
        const status = document.getElementById('uploadStatus');
        if (this.files && this.files[0]) {
            status.textContent = `Selected file: ${this.files[0].name}`;
            status.classList.add('visible');
        } else {
            status.textContent = 'No file selected';
            status.classList.remove('visible');
        }
    });

    // Rename titles
    document.querySelectorAll('.title-container').forEach(container => {
        container.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    window.editTitle = function(e, index) {
        e.preventDefault();
        e.stopPropagation();
        const editForm = document.getElementById(`edit-${index}`);
        const input = document.getElementById(`input-${index}`);
        const titleLabel = document.querySelector(`#edit-${index}`).previousElementSibling;
        
        if (editForm) {
            titleLabel.style.display = 'none';
            editForm.style.display = 'block';
            input.focus();
            input.select();

            input.addEventListener('keypress', async function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    await saveTitle(e, index);
                }
            });
        }
    };

    window.saveTitle = async function(e, index) {
        e.preventDefault();
        e.stopPropagation();
        const input = document.getElementById(`input-${index}`);
        const newTitle = input.value;
        
        try {
            const response = await fetch(`/update_title/${index}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: newTitle })
            });
            
            if (response.ok) {
                const titleLabel = document.querySelector(`#edit-${index}`).previousElementSibling;
                titleLabel.textContent = newTitle;
                titleLabel.style.display = 'block';
                document.getElementById(`edit-${index}`).style.display = 'none';
                window.location.reload();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
});

