import logging
from datetime import datetime
from os.path import exists
from os import mkdir

TOKEN = "1592564986:AAHP0hRepfPQ0BxaqklnERaLXgAaX0Fb0cU"
url = 'https://vk.com/itpedia_youtube'
headers = {'user-agent': """Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko)
 Chrome/88.0.4324.96 Safari/537.36""",
           'accept-language': 'ru-RU'}

admins = {
    'FBICIAIIA': 575704682,
    'Chivotebe': 572317802,
}

logging_path = './LogHistory/'


def directory():
    if not exists(logging_path):
        mkdir(logging_path)

    return logging_path


directory()


def gen_name():
    t = str(datetime.today())
    t = t.replace(' ', '-')
    t = t.replace(':', '-')
    t = t.replace('.', '-')
    path = '/LogHistory/'
    lib_name = './' + path.split('/')[1] + '/'
    pattern = '{}{}-{}.log'
    return pattern.format(lib_name, t, 'INFO')


config_logger = {
    'level': logging.INFO,
    'filemode': 'w',
    'filename': gen_name(),
    'format': '[%(asctime)s] %(filename)24s %(levelname)16s:  %(message)-70s'
}