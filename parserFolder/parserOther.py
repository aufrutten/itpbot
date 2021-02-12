from .parser import Parser_Public


class StartPack(Parser_Public):

    def __init__(self):
        Parser_Public.__init__(self)
        self.posts = self.get_html_post(0, True)
        self.pack_dict = {}

        self.get_index_post()
        self.get_comment_post()
        self.get_owner_post()
        self.get_content_post()

    def get_index_post(self):
        count = 0
        for i in self.posts:
            count += 1
            index_post_re = i.a.get('name')
            index = str(index_post_re)[5:13] + str(index_post_re)[14:]
            self.pack_dict[str(count)] = {'index': index}

    def get_comment_post(self):
        count = 0
        for i in self.posts:
            count += 1
            try:
                text_r = i.findAll(class_='pi_text')
                text_r = str(text_r).replace('<br/>', '\n')
                text_r = text_r[21:]
                text_r = text_r[:len(text_r) - 6]

                self.pack_dict[str(count)]['comment'] = text_r

            except IndexError:
                self.pack_dict[str(i)]['comment'] = ' '

    def get_owner_post(self):
        count = 0
        for i in self.posts:
            count += 1
            try:
                owner = str(i.findAll(class_='user')[0].get_text())
                self.pack_dict[str(count)]['owner'] = owner

            except IndexError:
                self.pack_dict[str(count)]['owner'] = 'None'

    def get_content_post(self):
        count = 0
        for i in self.posts:
            count += 1
            try:

                content = i.findAll(class_='thumb_map_img thumb_map_img_as_div')[0]
                IMG = content.get('data-src_big')
                self.pack_dict[str(count)]['content'] = IMG

            except:
                return False