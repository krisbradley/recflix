import os
from PIL import Image
from PIL import ImageOps

from SlimInstagramAPI import InstagramAPI
from botocore.vendored import requests

def lambda_handler(event, context):
    response = requests.get('https://api.reelgood.com/roulette/netflix?availability=onAnySource&content_kind=movie&minimum_imdb=7&minimum_rt=60')
    responseJson = response.json()
    movieImageUrl = 'https://img.reelgood.com/content/movie/' + responseJson['id'] + '/poster-780.jpg'
    print(movieImageUrl)
    filename = '/tmp/image.jpg'

    img_data = requests.get(movieImageUrl).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)

    im = Image.open(filename)

    # THIS CENTER-CROPPED THE IMAGE, LOOKED TERRIBLE
    # ---------
    # width, height = im.size
    # left = (width - 640) / 2
    # top = (height - 762) / 2
    # right = (width + 640) / 2
    # bottom = (height + 762) / 2
    # cropped_image = im.crop((left, top, right, bottom))
    # cropped_image.save(filename)

    # THIS RE-SIZED THE IMAGE, LOOKED FAT
    # ---------
    # resized_image = im.resize((640,762), Image.ANTIALIAS)

    # THIS DYNAMICALLY RE-SIZED THEN CROPPED THE IMAGE, LOOKED GREAT
    # ---------
    resized_image = ImageOps.fit(im, (640,762), Image.ANTIALIAS)
    resized_image.save(filename)

    # DONT SAVE FILES THIS WAY, DO IT LIKE ABOVE, WAY EASIER
    # ---------
    # with open(filename, 'wb') as handler:
    #     for chunk in cropped_image.chunks():
    #         handler.write(chunk)

    Instagram = InstagramAPI(os.environ['RECFLIX_USER'], os.environ['RECFLIX_PASSWORD'])
    Instagram.login()
    caption = responseJson['title'] + '\n' + responseJson['overview']
    Instagram.uploadPhoto(filename, caption=caption)

lambda_handler('','')