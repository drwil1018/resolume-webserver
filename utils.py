import requests
from time import sleep
import base64


def select_deck(deck_index, base_url):
    select = requests.post(f"{base_url}/composition/decks/{deck_index}/select")
    sleep(0.3)
    update = requests.put(
        f"{base_url}/composition/layers/1",
        json={"video": {"opacity": {"value": 1.0}}}
    )
    update2 = requests.put(
            f"{base_url}/composition", json={"master": {"value": 1.0}}
    )

    thumbnails = []
    titles = []
    clip_index = 1
    while True:
        thumbnail = requests.get(f"{base_url}/composition/layers/1/clips/{clip_index}/thumbnail")
        decoded_thumbnail = base64.b64encode(thumbnail.content).decode("utf-8")
        clip_data = requests.get(f"{base_url}/composition/layers/1/clips/{clip_index}")
        title = clip_data.json().get('name', {}).get('value')
        
        if len(decoded_thumbnail) > 528:
            thumbnails.append(decoded_thumbnail)
            titles.append(title)
            clip_index += 1
        else:
            break
    
    total_clips = len(thumbnails)
    return select, update, update2, thumbnails, total_clips, titles


def check_effects(base_url):
        response = requests.get(f"{base_url}/composition/clips/selected")
        if response.status_code == 200:
            data = response.json()
            effects = data.get('video', {}).get('effects', [])
            
            if len(effects) > 1:
                if effects[1].get('name') == 'Exposure':
                    expose_value = round(effects[1].get('params', {}).get('Exposure', {}).get('value'), 2)
                    return expose_value
                    