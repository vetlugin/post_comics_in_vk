import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()


def download_picture(pic_path, pic_name = None):
    '''
    Function download pictures from url to local directory.
    Create directory if it no exist.
    If

    Keywords arguments:
    pic_path -- url of picture fo download
    pic_name -- name of picture
    #pic_dir -- local directory for picture dowload
    '''
    #os.makedirs(pic_dir, exist_ok=True)
    if pic_name is None:
        pic_name = re.findall(r'\w+\.png', pic_path)[0]

    filename = os.path.join('.', pic_name)
    response = requests.get(pic_path)

    with open(filename, 'wb') as file:
        file.write(response.content)


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


def get_list_of_group():
    method_name = 'groups.get'
    token = os.getenv("TOKEN")
    client_id = os.getenv("client_id")
    vk_version = '5.95'
    parameters = f'user_id={client_id}'

    url_request = f'https://api.vk.com/method/{method_name}?{parameters}&access_token={token}&v={vk_version}'
    print(url_request)
    response = requests.get(url_request)
    print(response.json())


def main():

    comics_info = get_xkcd_comics_info()
    comics_url = comics_info['img']
    comics_alt = comics_info['alt']
    client_id = os.getenv("client_id")
    print(client_id)
    get_list_of_group()

    #download_picture(comics_url)


if __name__ == '__main__':
    main()
