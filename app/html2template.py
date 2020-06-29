import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from tornado.options import options

def str2timestamp(time_str):
    try:
        if ':' in time_str:
            if '/' in time_str:
                return (time_str.split('/')[0],
                        time.mktime(datetime.datetime.strptime(time_str,
                                                               '%Y/%m/%d %H:%M:%S').timetuple()))
            return (time_str.split('-')[0],
                    time.mktime(datetime.datetime.strptime(time_str,
                                                           '%Y-%m-%d %H:%M:%S').timetuple()))
        elif '/' in time_str:
            return (time_str.split('/')[0],
                    time.mktime(datetime.datetime.strptime(time_str,
                                                           '%Y/%m/%d %H-%M-%S').timetuple()))
        else:
            return (time_str.split('-')[0],
                    time.mktime(datetime.datetime.strptime(time_str,
                                                           '%Y-%m-%d %H-%M-%S').timetuple()))
    except Exception as err:
        options.config['root_logger'].error(err, exc_info=True)
        return 0

def html2template():
    posts = []
    new_posts = os.listdir(os.path.join(options.config['root_path'], 'post_html'))
    for template_file_name in os.listdir(
            os.path.join(
                options.config['root_path'],
                'app/template/post'
            )
        ):
        if template_file_name not in new_posts:
            os.remove(
                os.path.join(
                    options.config['root_path'],
                    'app/template/post',
                    template_file_name
                )
            )
    for post_file_name in new_posts:
        if '.html' in post_file_name:
            post = {'title': post_file_name.replace('.html', '')}
            post['id'] = post['title'].replace(' ', '')
            with open(
                os.path.join(
                    options.config['root_path'],
                    'post_html/%s' % post_file_name
                ),
                'r'
            ) as source_file:
                text = source_file.read()
            soup = BeautifulSoup(text, 'lxml')
            post['year'], post['timestamp'] = str2timestamp(soup.find('p').get_text())
            soup.find('p').decompose()
            post_link = ' ...<a href="/p/%s"> 阅读全文</a>' % post['id']
            try:
                post['abstract'] = str(soup.find('div', attrs={'class': 'a'})).\
                replace('</p></div>', post_link + '</p></div>')
            except Exception as err:
                options.config['root_logger'].error(err, exc_info=True)
                post['abstract'] = str(soup.find('div', attrs={'class': 'a'})).\
                replace('</div>', post_link + '</div>')
            if post['abstract'] == str(None):
                post['abstract'] = str(soup.find('p')).replace('</p>', post_link + '</p>')
            try:
                template = (
                    '{% extends "../base.html" %}{% block description %}'
                    + post['title']
                    + '{% end %}{% block title %}' + post['title']
                    + ' - Jackeriss{% end %}{% block section %}<div class="postBlock">'
                    + str(soup.find('body')).replace(
                        '</h2>',
                        '</h2><div class="time"><input type="hidden" value="{{ timestamp }}"/></div>')
                    + '<div id="gitalk-container"></div></div>{% end %}')
            except Exception as err:
                options.config['root_logger'].error(err, exc_info=True)
            with open(os.path.join(options.config['root_path'],
                                   'app/template/post/%s.html' % post['title']),
                      'w') as template_file:
                template_file.write(template)
            posts.append(post)
    posts.sort(key=lambda x: x['timestamp'], reverse=True)
    with open('urls.txt', 'w') as urls:
        for post in posts:
            urls.write('https://www.jackeiss.com/p/' + post['id'] + '\n')
    options.config['root_logger'].info(
        requests.post(
            options.config['baidu_commit_url'],
            files={'file': open('urls.txt', 'r')}
        ).text
    )
    return posts

if __name__ == '__main__':
    POSTS = html2template()
    for p in POSTS:
        print(p['id'])
