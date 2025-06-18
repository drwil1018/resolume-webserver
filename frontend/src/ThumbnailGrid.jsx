import { useState, useEffect, useRef } from "react";

// Get API URL from environment variables with fallback
import { API_URL } from "./api";

function ThumbnailGrid({ deck, loading, setLoading, selectedLayer, isDeleting }) {
    const [thumbnails, setThumbnails] = useState([]);
    const [titles, setTitles] = useState([]);
    const [selectedIndex, setSelectedIndex] = useState({
        '1': null,
        '8': null
    });
    const [error, setError] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const gridRef = useRef(null);

    async function fetchThumbnails() {
            setLoading(true);
            try {
                const response = await fetch(`${API_URL}/get_thumbnails?deck=${deck.toString()}&layer=${selectedLayer}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                  }
                const data = await response.json();
                setThumbnails(data.thumbnails);
                setTitles(data.titles);
                if (data.selection_index) {
                    setSelectedIndex(data.selection_index);
                }
                setLoading(false);
            } catch (error) {
                setError(error.message);
                setLoading(false);
            }
        }
        
    useEffect(() => {
        if (!deck) return;

        fetchThumbnails();
    }, [deck, selectedLayer, isDeleting]);

    useEffect(() => {
      const sendSelectedClip = async () => {
        if (selectedIndex) {
          await fetch(`${API_URL}/get_selected_clip`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              selected: selectedIndex,
              layer: selectedLayer
            }),
          });
        }
      }
      
      sendSelectedClip();
    }, [selectedIndex]);

    function handleThumbnailClick(index) {
        setSelectedIndex(index + 1);
        console.log(`Selected thumbnail index: ${index + 1}`);
    }

    // Drag and drop handlers
    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    };
    
    // Add this function to check if mouse is still over the element
    const isMouseOverElement = (e) => {
        if (!gridRef.current) return false;
        
        const rect = gridRef.current.getBoundingClientRect();
        const padding = 0;
        
        return (
            e.clientX >= (rect.left - padding) &&
            e.clientX <= (rect.right + padding) &&
            e.clientY >= (rect.top - padding) &&
            e.clientY <= (rect.bottom + padding)
        );
    };
    
    // Handle drag leave with position check
    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        // Only set isDragging to false if mouse is actually leaving the container
        if (!isMouseOverElement(e)) {
            setIsDragging(false);
        }
    };
    
    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };
    
    const handleDrop = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
        
        const files = Array.from(e.dataTransfer.files);
        const mediaFiles = files.filter(file => 
            file.type.startsWith('video/') || 
            file.type.startsWith('image/') || 
            file.name.match(/\.(mp4|mov|avi|wmv|flv|mkv|jpg|jpeg|png|gif|bmp|tiff|webp)$/i)
        );
        
        if (mediaFiles.length === 0) {
            alert('Please drop image or video files only.');
            return;
        }
        
        await uploadFiles(mediaFiles);
    };
    
    const uploadFiles = async (files) => {
        setLoading(true);
        
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            setUploadProgress(0);
            
            // Create FormData to send file
            const formData = new FormData();
            formData.append('file', file);
            formData.append('deck', deck);
            formData.append('layer', selectedLayer);
            
            try {
                const response = await fetch(`${API_URL}/upload_video`, {
                    method: 'POST',
                    body: formData,
                    // This allows us to track upload progress
                    onUploadProgress: (progressEvent) => {
                        const percentCompleted = Math.round(
                            (progressEvent.loaded * 100) / progressEvent.total
                        );
                        setUploadProgress(percentCompleted);
                    }
                });
                
                if (!response.ok) {
                    throw new Error(`Upload failed: ${response.statusText}`);
                }
                
                // Refresh thumbnails after successful upload
                await fetchThumbnails();
                
            } catch (error) {
                setError(`Upload failed: ${error.message}`);
                setLoading(false);
            }
        }
        
        setLoading(false);
    };

    return (
        <div 
            ref={gridRef}
            className={`grid-wrapper ${isDragging ? 'dragging' : ''}`}
            onDragEnter={handleDragEnter}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
        >
            {uploadProgress > 0 && uploadProgress < 100 && (
                <div className="upload-progress">
                    <div 
                        className="progress-bar" 
                        style={{ width: `${uploadProgress}%` }}
                    />
                    <span>{uploadProgress}%</span>
                </div>
            )}
            
            {loading ? (
                <div className="empty-state">Loading thumbnails...</div>
            ) : error ? (
                <div className="empty-state">Error loading thumbnails: {error}</div>
            ) : thumbnails.length === 0 ? (
                <div className="empty-state">
                    {isDragging ? (
                        <div className="upload-indicator">Drop video files here</div>
                    ) : (
                        <>
                            <div>No thumbnails available</div>
                            <div className="drop-hint">Drag and drop videos or images here to add content</div>
                        </>
                    )}
                </div>
            ) : (
                <div className="thumbnail-grid">
                    {thumbnails.map((thumbnail, index) => (
                        <div key={index} className="thumbnail-img">
                            <img
                                src={`data:image/jpeg;base64,${thumbnail}`}
                                alt={titles[index] || `Clip ${index + 1}`}
                                className={selectedIndex === index + 1 ? "selected" : ""}
                                onClick={() => handleThumbnailClick(index)}
                            />
                            <div className="thumbnail-label">{titles[index] || `Clip ${index + 1}`}</div>
                        </div>
                    ))}
                    
                    {/* Upload placeholder/indicator */}
                    {isDragging && (
                        <div className="upload-indicator">
                            <div>Drop video files here</div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default ThumbnailGrid;