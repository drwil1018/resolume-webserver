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
    const slider = document.getElementById('exposure');
    const display = document.getElementById('exposureValue');
    
    if (slider && display) {
        slider.addEventListener('input', async (e) => {
            const value = e.target.value;
            display.textContent = value;

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