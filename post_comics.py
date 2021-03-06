import os
import requests
import random
from dotenv import load_dotenv

#тут load_dotenv работает
load_dotenv()

TOKEN=os.getenv("TOKEN")
GROUP_ID=os.getenv("GROUP_ID")
VK_VERSION='5.95'


def get_xkcd_comics_info(issue_id = None):
    '''Function get url of issue of xkcd comics.
    If issue_id is not None than function return url of issue_id comics.
    If issue_id is None than function return url of last comics.

    Keywords arguments:
    issue_id -- id of issue xkcd comics'''
    if issue_id is not None:
        url_path = f'https://xkcd.com/{issue_id}/info.0.json'
    else:
        url_path = 'https://xkcd.com/info.0.json'

    response = requests.get(url_path)
    if response.ok:
        return response.json()
    else:
        return


def download_picture(img_url, img_dir = '.'):
    '''Function download pictures from url to local directory.
    Create directory if it no exist.

    Keywords arguments:
    img_url -- url of picture fo download
    img_name -- name of picture
    img_dir -- local directory for picture dowload

    Return img_local_full_path'''
    #os.makedirs(img_dir, exist_ok=True)
    img_name = os.path.basename(img_url)

    img_local_full_path = os.path.join(img_dir, img_name)

    try:
        response = requests.get(img_url)
        with open(img_local_full_path, 'wb') as file:
            file.write(response.content)
        return img_local_full_path

    except OSError as e:  ## if failed, report it back to the user ##
        print (f'Error: {e.filename} - {e.strerror}.')


def get_random_xkcd_comics():
    #Get information about last issue comics
    last_comics_num = get_xkcd_comics_info()['num']
    comics_info = get_xkcd_comics_info(random.randrange(1,last_comics_num))
    comics_url = comics_info['img']
    comics_alt = comics_info['alt']

    # Download image to file with img_local_full_path address
    img_local_full_path = download_picture(comics_url)
    return {'title': comics_alt, 'path': img_local_full_path}


def get_address_upload_photos():
    '''Get address to upload photos'''
    method_name = 'photos.getWallUploadServer'
    payload = {
        'group_id': GROUP_ID,
        'access_token': TOKEN,
        'v': VK_VERSION,
    }
    url = f'https://api.vk.com/method/{method_name}'
    response = requests.get(url, params=payload)
    if not response.ok:
        return
    if response.json().get('error'):
        error_msg = response.json()['error']['error_msg']
        raise requests.HTTPError(f'The get_address_upload_photos function raised the error: {error_msg}')
    else:
        return response.json()['response']['upload_url']


def upload_photo_to_server(url, img_path):
    '''Upload photo to server.'''
    open_file = open(img_path, 'rb')
    files = {'file': open_file}

    response = requests.post(url, files=files)
    if not response.ok:
        return
    if response.json().get('error'):
        error_msg = response.json()['error']['error_msg']
        raise requests.HTTPError(f'The upload_photo_to_server function raised the error: {error_msg}')
    else:
        return response.json()


def save_wall_photo(photo_on_server):
    '''Save photo on server to prepare for post.'''
    method_name = 'photos.saveWallPhoto'
    payload = {
        'group_id': GROUP_ID,
        'photo': photo_on_server['photo'],
        'hash': photo_on_server['hash'],
        'server': photo_on_server['server'],
        'access_token': TOKEN,
        'v': VK_VERSION,
        }
    url = f'https://api.vk.com/method/{method_name}'
    response = requests.get(url, params=payload)
    if not response.ok:
        return
    if response.json().get('error'):
        error_msg = response.json()['error']['error_msg']
        raise requests.HTTPError(f'The save_wall_photo function raised the error: {error_msg}')
    else:
        return response.json()


def post_wall_photo(owner_id, media_id, message):
    '''Post picture with title on the wall vk community.'''
    method_name = 'wall.post'
    payload = {
        'group_id': GROUP_ID,
        'owner_id':f'-{GROUP_ID}',
        'attachments':f'photo{owner_id}_{media_id}',
        'message': message,
        'access_token': TOKEN,
        'v': VK_VERSION,
        }
    url = f'https://api.vk.com/method/{method_name}'
    response = requests.get(url, params=payload)
    if not response.ok:
        return
    if response.json().get('error'):
        error_msg = response.json()['error']['error_msg']
        raise requests.HTTPError(f'The post_wall_photo function raised the error: {error_msg}')
    else:
        return response.json()


def upload_and_post_wall_vk(img_local_full_path,comics_title):
    # Get url on server to upload picture
    img_upload_url = get_address_upload_photos()

    # Upload picture to img_upload_url from img_local_full_path
    photo_on_server = upload_photo_to_server(img_upload_url, img_local_full_path)

    #Post uploaded pictures on the wall of the group
    save_wall_response = save_wall_photo(photo_on_server)
    media_id = save_wall_response['response'][0]['id']
    owner_id = save_wall_response['response'][0]['owner_id']
    post_wall_photo(owner_id, media_id, comics_title)


def delete_local_file(path):
    try:
        os.remove(path)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))


def main():
    try:
        random_comics_info = get_random_xkcd_comics()

        img_local_full_path = random_comics_info['path']
        comics_title = random_comics_info['title']
        upload_and_post_wall_vk(img_local_full_path,comics_title)

        delete_local_file(img_local_full_path)
    except Exception as error:
        print(error)
        return

if __name__ == '__main__':
    #тут load_dotenv не работает
    #load_dotenv()
    main()
