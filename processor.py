import os
import time
import datetime

from snownlp import SnowNLP
from bs4 import BeautifulSoup
from tornado.options import options

def str2timestamp(time_str):
    try:
        if ':' in time_str:
            if '/' in time_str:
                return time.mktime(datetime.datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S').timetuple())
            else:
                return time.mktime(datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').timetuple())
        elif '/' in time_str:
            return time.mktime(datetime.datetime.strptime(time_str, '%Y/%m/%d %H-%M-%S').timetuple())
        else:
            return time.mktime(datetime.datetime.strptime(time_str, '%Y-%m-%d %H-%M-%S').timetuple())
    except Exception as err:
        options.config['root_logger'].error(err, exc_info=True)
        return 0

def process():
    posts = []
    new_posts = os.listdir('posts')
    for template_file_name in os.listdir('app/templates/posts'):
        if template_file_name not in new_posts:
            os.remove(os.path.join(options.config['root_path'], 'app/templates/posts', template_file_name))
    for post_file_name in new_posts:
        if '.html' in post_file_name:
            post = {}
            post['title'] = post_file_name.replace('.html', '')
            title = SnowNLP(post['title'])
            post['id'] = '_'.join(title.pinyin)
            with open('posts/%s' % post_file_name, 'r') as source_file:
                text = source_file.read()
            soup = BeautifulSoup(text, 'lxml')
            post['timestamp'] = str2timestamp(soup.find('p').get_text())
            soup.find('p').decompose()
            post_link = ' ...<a href="/p/%s"> 阅读全文</a>' % post['id']
            try:
                post['abstract'] = str(soup.find('div', attrs={'class':'a'})).\
                replace('</p></div>', post_link + '</p></div>')
            except Exception as err:
                options.config['root_logger'].error(err, exc_info=True)
                post['abstract'] = str(soup.find('div', attrs={'class':'a'})).\
                replace('</div>', post_link + '</div>')
            if post['abstract'] == str(None):
                post['abstract'] = str(soup.find('p')).replace('</p>', post_link + '</p>')
            try:
                template = '{% extends "../base.html" %}{% block description %}' \
                + post['title'] + '{% end %}{% block title %}' + post['title'] + \
                '{% end %}{% block section %}<div class="postBlock">' + \
                str(soup.find('body')).replace('</h2>', '</h2><div class="time">\
                                               <input type="hidden" value="{{ \
                                               timestamp }}"/></div>') + \
                ('<div id="comments"></div>'
                 '<script type="text/javascript">'
                 'const gitment = new Gitment({'
                 'id: "' + post['id'] + '",'
                 'owner: "Jackeriss",'
                 'repo: "comments_of_www.jackeriss.com",'
                 'oauth: {'
                 '  client_id: "748b4dac7ace16b6d7cb",'
                 '  client_secret: "c5db352dad6f88b898840d628e44cfb5b4eaf4c0",'
                 '},'
                 '});'
                 'gitment.render("comments")'
                 '</script>'
                 '{% end %}')
            except Exception as err:
                options.config['root_logger'].error(err, exc_info=True)
            with open('app/templates/posts/%s.html' % post['title'], 'w') as template_file:
                template_file.write(template)
            posts.append(post)
    posts.sort(key=lambda x: x['timestamp'], reverse=True)
    return posts

if __name__ == '__main__':
    POSTS = process()
    for p in POSTS:
        print(p['url'])
