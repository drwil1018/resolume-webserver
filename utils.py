from flask import session
import requests
import base64


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
    while True:
        thumbnail = requests.get(f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}/thumbnail")
        decoded_thumbnail = base64.b64encode(thumbnail.content).decode("utf-8")
        clip_data = requests.get(f"{base_url}/composition/layers/{layer_index}/clips/{clip_index}")
        title = clip_data.json().get('name', {}).get('value')
        
        if len(decoded_thumbnail) > 528:
            thumbnails.append(decoded_thumbnail)
            titles.append(title)
            clip_index += 1
        else:
            break
    
    total_clips = len(thumbnails)
    return update, update2, thumbnails, total_clips, titles


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
                    print(f"expose: {expose_value}, hue: {hue_value}, scale: {scale_value}, shiftx: {shiftx_value}, shifty: {shifty_value}, sat: {sat_value}")
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
                
                    