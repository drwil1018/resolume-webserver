from flask import *
import requests
import logging
from werkzeug.utils import secure_filename
import os
from utils import select_deck, check_effects, store_effects, apply_effects, store_effects_index
from time import sleep


app = Flask(__name__, template_folder="templates", static_url_path='', static_folder="static")
app.secret_key = "cowboy_hacker_69"
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
        

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Development configuration
app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True
)

base_url = "http://localhost:8080/api/v1"

@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/deck1")
def deck1():
    session['exposure_page'] = False
    session['color_page'] = False
    session['transform_page'] = False
    session['current_deck'] = "deck1"
    select = requests.post(f"{base_url}/composition/decks/1/select")
    session['layer_index'] = 1
    layer_index = session.get("layer_index")
    sleep(0.3)

    effect_values = store_effects(base_url)
    session["effect_values_cancel"] = effect_values
    
    if session.get("sides_on") is not True:
        try:
            update, update2, thumbnails, total_clips, titles, selection_index = select_deck(layer_index, base_url)
            session["total_clips"] = total_clips
            
            if select.status_code != 204:
                flash(f'Error: {select.status_code}', 'error, could not select deck')
                deck = session.get("current_deck")
                return render_template(f"{deck}.html")
            elif update.status_code != 204:
                flash(f'Error: {update.status_code}', 'error, could not update layer data')
                deck = session.get("current_deck")
                return render_template(f"{deck}.html")
            elif update2.status_code != 204:
                flash(f'Error: {update.status_code}', 'error, could not update layer data')
                deck = session.get("current_deck")
                return render_template(f"{deck}.html")
            
            deck = session.get("current_deck")
            return render_template(f"{deck}.html", thumbnails=thumbnails, titles=titles, selection_index=selection_index, zip=zip)
        
    
        except requests.RequestException as e:
            flash(f'Connection error: {str(e)}', 'error')
            deck = session.get("current_deck")
            return render_template(f"{deck}.html")
    else:
        deck = session.get("current_deck")
        return redirect(url_for("select_sides"))

@app.route("/deck2")
def deck2():
    session['exposure_page'] = False
    session['color_page'] = False
    session['transform_page'] = False
    session['current_deck'] = "deck2"
    select = requests.post(f"{base_url}/composition/decks/2/select")
    session['layer_index'] = 1
    layer_index = session.get("layer_index")
    sleep(0.3)

    effect_values = store_effects(base_url)
    session["effect_values_cancel"] = effect_values

    if session.get("sides_on") is not True:
        try:
            update, update2, thumbnails, total_clips, titles, selection_index = select_deck(layer_index, base_url)
            session["total_clips"] = total_clips
            
            if select.status_code != 204:
                flash(f'Error: {select.status_code}', 'error, could not select deck')
                deck = session.get("current_deck")
                return render_template(f"{deck}.html")
            elif update.status_code != 204:
                flash(f'Error: {update.status_code}', 'error, could not update layer data')
                deck = session.get("current_deck")
                return render_template(f"{deck}.html")
            elif update2.status_code != 204:
                flash(f'Error: {update.status_code}', 'error, could not update layer data')
                deck = session.get("current_deck")
                return render_template(f"{deck}.html")
            
            deck = session.get("current_deck")
            return render_template(f"{deck}.html", thumbnails=thumbnails, titles=titles, selection_index=selection_index, zip=zip)
        
    
        except requests.RequestException as e:
            flash(f'Connection error: {str(e)}', 'error')
            deck = session.get("current_deck")
            return render_template(f"{deck}.html")
    else:
        deck = session.get("current_deck")
        return redirect(url_for("select_sides"))
    
@app.route("/deck3")
def deck3():
    session['exposure_page'] = False
    session['color_page'] = False
    session['transform_page'] = False
    session['current_deck'] = "deck3"
    select = requests.post(f"{base_url}/composition/decks/3/select")
    session['layer_index'] = 1
    layer_index = session.get("layer_index")
    sleep(0.3)

    effect_values = store_effects(base_url)
    session["effect_values_cancel"] = effect_values

    if session.get("sides_on") is not True:
        try:
            update, update2, thumbnails, total_clips, titles, selection_index = select_deck(layer_index, base_url)
            session["total_clips"] = total_clips
            
            if select.status_code != 204:
                flash(f'Error: {select.status_code}', 'error, could not select deck')
                deck = session.get("current_deck")
                return render_template(f"{deck}.html")
            elif update.status_code != 204:
                flash(f'Error: {update.status_code}', 'error, could not update layer data')
                deck = session.get("current_deck")
                return render_template(f"{deck}.html")
            elif update2.status_code != 204:
                flash(f'Error: {update.status_code}', 'error, could not update layer data')
                deck = session.get("current_deck")
                return render_template(f"{deck}.html")
            
            deck = session.get("current_deck")
            return render_template(f"{deck}.html", thumbnails=thumbnails, titles=titles, selection_index=selection_index, zip=zip)
        
    
        except requests.RequestException as e:
            flash(f'Connection error: {str(e)}', 'error')
            deck = session.get("current_deck")
            return render_template(f"{deck}.html")
    else:
        deck = session.get("current_deck")
        return redirect(url_for("select_sides"))

@app.route("/data")
def data():
    try:
        response = requests.get(f"{base_url}/composition/layers/1/clips/1")
        
        if response.status_code != 200:
            flash('Error: Could not complete request', 'error')
            return render_template("data.html")
        
        flash('Data retrieved successfully', 'success')
        return render_template("data.html", data=response.json())
        
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        return render_template("data.html")
    
@app.route("/select_clip/<int:clip_index>")
def select_clip(clip_index):
    layer_index = session.get("layer_index")
    session["clip_index"] = clip_index
    try:
        select = requests.post(f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}/select")
        connect = requests.post(f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}/connect")

        if select.status_code != 204 or connect.status_code != 204:
            flash(f'Error: {select.status_code}', 'error, could not select clip')
        else:
            current_deck = session.get("current_deck")
            return redirect(url_for(current_deck))

    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
    
@app.route("/edit")
def edit():
    layer_index = session.get("layer_index")
    update, update2, thumbnails, total_clips, titles, selection_index = select_deck(layer_index, base_url)
    effects = ["effect:///video/Exposure", "effect:///video/Hue%20Rotate", ]
    expose_value, hue_value, scale_value, shiftx_value, shifty_value, sat_value = check_effects(base_url)
    try:
        if session.get("effects") is False:
            for effect in effects:
                response = requests.post(f"{base_url}/composition/clips/selected/effects/video/add", data=effect)

                if response.status_code != 204:
                    flash(f'Error: {response.status_code}', 'error, could not add effect')

        current_deck = session.get("current_deck")
        return render_template("edit.html", expose_value=expose_value, hue_value=hue_value, sat_value=sat_value, scale_value=scale_value, shiftx_value=shiftx_value, shifty_value=shifty_value, titles=titles, selection_index=selection_index)
    
    except TypeError as e:  
        flash(f'Please select a clip', 'error, please sleect a clip')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))      
    
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
    
@app.route("/default_effects_deck")
def default_effects_deck():
    try:
        resest_scale = requests.put(
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

        resest_shiftx = requests.put(
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

        resest_shifty = requests.put(
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

        if resest_scale.status_code != 204:
            flash(f'Error: Reset of transform failed', 'error, could not resest transform effects')

        while True:
            response = requests.delete(f"{base_url}/composition/clips/selected/effects/video/1")
            if response.status_code == 204:
                continue
            else:
                break
        
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
        
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
    
@app.route("/update_exposure", methods=["POST"])
def update_exposure():
    try:
        value = request.json.get("value")
        response = requests.put(
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

        if response.status_code != 204:
            return jsonify({"error": "Failed to update exposure"}), 400
        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/update_hue", methods=["POST"])
def update_hue():
    try:
        value = request.json.get("value")
        response = requests.put(
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

        if response.status_code != 204:
            return jsonify({"error": "Failed to update exposure"}), 400
        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/update_sat", methods=["POST"])
def update_sat():
    try:
        value = request.json.get("value")
        response = requests.put(
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

        if response.status_code != 204:
            return jsonify({"error": "Failed to update exposure"}), 400
        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/update_scale", methods=["POST"])
def update_scale():
    try:
        value = request.json.get("value")
        response = requests.put(
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

        if response.status_code != 204:
            return jsonify({"error": "Failed to update exposure"}), 400
        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/update_shiftx", methods=["POST"])
def update_shiftx():
    try:
        value = request.json.get("value")
        response = requests.put(
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

        if response.status_code != 204:
            return jsonify({"error": "Failed to update exposure"}), 400
        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/update_shifty", methods=["POST"])
def update_shifty():
    try:
        value = request.json.get("value")
        response = requests.put(
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

        if response.status_code != 204:
            return jsonify({"error": "Failed to update exposure"}), 400
        return jsonify({"success": True}), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/save")
def save():
    current_deck = session.get("current_deck")
    return redirect(url_for(current_deck))
     
@app.route("/upload_file", methods=["POST"])
def upload_file():
    
    if 'file' not in request.files:
        flash('No file part', 'error')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
    
    file = request.files['file']
    total_clips = session.get("total_clips")
    

    if file.filename == '':
        flash('No selected file', 'error')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
    
    if file:
        select_clip(total_clips + 1)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_updload = os.path.abspath(file_path)
        resquest = requests.post(f"{base_url}/composition/clips/selected/open", data=f"file://{file_updload}")

        if resquest.status_code != 204:
            flash(f'Error: {resquest.status_code}', 'error, could not upload file')
            current_deck = session.get("current_deck")
            return redirect(url_for(current_deck))

        print(file_updload)
        flash('File successfully uploaded', 'success')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
   
@app.route("/clear_all")
def clear_all():
    layer_index = session.get("layer_index")
    try:
        response = requests.post(f"{base_url}/composition/layers/{layer_index}/clearclips")

        upload_folder = app.config['UPLOAD_FOLDER']
        for file in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                flash (f'Error: {str(e)}', 'error, could not delete file')

        if response.status_code != 204:
            flash(f'Error: {response.status_code}', 'error, could not clear all')
        else:
            current_deck = session.get("current_deck")
            return redirect(url_for(current_deck))
        
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))

@app.route("/select_sides")
def select_sides():
    session['layer_index'] = 3
    session['sides_on'] = True
    layer_index = session.get("layer_index")
    try:
        update, update2, thumbnails, total_clips, titles, selection_index = select_deck(layer_index, base_url)
        session["total_clips"] = total_clips
        if update.status_code != 204:
            flash(f'Error: {update.status_code}', 'error, could not update layer data')
            deck = session.get("current_deck")
            return render_template(f"{deck}.html")
        elif update2.status_code != 204:
            flash(f'Error: {update.status_code}', 'error, could not update layer data')
            deck = session.get("current_deck")
            return render_template(f"{deck}.html")
        
        deck = session.get("current_deck")
        return render_template(f"{deck}.html", thumbnails=thumbnails, titles=titles, selection_index=selection_index, zip=zip)
        
    
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        deck = session.get("current_deck")
        return render_template(f"{deck}.html")

@app.route("/select_center")
def select_center():
    layer_index = session['layer_index'] = 1
    session['sides_on'] = False
    update, update2, thumbnails, total_clips, titles, selection_index = select_deck(layer_index, base_url)
    deck = session.get("current_deck")
    return render_template(f"{deck}.html", thumbnails=thumbnails, titles=titles, selection_index=selection_index, zip=zip)

@app.route("/update_title/<int:clip_index>", methods=["POST"])
def update_title(clip_index):
    try:
        new_title = request.json.get("title")
        layer_index = session.get("layer_index")
        response = requests.put(
            f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}",
            json={"name": {"value": new_title}}
        )
        
        if response.status_code != 204:
            return jsonify({"error": "Failed to update title"}), 400
        
        return jsonify({"success": True, "title": new_title}), 200
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/exposure_page")
def exposure_page():
    session["exposure_page"] = True
    session["color_page"] = False
    session["transform_page"] = False
    return redirect(url_for("edit"))

@app.route("/color_page")
def color_page():
    session["color_page"] = True
    session["exposure_page"] = False
    session["transform_page"] = False
    return redirect(url_for("edit"))

@app.route("/transform_page")
def transform_page():
    session["transform_page"] = True
    session["exposure_page"] = False
    session["color_page"] = False
    return redirect(url_for("edit"))

@app.route("/delete_clip")
def delete_clip():
    layer_index = session.get("layer_index")
    update, update2, thumbnails, total_clips, titles, selection_index = select_deck(layer_index, base_url)
    try:
        response = requests.post(f"{base_url}/composition/clips/selected/clear")
        while selection_index < total_clips:
            clip_index = selection_index + 1
            path_request = requests.get(f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}")
            effect_values = store_effects_index(base_url, layer_index, clip_index)
            path = path_request.json().get('video', {}).get('fileinfo', {}).get('path')
            file_updload = os.path.abspath(path).replace(" ", "%20")
            resquest = requests.post(f"{base_url}/composition/layers/{layer_index}/clips/{selection_index}/open", data=f"file://{file_updload}")
            if effect_values is not None:
                update_exposure, update_hue, update_scale, update_shiftx, update_shifty, update_sat = apply_effects(base_url, layer_index, selection_index, effect_values[0], effect_values[1], effect_values[2], effect_values[3], effect_values[4], effect_values[5])

            if resquest.status_code != 204:
                flash(f'Error: {resquest.status_code}, could not move clips', 'error, could not open clip')
                deck = session.get("current_deck")
                return redirect(url_for(deck))
            
            selection_index += 1

        requests.post(f"{base_url}/composition/layers/{layer_index}/clips/{total_clips}/select")
        sleep(0.1)
        requests.post(f"{base_url}/composition/clips/selected/clear")

        if response.status_code != 204:
            flash(f'Error: {response.status_code}', 'error, could not delete clip')
            deck = session.get("current_deck")
            return redirect(url_for(deck))
        
        deck = session.get("current_deck")
        return redirect(url_for(deck))
        
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        deck = session.get("current_deck")
        return redirect(url_for(deck))

@app.route("/cancel_edit")
def cancel_edit():
    effect_values = session.get("effect_values_cancel")
    print(effect_values)
    if effect_values is not None:
        update_exposure, update_hue, update_scale, update_shiftx, update_shifty, update_sat = apply_effects(base_url, session.get("layer_index"), session.get("clip_index"), effect_values[0], effect_values[1], effect_values[2], effect_values[3], effect_values[4], effect_values[5])
    else:
        default_effects_deck()
    
    current_deck = session.get("current_deck")
    return redirect(url_for(current_deck))

@app.route("/reset_effect/<effect_id>", methods=["POST"])
def reset_effect(effect_id):
    try:
        value = request.json.get("value")
        layer_index = session.get("layer_index")

        if effect_id == "exposure":
            response = requests.put(
                f"{base_url}/composition/clips/selected",
                json={
                    "video": {
                        "effects": [
                            {},
                            {
                                "params": {
                                    "Exposure": {
                                        "value": value
                                    }
                                }
                            }
                        ]
                    }
                }
            )

        elif effect_id == "hue":
            response = requests.put(
                f"{base_url}/composition/clips/selected",
                json={
                    "video": {
                        "effects": [
                            {}, {},
                            {
                                "params": {
                                    "Hue Rotate": {
                                        "value": value
                                    }
                                }
                            }
                        ]
                    }
                }
            )

        elif effect_id == "sat":
            response = requests.put(
                f"{base_url}/composition/clips/selected",
                json={
                    "video": {
                        "effects": [
                            {}, {},
                            {
                                "params": {
                                    "Sat. Scale": {
                                        "value": value
                                    }
                                }
                            }
                        ]
                    }
                }
            )
        
        elif effect_id == "scale":
            response = requests.put(
                f"{base_url}/composition/clips/selected",
                json={
                    "video": {
                        "effects": [
                            {
                                "params": {
                                    "Scale": {
                                        "value": value
                                    }
                                }
                            }
                        ]
                    }
                }
            )
        
        elif effect_id == "shiftx":
            response = requests.put(
                f"{base_url}/composition/clips/selected",
                json={
                    "video": {
                        "effects": [
                            {
                                "params": {
                                    "Position X": {
                                        "value": value
                                    }
                                }
                            }
                        ]
                    }
                }
            )
        
        elif effect_id == "shifty":
            response = requests.put(
                f"{base_url}/composition/clips/selected",
                json={
                    "video": {
                        "effects": [
                            {
                                "params": {
                                    "Position Y": {
                                        "value": value
                                    }
                                }
                            }
                        ]
                    }
                }
            )
        
        if response.status_code != 204:
            return jsonify({"error": "Failed to reset effect"}), 400
        return jsonify({"success": True}), 200
    
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=True,
        host="0.0.0.0",
        port=5000,
        threaded=True
        )
