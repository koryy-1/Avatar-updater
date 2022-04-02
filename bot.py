import os
import time
import schedule
import random
import requests
# import config
from keep_alive import keep_alive

import vk_api

# from vk_api.utils import get_random_id
# from urllib import urlretrieve

# keep_alive()

def update_ava():
    global prev_img
    vk_session = vk_api.VkApi(os.environ['login'], os.environ['password'])
    vk_session.auth(token_only=True)

    vk = vk_session.get_api()

    images = os.listdir("images")

    next_img = random.randint(0, len(images)-1)
    while(next_img == prev_img):
        next_img = random.randint(0, len(images)-1)
    prev_img = next_img

    url = vk.photos.getOwnerPhotoUploadServer()['upload_url']

    request = requests.post(url, files={'photo': open('images/'+images[next_img], 'rb')}).json()
    photo = request['photo']
    server = request['server']
    hash = request['hash']

    vk.photos.saveOwnerPhoto(server = server, hash = hash, photo = photo)

    posts = vk.wall.get()
    post_id = posts["items"][0]["id"]
    vk.wall.delete(post_id = post_id)
    
    photos = vk.photos.getAll()
    if (photos['count']>1):
        photo_id = photos["items"][1]["id"]
        vk.photos.delete(photo_id = photo_id)
    

prev_img = 0
def run():
    print('bot is running')
    schedule.every().day.at("23:00").do(update_ava) # schedule time for update ava
    try:
        while(True):
            schedule.run_pending()
            time.sleep(60*20)
            print('прошло 20 минут')
            
    except vk_api.AuthError as error_msg:
        print(error_msg)
        with open('logs.txt', 'a', encoding='utf-8') as file:
            file.write(error_msg)