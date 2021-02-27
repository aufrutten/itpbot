import logging
import requests
import os

from bs4 import BeautifulSoup as BS

from configuration import config
from controllerDB import DataBasePostsSQL


class DataBase_For_Parser:

    def __init__(self):
        logging.info('__init__DataBaseForParser')
        self.file_name = './DATABASE/index_post.txt'  # file_name DataBase
        self.result_about_exist_file = self.exist_filename()

    def exist_filename(self):
        """
        That function do one things
        she checks, exist file or no? which stores the index
        if True - return True
        elif False - Create that file, and return True
        else return False
        """
        if os.path.exists(self.file_name):  # if file exist - True
            return True
        elif not os.path.exists(self.file_name):  # elif file not exist - False
            with open(self.file_name, 'w') as f:
                f.write('0')
                f.close()
            return True

        else:
            return False

    def reader_file_from_filename(self):
        """
        That function read index from file and return up
        """
        try:
            with open(self.file_name, 'r') as f:
                index = f.read()
                f.close()
                return index
        except FileNotFoundError:
            self.exist_filename()

        except:
            pass
        finally:
            try:
                with open(self.file_name, 'r') as f:
                    index = f.read()
                    f.close()

                    return index
            except:
                print('Big pizda')

    def write_file_from_filename(self, index):
        with open(self.file_name, 'w') as f:
            f.write(str(index))
            f.close()


class Writer_HTML_In_File:

    @staticmethod
    def write_current_contentHTML(html):
        if not os.path.exists('./HTML'):
            os.mkdir('./HTML')
        try:
            with open('./HTML/current_html.html', 'w') as f:
                f.write(str(html.prettify()))
                f.close()
        except:
            return False

        return True


class Parser_Public(Writer_HTML_In_File):

    def __init__(self):
        logging.info('__init__ParserPublic')
        self.url = config.url
        self.update_html()

    def update_html(self):

        api = requests.get(self.url, config.headers)
        html = BS(api.content, 'html.parser')
        self.html = html

        self.write_current_contentHTML(html)

    def get_html_post(self, number=0, returnAll=False):

        public_wall = self.html.findAll(class_='wall_item')

        if not returnAll:
            return public_wall[number]

        elif returnAll:
            return public_wall


class Common_Metod(Parser_Public):

    def __init__(self):
        Parser_Public.__init__(self)
        self.dictionary = {'index': self.get_index_post(),
                           'owner': self.get_owner_post(),
                           'comment': self.get_comment_post(),
                           'content': self.get_content_post()}

    def get_index_post(self):
        post = self.get_html_post()
        index_post_re = post.a.get('name')
        index = str(index_post_re)[5:13] + str(index_post_re)[14:]
        return index

    def get_comment_post(self):
        post = self.get_html_post()
        try:
            text_r = post.findAll(class_='pi_text')[0]
            a_text = text_r.get_text()

            text_r = str(text_r).replace('<br/>', '\n')
            text_r = text_r[21:]
            text_r = text_r[:len(text_r) - 6]
            return a_text

        except IndexError:
            return ' '

    def get_owner_post(self):
        post = self.get_html_post()
        try:
            owner = str(post.findAll(class_='user')[0].get_text())
            return owner

        except:
            return 'Неизвестно'

    def get_content_post(self):
        post = self.get_html_post()
        try:

            content = post.findAll(class_='thumb_map_img thumb_map_img_as_div')[0]
            IMG = content.get('data-src_big')
            return str(IMG)

        except:
            return ' '


class MainParser(DataBase_For_Parser, Common_Metod):

    def __init__(self):
        logging.info('__init__MainParser')
        DataBase_For_Parser.__init__(self)
        Common_Metod.__init__(self)
        self.black_list = DataBasePostsSQL.SQLBlackList('DATABASE/blackList.sqlite')

    def comparison_index_in_file(self):
        index_in_file = self.reader_file_from_filename()
        self.update_html()
        index_in_current_post = self.get_index_post()

        flag = True
        content = self.get_content_post()

        for x in self.black_list.get_all():
            if x == content:
                flag = False

        if flag:
            if index_in_current_post == index_in_file:
                return False

            elif index_in_current_post != index_in_file:
                self.write_file_from_filename(index_in_current_post)
                self.dictionary = {'index': self.get_index_post(),
                                   'owner': self.get_owner_post(),
                                   'comment': self.get_comment_post(),
                                   'content': self.get_content_post()}
                return True


if __name__ == '__main__':
    pass