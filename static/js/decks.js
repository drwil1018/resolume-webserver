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
});