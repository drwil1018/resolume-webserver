from flask import session, flash, redirect, url_for
import requests
import base64
from time import sleep


def select_deck(layer_index, base_url):
    update = requests.put(
        f"{base_url}/composition/layers/{layer_index}",
        json={"video": {"opacity": {"value": 1.0}}}
    )
    update2 = requests.put(
            f"{base_url}/composition", json={"master": {"value": 1.0}}
    )

    thumbnails = []
    titles = []
    clip_index = 1
    selection_index = None
    while True:
        thumbnail = requests.get(f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}/thumbnail")
        decoded_thumbnail = base64.b64encode(thumbnail.content).decode("utf-8")
        clip_data = requests.get(f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}")
        title = clip_data.json().get('name', {}).get('value')
        selecition = clip_data.json().get('selected', {}).get('value')
        if selecition == True:
            selection_index = clip_index
        
        if len(decoded_thumbnail) > 528:
            thumbnails.append(decoded_thumbnail)
            titles.append(title)
            clip_index += 1
        else:
            break
    
    total_clips = len(thumbnails)
    return update, update2, thumbnails, total_clips, titles, selection_index


def check_effects(base_url):
        response = requests.get(f"{base_url}/composition/clips/selected")
        if response.status_code == 200:
            try:
                data = response.json()
                effects = data.get('video', {}).get('effects', [])
                
                if len(effects) > 2:
                    session["effects"] = True
                    scale_value = round(effects[0].get('params', {}).get('Scale', {}).get('value'))
                    shiftx_value = round(effects[0].get('params', {}).get('Position X', {}).get('value'))
                    shifty_value = round(effects[0].get('params', {}).get('Position Y', {}).get('value'))
                    expose_value = round(effects[1].get('params', {}).get('Exposure', {}).get('value'), 2)
                    hue_value = round(effects[2].get('params', {}).get('Hue Rotate', {}).get('value'), 2)
                    sat_value = round(effects[2].get('params', {}).get('Sat. Scale', {}).get('value'), 2)
                    return expose_value, hue_value, scale_value, shiftx_value, shifty_value, sat_value
                    
                else:
                    session["effects"] = False
                    expose_value = None
                    hue_value = None
                    scale_value = None
                    shiftx_value = None
                    shifty_value = None
                    sat_value = None
                    return expose_value, hue_value, scale_value, shiftx_value, shifty_value, sat_value
            
            except Exception as e:
                print(e)
                
def store_effects_index(base_url, layer_index, clip_index):
    response = requests.get(f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}")
    data = response.json()

    if data is not None:
        effects = data.get('video', {}).get('effects', [])

        try:
            if len(effects) >= 3:
                scale_value = round(effects[0].get('params', {}).get('Scale', {}).get('value'))
                shiftx_value = round(effects[0].get('params', {}).get('Position X', {}).get('value'))
                shifty_value = round(effects[0].get('params', {}).get('Position Y', {}).get('value'))
                expose_value = round(effects[1].get('params', {}).get('Exposure', {}).get('value'), 2)
                hue_value = round(effects[2].get('params', {}).get('Hue Rotate', {}).get('value'), 2)
                sat_value = round(effects[2].get('params', {}).get('Sat. Scale', {}).get('value'), 2)
                effect_values = [expose_value, hue_value, scale_value, shiftx_value, shifty_value, sat_value]
                return effect_values
            
            else:
                return None
        
        except Exception as e:
            flash("Error storing effects")
            current_deck = session.get("current_deck")
            return redirect(url_for(current_deck))

def store_effects(base_url):
    response = requests.get(f"{base_url}/composition/clips/selected")
    data = response.json()

    if data is not None:
        try:
            effects = data.get('video', {}).get('effects', [])

        except AttributeError:
            return None

    try:
        if len(effects) >= 3:
            scale_value = round(effects[0].get('params', {}).get('Scale', {}).get('value'))
            shiftx_value = round(effects[0].get('params', {}).get('Position X', {}).get('value'))
            shifty_value = round(effects[0].get('params', {}).get('Position Y', {}).get('value'))
            expose_value = round(effects[1].get('params', {}).get('Exposure', {}).get('value'), 2)
            hue_value = round(effects[2].get('params', {}).get('Hue Rotate', {}).get('value'), 2)
            sat_value = round(effects[2].get('params', {}).get('Sat. Scale', {}).get('value'), 2)
            effect_values = [expose_value, hue_value, scale_value, shiftx_value, shifty_value, sat_value]
            return effect_values
        
        else:
            return None
    
    except Exception as e:
        flash("Error storing effects")
        current_deck = session.get("current_deck")
        return redirect(url_for(current_deck))
    
def apply_effects(base_url, layer_index, clip_index, expose_value, hue_value, scale_value, shiftx_value, shifty_value, sat_value):
    update_exposure = requests.put(
            f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}",
            json={
                "video": {
                    "effects": [
                        {},
                            {
                                "params": {
                                    "Exposure": {
                                        "value": expose_value
                                    }
                                }
                            }
                    ]
                }
            }
        )
    
    update_hue = requests.put(
            f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}",
            json={
                "video": {
                    "effects": [
                        {}, {},
                            {
                                "params": {
                                    "Hue Rotate": {
                                        "value": hue_value
                                    }
                                }
                            }
                    ]
                }
            }
        )
    
    update_scale = requests.put(
            f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}",
            json={
                "video": {
                    "effects": [
                            {
                                "params": {
                                    "Scale": {
                                        "value": scale_value
                                    }
                                }
                            }
                    ]
                }
            }
        )
    
    update_shiftx = requests.put(
            f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}",
            json={
                "video": {
                    "effects": [
                            {
                                "params": {
                                    "Position X": {
                                        "value": shiftx_value
                                    }
                                }
                            }
                    ]
                }
            }
        )
    
    update_shifty = requests.put(
            f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}",
            json={
                "video": {
                    "effects": [
                            {
                                "params": {
                                    "Position Y": {
                                        "value": shifty_value
                                    }
                                }
                            }
                    ]
                }
            }
        )
    
    update_sat = requests.put(
            f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}",
            json={
                "video": {
                    "effects": [
                        {}, {},
                            {
                                "params": {
                                    "Sat. Scale": {
                                        "value": sat_value
                                    }
                                }
                            }
                    ]
                }
            }
        )
    
    return update_exposure, update_hue, update_scale, update_shiftx, update_shifty, update_sat