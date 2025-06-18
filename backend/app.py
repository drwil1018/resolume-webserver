from flask import request, jsonify, session
import requests
import base64
from time import sleep
from config import app, base_url
import os
from werkzeug.utils import secure_filename
import logging
import platform

app.secret_key = "cowboy_hackz"

UPLOAD_FOLDER = 'resolume_uploads/'
ALLOWED_EXTENSIONS = {
    # Video formats
    'mp4', 'mov', 'avi', 'wmv', 'flv', 'mkv',
    # Image formats
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'
}

# Path translation for Docker
def is_running_in_docker():
    """Detect if we're running inside a Docker container"""
    # Check for .dockerenv file
    docker_env = os.path.exists('/.dockerenv')
    # Check container-specific cgroup
    try:
        with open('/proc/1/cgroup', 'rt') as f:
            return 'docker' in f.read() or docker_env
    except:
        return docker_env

# Docker environment flag
IS_DOCKER = is_running_in_docker()

# Host path (where Resolume can access files)
# This should be the absolute path on your host machine
HOST_PATH_PREFIX = '/Users/dylanprado/Documents/coding/resolume_webserver_react/backend'
# Docker container path prefix
CONTAINER_PATH_PREFIX = '/app'

def translate_path_for_resolume(file_path):
    """Translate a container path to a host path that Resolume can access"""
    if not IS_DOCKER:
        # If not running in Docker, return the path unchanged
        return file_path
    
    # Get absolute path
    abs_path = os.path.abspath(file_path)
    
    # Replace container path with host path if needed
    if abs_path.startswith(CONTAINER_PATH_PREFIX):
        translated_path = abs_path.replace(CONTAINER_PATH_PREFIX, HOST_PATH_PREFIX)
        print(f"Path translation: {abs_path} -> {translated_path}")
        return translated_path
    
    # If path doesn't need translation, return the original
    return abs_path

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_selected_layer():
    if 'selected_layer' not in session:
        session['selected_layer'] = '1'
    return session['selected_layer']

def set_selected_layer(layer):
    session['selected_layer'] = str(layer)

def get_selected_clip(layer=None):
    if layer is None:
        layer = session.get('selected_layer')
    else:
        layer = str(layer)

    if 'selected_clips' not in session:
        session['selected_clips'] = {
            '1': None,
            '8': None,
        }
    
    return session['selected_clips'].get(layer)

def set_selected_clip(clip_index, layer=None):
    if layer is None:
        layer = session.get('selected_layer')
    else:
        layer = str(layer)

    if 'selected_clips' not in session:
        session['selected_clips'] = {
            '1': None,
            '8': None,
        }
    
    session['selected_clips'][layer] = clip_index

@app.route('/deck_selection', methods=['POST'])
def deck_selection():
    session['deck'] = request.json.get('deck')
    deck = session.get('deck')
    requests.post(f"{base_url}/composition/decks/{deck}/select")
    sleep(0.5)
    requests.put(f"{base_url}/composition/layers/1",
                        json={"video": {"opacity": {"value": 1.0}}})
    
    for layer in range(2, 10):
        requests.put(f"{base_url}/composition/layers/{layer}",
                        json={"video": {"opacity": {"value": 0.0}}})
    # Reset the master layer to 1.0 opacity
    requests.put(f"{base_url}/composition", json={"master": {"value": 1.0}})
    
    return jsonify({'deck': deck})

@app.route('/get_thumbnails', methods=['GET'])
def get_thumbnails():
    deck = request.args.get('deck')
    layer = request.args.get('layer', '1')  # Default to layer 1 if not specified
    set_selected_layer(layer)

    
    if not deck:
        return jsonify({'error': 'No deck specified'}), 400
    sleep(0.5)
    
    thumbnails = []
    titles = []
    clip_index = 1
    selection_index = None
    
    while True:
        thumbnail = requests.get(f"{base_url}/composition/layers/{layer}/clips/{clip_index}/thumbnail")
        decoded_thumbnail = base64.b64encode(thumbnail.content).decode("utf-8")
        clip_data = requests.get(f"{base_url}/composition/layers/{layer}/clips/{clip_index}")
        title = clip_data.json().get('name', {}).get('value')
        selection = clip_data.json().get('selected', {}).get('value')
        
        if selection == True:
            set_selected_clip(clip_index)

        if len(decoded_thumbnail) > 528:
            thumbnails.append(decoded_thumbnail)
            titles.append(title)
            clip_index += 1
        else:
            break
    
    return jsonify({
        'thumbnails': thumbnails,
        'titles': titles,
        'selection_index': session.get('selected_clips', {})
    })

@app.route('/select_output', methods=['POST'])
def select_output():
    output = request.json.get('isOutputSelected')
    layer = 8
    if output:
        requests.put(f"{base_url}/composition/layers/{layer}",
                        json={"video": {"opacity": {"value": 1.0}}})
        
    else:
        requests.put(f"{base_url}/composition/layers/{layer}",
                        json={"video": {"opacity": {"value": 0.0}}})
        
    return jsonify({'success': True})

@app.route('/get_selected_clip', methods=['POST', 'GET'])
def handle_selected_clip():
    selected = request.json.get('selected')
    layer = request.json.get('layer', '1')  # Default to layer 1 if not specified
    
    requests.post(f"{base_url}/composition/layers/{layer}/clips/{selected}/select")
    requests.post(f"{base_url}/composition/layers/{layer}/clips/{selected}/connect")

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
    try:
        response = requests.get(f"{base_url}/composition/clips/selected")
        data = response.json()

        effects = data.get('video', {}).get('effects', [])
        
        # Default values in case we can't fetch from Resolume
        effect_values = {
            "zoom": 100,
            "shiftX": 0,
            "shiftY": 0,
            "exposure": 0.5,
            "hue": 0,
            "saturation": 1,
        }
        
        # Only try to get values if we have enough effects
        if len(effects) >= 3:
            try:
                effect_values.update({
                    "zoom": round(effects[0].get('params', {}).get('Scale', {}).get('value', 100)),
                    "shiftX": round(effects[0].get('params', {}).get('Position X', {}).get('value', 0)),
                    "shiftY": round(effects[0].get('params', {}).get('Position Y', {}).get('value', 0)),
                    "exposure": round(float(effects[1].get('params', {}).get('Exposure', {}).get('value', 0.5)), 2),
                    "hue": round(float(effects[2].get('params', {}).get('Hue Rotate', {}).get('value', 0)), 2),
                    "saturation": round(float(effects[2].get('params', {}).get('Sat. Scale', {}).get('value', 1)), 2),
                })
            except (IndexError, TypeError, ValueError) as e:
                print(f"Error parsing effect values: {e}")
                # We'll use the default values defined above
        
        return jsonify(effect_values)
    except Exception as e:
        print(f"Error in get_effects: {e}")
        return jsonify({
            "error": str(e),
            "zoom": 100,
            "shiftX": 0,
            "shiftY": 0,
            "exposure": 0.5,
            "hue": 0,
            "saturation": 1,
        }), 500

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
            
            # Get the layer parameter from the form data
            layer = request.form.get('layer', '1')  # Default to layer 1
            
            select_last_clip(layer)
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

def select_last_clip(layer='1'):
    clip_index = 0

    while True:
        clip_index += 1
        response = requests.get(f"{base_url}/composition/layers/{layer}/clips/{clip_index}")
        thumbnail_default = response.json().get('thumbnail', {}).get('is_default')

        if response.status_code != 200 or thumbnail_default == True:
            break

    requests.post(f"{base_url}/composition/layers/{layer}/clips/{clip_index}/select")
    requests.post(f"{base_url}/composition/layers/{layer}/clips/{clip_index}/connect")

def add_video_to_resolume(file_path):
    # First verify file exists and is readable
    if not os.path.isfile(file_path):
        print(f"Error: File not found or not accessible: {file_path}")
        return {'error': 'File not found or not accessible'}
    
    # Translate path for Resolume (only changes in Docker)
    resolume_path = translate_path_for_resolume(file_path)
    print(f"Original file path: {file_path}")
    print(f"Translated for Resolume: {resolume_path}")
    
    with open(file_path, 'rb') as file:
        # Use the translated path when sending to Resolume
        file_url = f"file://{resolume_path}"
        print(f"Sending to Resolume: {file_url}")
        
        response = requests.post(
            f"{base_url}/composition/clips/selected/open",
            data=file_url)
        
        # Additional error checking
        if response.status_code != 200:
            print(f"Error from Resolume API: Status {response.status_code}, Response: {response.text}")
    
    return response.json() if response.text else {'success': True}

def add_image_to_resolume(file_path):
    # First verify file exists and is readable
    if not os.path.isfile(file_path):
        print(f"Error: File not found or not accessible: {file_path}")
        return {'error': 'File not found or not accessible'}
    
    # Translate path for Resolume (only changes in Docker)
    resolume_path = translate_path_for_resolume(file_path)
    print(f"Original file path: {file_path}")
    print(f"Translated for Resolume: {resolume_path}")
    
    with open(file_path, 'rb') as file:
        # Use the translated path when sending to Resolume
        file_url = f"file://{resolume_path}"
        print(f"Sending to Resolume: {file_url}")
        
        response = requests.post(
            f"{base_url}/composition/clips/selected/open",
            data=file_url)
        
        # Additional error checking
        if response.status_code != 200:
            print(f"Error from Resolume API: Status {response.status_code}, Response: {response.text}")
        
    return response.json() if response.text else {'success': True}

@app.route('/clear_all', methods=['POST'])
def clear_all():
    layer = request.args.get('selectedLayer', '1')  # Default to layer 1 if not specified
    try:
        response = requests.post(f"{base_url}/composition/layers/{layer}/clearclips")
        upload_folder = UPLOAD_FOLDER
        for file in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        if response.status_code != 204:
            return jsonify({'error': 'Failed to clear clips'}), 500
            
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error clearing clips: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)