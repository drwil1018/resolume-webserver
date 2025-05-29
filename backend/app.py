from flask import request, jsonify, session
import requests
import base64
from time import sleep
from config import app, base_url
import os
from werkzeug.utils import secure_filename
import logging

app.secret_key = "cowboy_hackz"

UPLOAD_FOLDER = 'resolume_uploads/'
ALLOWED_EXTENSIONS = {
    # Video formats
    'mp4', 'mov', 'avi', 'wmv', 'flv', 'mkv',
    # Image formats
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'
}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/deck_selection', methods=['POST'])
def deck_selection():
    session['deck'] = request.json.get('deck')
    deck = session.get('deck')
    requests.post(f"{base_url}/composition/decks/{deck}/select")
    
    return jsonify({'deck': deck})

@app.route('/get_thumbnails', methods=['GET'])
def get_thumbnails():
    deck = request.args.get('deck')
    if not deck:
        return jsonify({'error': 'No deck specified'}), 400
    sleep(0.5)
    
    thumbnails = []
    titles = []
    clip_index = 1
    selection_index = None
    
    while True:
        thumbnail = requests.get(f"{base_url}/composition/layers/1/clips/{clip_index}/thumbnail")
        decoded_thumbnail = base64.b64encode(thumbnail.content).decode("utf-8")
        clip_data = requests.get(f"{base_url}/composition/layers/1/clips/{clip_index}")
        title = clip_data.json().get('name', {}).get('value')
        selection = clip_data.json().get('selected', {}).get('value')
        
        if selection == True:
            selection_index = clip_index
        
        if len(decoded_thumbnail) > 528:
            thumbnails.append(decoded_thumbnail)
            titles.append(title)
            clip_index += 1
        else:
            break
    
    return jsonify({
        'thumbnails': thumbnails,
        'titles': titles,
    })

@app.route('/get_selected_clip', methods=['POST'])
def get_selected_clip():
    selected = request.json.get('selected')
    requests.post(f"{base_url}/composition/layers/1/clips/{selected}/select")
    requests.post(f"{base_url}/composition/layers/1/clips/{selected}/connect")

    return jsonify({'selected': selected})

@app.route("/update_exposure", methods=["POST"])
def update_exposure():
    try:
        value = request.json.get("value")
        requests.put(
            f"{base_url}/composition/clips/selected",
            json={
                "video": {
                    "effects": [
                        {},
                            {
                                "params": {
                                    "Exposure": {
                                        "value": float(value)
                                    }
                                }
                            }
                    ]
                }
            }
        )

        return jsonify({"success": True})

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_hue", methods=["POST"])
def update_hue():
    try:
        value = request.json.get("value")
        requests.put(
            f"{base_url}/composition/clips/selected",
            json={
                "video": {
                    "effects": [
                        {}, {},
                            {
                                "params": {
                                    "Hue Rotate": {
                                        "value": float(value)
                                    }
                                }
                            }
                    ]
                }
            }
        )

        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_saturation", methods=["POST"])
def update_sat():
    try:
        value = request.json.get("value")
        requests.put(
            f"{base_url}/composition/clips/selected",
            json={
                "video": {
                    "effects": [
                        {}, {},
                            {
                                "params": {
                                    "Sat. Scale": {
                                        "value": float(value)
                                    }
                                }
                            }
                    ]
                }
            }
        )

        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/update_zoom", methods=["POST"])
def update_scale():
    try:
        value = request.json.get("value")
        requests.put(
            f"{base_url}/composition/clips/selected",
            json={
                "video": {
                    "effects": [

                            {
                                "params": {
                                    "Scale": {
                                        "value": float(value)
                                    }
                                }
                            }
                    ]
                }
            }
        )

        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_shiftX", methods=["POST"])
def update_shiftx():
    try:
        value = request.json.get("value")
        requests.put(
            f"{base_url}/composition/clips/selected",
            json={
                "video": {
                    "effects": [

                            {
                                "params": {
                                    "Position X": {
                                        "value": float(value)
                                    }
                                }
                            }
                    ]
                }
            }
        )

        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/update_shiftY", methods=["POST"])
def update_shifty():
    try:
        value = request.json.get("value")
        requests.put(
            f"{base_url}/composition/clips/selected",
            json={
                "video": {
                    "effects": [

                            {
                                "params": {
                                    "Position Y": {
                                        "value": float(value)
                                    }
                                }
                            }
                    ]
                }
            }
        )

        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/edit_clip" , methods=["POST"])
def edit_clip():
    effect_pool = ["effect:///video/Exposure", "effect:///video/Hue%20Rotate", ]
    is_editing = request.json.get("isEditing")
    response = requests.get(f"{base_url}/composition/clips/selected")
    data = response.json()

    effects = data.get('video', {}).get('effects', [])
    count = len(effects)

    if is_editing and len(effects) != 3:
        while count > 1:
            requests.delete(f"{base_url}/composition/clips/selected/effects/video/1")
            count -= 1

        for effect in effect_pool:
            requests.post(f"{base_url}/composition/clips/selected/effects/video/add", data=effect)
        



    return jsonify({"isEditing": is_editing})

@app.route("/reset_effects", methods=["POST"])
def reset_effects():
    response = requests.get(f"{base_url}/composition/clips/selected")
    data = response.json()

    effects = data.get('video', {}).get('effects', [])
    count = len(effects)

    if len(effects) > 1:
        while count > 1:
            requests.delete(f"{base_url}/composition/clips/selected/effects/video/1")
            count -= 1

        update_scale = requests.put(
            f"{base_url}/composition/clips/selected",
            json={
                "video": {
                    "effects": [
                            {
                                "params": {
                                    "Scale": {
                                        "value": 100
                                    }
                                }
                            }
                    ]
                }
            }
        )
    
        update_shiftx = requests.put(
            f"{base_url}/composition/clips/selected",
            json={
                "video": {
                    "effects": [
                            {
                                "params": {
                                    "Position X": {
                                        "value": 0
                                    }
                                }
                            }
                    ]
                }
            }
        )
    
    update_shifty = requests.put(
            f"{base_url}/composition/clips/selected",
            json={
                "video": {
                    "effects": [
                            {
                                "params": {
                                    "Position Y": {
                                        "value": 0
                                    }
                                }
                            }
                    ]
                }
            }
        )


    return jsonify({"success": True})

@app.route("/get_effects", methods=["GET"])
def get_effects():
    response = requests.get(f"{base_url}/composition/clips/selected")
    data = response.json()

    effects = data.get('video', {}).get('effects', [])
    effect_values = {
        "zoom" : round(effects[0].get('params', {}).get('Scale', {}).get('value')),
        "shiftX" : round(effects[0].get('params', {}).get('Position X', {}).get('value')),
        "shiftY" : round(effects[0].get('params', {}).get('Position Y', {}).get('value')),
        "exposure" : round(effects[1].get('params', {}).get('Exposure', {}).get('value'), 2),
        "hue" : round(effects[2].get('params', {}).get('Hue Rotate', {}).get('value'), 2),
        "saturation" : round(effects[2].get('params', {}).get('Sat. Scale', {}).get('value'), 2),
    }

    return jsonify(effect_values)

@app.route('/upload_media', methods=['POST'])
def upload_media():
    # Print diagnostic information
    print(f"Current directory: {os.getcwd()}")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Upload folder exists: {os.path.exists(UPLOAD_FOLDER)}")
    print(f"Upload folder is writable: {os.access(UPLOAD_FOLDER, os.W_OK)}")
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    deck = request.form.get('deck')
    
    print(f"Received file: {file.filename}, Content-Type: {file.content_type}")
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        # Ensure directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            try:
                os.makedirs(UPLOAD_FOLDER)
                print(f"Created directory: {UPLOAD_FOLDER}")
            except Exception as e:
                print(f"Error creating directory: {e}")
                return jsonify({'error': f"Could not create upload directory: {str(e)}"}), 500
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        try:
            print(f"Saving file to: {file_path}")
            file.save(file_path)
            print(f"File saved? {os.path.exists(file_path)}")
            print(f"File size: {os.path.getsize(file_path) if os.path.exists(file_path) else 0} bytes")
            
            file_upload = os.path.abspath(file_path)
            
            # Determine if the file is an image or video based on content type
            is_image = file.content_type.startswith('image/')
            
            select_last_clip()
            sleep(0.3)
            
            # Add the media to Resolume via API
            if is_image:
                result = add_image_to_resolume(file_upload)
            else:
                result = add_video_to_resolume(file_upload)
            
            media_type = "image" if is_image else "video"
            return jsonify({'success': True, 'message': f'{media_type} uploaded successfully', 'type': media_type})
            
        except Exception as e:
            print(f"Error saving file: {e}")
            return jsonify({'error': f"Failed to save file: {str(e)}"}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/upload_video', methods=['POST'])
def upload_video():
    return upload_media()

def select_last_clip():
    clip_index = 0

    while True:
        clip_index += 1
        response = requests.get(f"{base_url}/composition/layers/1/clips/{clip_index}")
        thumbnail_default = response.json().get('thumbnail', {}).get('is_default')

        if response.status_code != 200 or thumbnail_default == True:
            break

    requests.post(f"{base_url}/composition/layers/1/clips/{clip_index}/select")
    requests.post(f"{base_url}/composition/layers/1/clips/{clip_index}/connect")

def add_video_to_resolume(file_path):
    
    with open(file_path, 'rb') as file:
        response = requests.post(
            f"{base_url}/composition/clips/selected/open",
            data=f"file://{file_path}")
        
    
    return response.json() if response.text else {'success': True}

def add_image_to_resolume(file_path):
    """
    Add an image file to Resolume Arena via its API
    Similar to add_video_to_resolume but might have different parameters/handling
    """
    with open(file_path, 'rb') as file:
        response = requests.post(
            f"{base_url}/composition/clips/selected/open",
            data=f"file://{file_path}")
        
    return response.json() if response.text else {'success': True}

if __name__ == '__main__':
    app.run(debug=True)