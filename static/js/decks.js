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

    // Thumbnail selection
    const currrentDeck = window.location.pathname.split('/').pop();
    storedDeck = sessionStorage.getItem('currentDeck');
    if (storedDeck && storedDeck !== currrentDeck) {
        sessionStorage.removeItem('selectedClipIndex');
    }
    sessionStorage.setItem('currentDeck', currrentDeck);
    let selectedThumbnail = null;
    const storedIndex = sessionStorage.getItem('selectedClipIndex');
    
    if (storedIndex) {
        const imgs = document.querySelectorAll('.thumbnail-grid img');
        selectedThumbnail = imgs[storedIndex - 1];
        selectedThumbnail.classList.add('selected');
    }

    document.querySelectorAll(".thumbnail-grid img").forEach((img, index) => {
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
});