import requests
from time import sleep
import base64


def select_deck(deck_index, base_url):
    select = requests.post(f"{base_url}/composition/decks/{deck_index}/select")
    sleep(0.25)
    update = requests.put(
        f"{base_url}/composition/layers/1",
        json={"video": {"opacity": {"value": 1.0}}}
    )
    update2 = requests.put(
            f"{base_url}/composition", json={"master": {"value": 1.0}}
    )

    thumbnails = []
    clip_index = 1
    while True:
        thumbnail = requests.get(f"{base_url}/composition/layers/1/clips/{clip_index}/thumbnail")
        decoded_thumbnail = base64.b64encode(thumbnail.content).decode("utf-8")
        
        if len(decoded_thumbnail) > 528:
            thumbnails.append(decoded_thumbnail)
            clip_index += 1
        else:
            break

    return select, update, update2, thumbnails
