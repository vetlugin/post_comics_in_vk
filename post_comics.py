import os
import requests


def download_picture(pic_path, pic_name, pic_dir):
    '''
    Function download pictures from url to local directory.
    Create directory if it no exist.

    Keywords arguments:
    pic_path -- url of picture fo download
    pic_name -- name of picture
    pic_dir -- local directory for picture dowload

    '''
    os.makedirs(pic_dir, exist_ok=True)

    filename = os.path.join(pic_dir, pic_name)
    response = requests.get(pic_path)

    with open(filename, 'wb') as file:
        file.write(response.content)

def main():

    


if __name__ == '__main__':
    main()
