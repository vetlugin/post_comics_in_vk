import os
import requests
import random
from dotenv import load_dotenv


load_dotenv()


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


def download_picture(img_url, img_dir = '.'):
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
    '''
    Upload photo to server.
    '''
    open_file = open(img_path, 'rb')
    files = {'file': open_file}

    response = requests.post(url, files=files)
    open_file.close()

    return response.json()


def save_wall_photo(photo_on_server):
    '''
    Save photo on server to prepare for post.
    '''
    method_name = 'photos.saveWallPhoto'
    token = os.getenv("TOKEN")
    vk_version = '5.95'
    group_id='181623583'
    photo = photo_on_server['photo']
    hash = photo_on_server['hash']
    server = photo_on_server['server']
    parameters = f'group_id={group_id}&photo={photo}&hash={hash}&server={server}'

    url_request = f'https://api.vk.com/method/{method_name}?{parameters}&access_token={token}&v={vk_version}'
    response = requests.post(url_request)
    return response.json()


def post_wall_photo(owner_id, media_id, message):
    '''
    Post picture with title on the wall vk community.
    '''
    method_name = 'wall.post'
    token = os.getenv("TOKEN")
    vk_version = '5.95'
    group_id='181623583'

    attachments = f"photo{owner_id}_{media_id}"

    parameters = f'group_id={group_id}&owner_id=-{group_id}&attachments={attachments}&message={message}'
    url_request = f'https://api.vk.com/method/{method_name}?{parameters}&access_token={token}&v={vk_version}'
    response = requests.post(url_request)
    return response.json()


def main():
    #Get information about last issue comics
    last_comics_num = get_xkcd_comics_info()['num']
    comics_info = get_xkcd_comics_info(random.randrange(1,last_comics_num))
    comics_url = comics_info['img']
    comics_alt = comics_info['alt']

    # Download image to file with img_local_full_path address
    img_local_full_path = download_picture(comics_url)

    # Get url on server to upload picture
    img_upload_url = get_address_upload_photos()

    # Upload picture to img_upload_url from img_local_full_path
    photo_on_server = upload_photo_to_server(img_upload_url, img_local_full_path)

    #Post uploaded pictures on the wall of the group
    save_wall_response = save_wall_photo(photo_on_server)

    media_id = save_wall_response['response'][0]['id']
    owner_id = save_wall_response['response'][0]['owner_id']
    post_wall_photo(owner_id, media_id, comics_alt)

    try:
        os.remove(img_local_full_path)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == '__main__':
    main()
