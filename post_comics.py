import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()


def download_picture(img_url, img_dir = '.', img_name = None):
    '''
    Function download pictures from url to local directory.
    Create directory if it no exist.

    Keywords arguments:
    img_url -- url of picture fo download
    img_name -- name of picture
    img_dir -- local directory for picture dowload

    Return img_local_full_path
    '''
    #os.makedirs(img_dir, exist_ok=True)
    img_name = os.path.basename(img_url)

    img_local_full_path = os.path.join(img_dir, img_name)
    response = requests.get(img_url)

    with open(img_local_full_path, 'wb') as file:
        file.write(response.content)
    return img_local_full_path


def get_xkcd_comics_info(issue_id = None):
    '''
    Function get url of issue of xkcd comics.
    If issue_id is not None than function return url of issue_id comics.
    If issue_id is None than function return url of last comics.

    Keywords arguments:
    issue_id -- id of issue xkcd comics
    '''

    if issue_id is not None:
        api_path = 'https://xkcd.com/{}/info.0.json'.format(issue_id)
    else:
        api_path = 'https://xkcd.com/info.0.json'

    response = requests.get(api_path).json()
    return response


def get_address_upload_photos():
    '''
    Get address to upload photos
    '''
    method_name = 'photos.getWallUploadServer'
    token = os.getenv("TOKEN")
    vk_version = '5.95'
    group_id='181623583'
    parameters = f'group_id={group_id}'

    url_request = f'https://api.vk.com/method/{method_name}?{parameters}&access_token={token}&v={vk_version}'
    response = requests.get(url_request)
    return response.json()['response']['upload_url']


def upload_photo_to_server(url, img_path):

    img_name = os.path.basename(img_path)

    image_file_descriptor = open(img_name, 'rb')
    files = {'file': image_file_descriptor}
    response = requests.post(url, files=files)
    image_file_descriptor.close()

    return response.json()


def save_wall_photo(photo_on_server, caption):
    '''
    __
    '''
    method_name = 'photos.saveWallPhoto'
    token = os.getenv("TOKEN")
    vk_version = '5.95'
    group_id='181623583'
    hash = photo_on_server['hash']
    server = photo_on_server['server']
    photo = photo_on_server['photo']
    parameters = f'group_id={group_id}&photo={photo}&hash={hash}&server={server}&caption={caption}'

    url_request = f'https://api.vk.com/method/{method_name}?{parameters}&access_token={token}&v={vk_version}'
    print(url_request)
    response = requests.get(url_request)
    return response.json()


def main():
    print('*********')
    comics_info = get_xkcd_comics_info()
    comics_url = comics_info['img']
    comics_alt = comics_info['alt']
    user_id = os.getenv("user_id")

    download_picture(comics_url)
    photos_upload_url = get_address_upload_photos()
    photo_on_server = upload_photo_to_server(photos_upload_url, comics_url)
    print(save_wall_photo(photo_on_server, comics_alt))

if __name__ == '__main__':
    main()
