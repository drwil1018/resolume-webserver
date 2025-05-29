import { useState } from "react";

function BottomButtons({ isEditing, setIsEditing }) {

    const [needsDeleting, setNeedsDeleting] = useState(false);
    const [needsDeletingAll, setNeedsDeletingAll] = useState(false);

    function handleEdit() {
        setIsEditing(true);
    }

    function handleDeleteSingle() {
        setNeedsDeleting(true);
    }

    function handleDeleteAll() {
        setNeedsDeletingAll(true);
    }

    return (
        <div className="button-container">
            <button className="button" onClick={handleEdit}>Edit</button>
        </div>
    );
}

export default BottomButtons;