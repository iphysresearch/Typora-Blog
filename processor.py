import os
import time
import datetime
from bs4 import BeautifulSoup

def str2timestamp(timeStr):
    try:
        if ':' in timeStr:
            if '/' in timeStr:
                return time.mktime(datetime.datetime.strptime(timeStr, '%Y/%m/%d %H:%M:%S').timetuple())
            else:
                return time.mktime(datetime.datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S').timetuple())
        elif '/' in timeStr:
            return time.mktime(datetime.datetime.strptime(timeStr, '%Y/%m/%d %H-%M-%S').timetuple())
        else:
            return time.mktime(datetime.datetime.strptime(timeStr, '%Y-%m-%d %H-%M-%S').timetuple())
    except:
        return 0

def process():
    posts = []
    newPosts = os.listdir('posts')
    for templateFileName in os.listdir('app/templates/posts'):
        if templateFileName not in newPosts:
            os.remove(os.path.join(os.getcwd(), 'app/templates/posts', templateFileName))
    for postFileName in newPosts:
        if '.html' in postFileName:
            post = {}
            post['title'] = postFileName.strip('.html')
            with open('posts/%s' % postFileName, 'r') as sourceFile:
                text = sourceFile.read()
            soup = BeautifulSoup(text, 'lxml')
            post['timestamp'] = str2timestamp(soup.find('p').get_text())
            soup.find('p').decompose()
            postLink = ' ...<a href="/p/%s"> 阅读全文</a>' % post['title']
            try:
                post['abstract'] = str(soup.find('div', attrs={'class':'a'})).replace('</p></div>', postLink + '</p></div>')
            except:
                post['abstract'] = str(soup.find('div', attrs={'class':'a'})).replace('</div>', postLink + '</div>')
            if post['abstract'] == str(None):
                post['abstract'] = str(soup.find('p')).replace('</p>', postLink + '</p>')
            try:
                template = '{% extends "../base.html" %}{% block description %}' + post['title'] + '{% end %}{% block title %}' + post['title'] + '{% end %}{% block section %}<div class="postBlock">' + str(soup.find('body')).replace('</h2>', '</h2><div class="time"><input type="hidden" value="{{ timestamp }}"/></div>') + '<div class="ds-thread" data-thread-key="' + post['title'] + '" data-title="' + post['title'] + '" data-url="https://www.jackeriss.com/' + post['title'] + '"></div></div>{% end %}'
            except:
                pass
            with open('app/templates/posts/%s.html' % post['title'], 'w') as templateFile:
                templateFile.write(template)
            posts.append(post)
    posts.sort(key=lambda x: x['timestamp'], reverse=True)
    return posts

if __name__ == '__main__':
    posts = process()
    for post in posts:
        print(post['url'])
