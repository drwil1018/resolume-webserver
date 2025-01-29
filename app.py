from flask import *
import requests
import logging
from werkzeug.utils import secure_filename
import os
from utils import select_deck, check_effects


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
    session['current_deck'] = "deck1"
    deck_index = 1
    try:
        select, update, update2, thumbnails, total_clips, titles = select_deck(deck_index, base_url)
        session["total_clips"] = total_clips
        expose_value = check_effects(base_url)
        if expose_value is not None:
            session["show_slider"] = True
        else:
            session.pop("show_slider", None)

        
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
        return render_template(f"{deck}.html", thumbnails=thumbnails, expose_value=expose_value, titles=titles, zip=zip)
        
    
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        deck = session.get("current_deck")
        return render_template(f"{deck}.html")

@app.route("/deck2")
def deck2():
    session['current_deck'] = "deck2"
    deck_index = 2
    try:
        select, update, update2, thumbnails, total_clips, titles = select_deck(deck_index, base_url)
        session["total_clips"] = total_clips
        expose_value = check_effects(base_url)
        if expose_value is not None:
            session["show_slider"] = True
        else:
            session.pop("show_slider", None)

        
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
        return render_template(f"{deck}.html", thumbnails=thumbnails, expose_value=expose_value, titles=titles, zip=zip)
        
    
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        deck = session.get("current_deck")
        return render_template(f"{deck}.html")
    
@app.route("/deck3")
def deck3():
    session['current_deck'] = "deck3"
    deck_index = 3
    try:
        select, update, update2, thumbnails, total_clips, titles = select_deck(deck_index, base_url)
        session["total_clips"] = total_clips
        expose_value = check_effects(base_url)
        if expose_value is not None:
            session["show_slider"] = True
        else:
            session.pop("show_slider", None)

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
        return render_template(f"{deck}.html", thumbnails=thumbnails, expose_value=expose_value, titles=titles, zip=zip)
        
    
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        deck = session.get("current_deck")
        return render_template(f"{deck}.html")

@app.route("/data")
def data():
    try:
        response = requests.get(f"{base_url}/composition/layers/1/clips/{1}")
        
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
    try:
        select = requests.post(f"{base_url}/composition/layers/1/clips/{clip_index}/select")
        connect = requests.post(f"{base_url}/composition/layers/1/clips/{clip_index}/connect")

        if select.status_code != 204 or connect.status_code != 204:
            flash(f'Error: {select.status_code}', 'error, could not select clip')
        else:
            current_deck = session.get("current_deck")
            return redirect(url_for(current_deck))
        
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
    
@app.route("/add_effect")
def add_effect():
    session["show_slider"] = True
    effect = "effect:///video/Exposure"
    try:
        response = requests.post(f"{base_url}/composition/clips/selected/effects/video/add", data=effect)

        if response.status_code != 204:
            flash(f'Error: {response.status_code}', 'error, could not add effect')
        else:
            current_deck = session.get("current_deck")
            return redirect(url_for(current_deck))
        
    except requests.RequestException as e:
        flash(f'Connection error: {str(e)}', 'error')
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
    
@app.route("/remove_effects")
def remove_effects():
    session.pop("show_slider", None)
    try:

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
    try:
        response = requests.post(f"{base_url}/composition/layers/1/clearclips")

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
    
if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=True,
        host="0.0.0.0",
        port=5000,
        threaded=True
        )
