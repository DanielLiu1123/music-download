import os
import uuid

import requests


def download_song_by_id(song_id):
    song_id = 'https://music.163.com/#/song?id=%s' % song_id
    source_url = 'http://www.eggvod.cn/music/'
    param = {
        'input': song_id,
        'filter': 'url',
        'type': '_',
        'page': 1
    }
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-US;q=0.8,zh;q=0.7',
        'Content-Length': '83',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'Hm_lvt_a2f7245c0b3fcd993003b1d9182d0a82=1604900775,1604900798',
        'Host': 'www.eggvod.cn',
        'Origin': 'http://www.eggvod.cn',
        'Referer': 'http://www.eggvod.cn/music/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 '
                      'Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36'
    }
    proxies = [
        {'http': 'http://171.35.161.219:9999'},
        {'http': 'http://123.163.115.165:9999'},
        {'http': 'http://171.15.152.9:9999'},
        {'http': 'http://115.221.246.100:9999'},
        {'http': 'http://118.27.28.45:3128'},
    ]

    print('正在请求获取下载链接...')
    response = requests.post(source_url, data=param, headers=header)
    # response = requests.post(source_url, data=param, headers=header, proxies=random.choice(proxies))
    # print(response)

    if not response:
        print(response)
        return False
    res_json = response.json()
    # print(res_json)
    if not res_json['data']:
        print(res_json)
        return False

    song_info = {}
    song_url = res_json['data'][0]['url']
    title = res_json['data'][0]['title']
    author = res_json['data'][0]['author']
    pic = res_json['data'][0]['pic']
    lyrics = res_json['data'][0]['lrc']
    song_info['url'] = song_url
    song_info['title'] = title
    song_info['author'] = author
    song_info['pic'] = pic
    song_info['lyrics'] = lyrics

    # 下载歌曲
    if song_info['url']:
        song = requests.get(song_info['url']).content
        # 保存歌曲
        songs_dir = './songs'
        if not os.path.exists(songs_dir):
            os.mkdir(songs_dir)

        # loc = song_dir + '/' + title + '-' + author + '.mp3'
        loc = '%s/%s-%s.mp3' % (songs_dir, song_info['title'], song_info['author'])
        lyrics_loc = '%s/%s-%s-歌词.txt' % (songs_dir, song_info['title'], song_info['author'])

        random_song_name = uuid.uuid4()
        # 保存歌曲
        try:
            with open(loc, 'wb') as fp:
                fp.write(song)
            print('歌曲保存成功! 位置%s' % loc)
        except Exception as e:
            print(
                '%s-%s.mp3歌名不合法,将歌曲名变为%s-%s.mp3储存' % (song_info['title'], song_info['author'], random_song_name,
                                                      song_info['author']))
            loc = '%s/%s-%s.mp3' % (songs_dir, random_song_name, song_info['author'])
            with open(loc, 'wb') as fp:
                fp.write(song)
            print('歌曲保存成功! 位置%s' % loc)

        # 保存歌词
        try:
            with open(lyrics_loc, 'w+', encoding='utf-8') as fp:
                fp.write(song_info['lyrics'])
            print('歌词保存成功! 位置%s' % lyrics_loc)
        except Exception as e:
            print(
                '%s-%s-歌词.txt不合法,将文件名变为%s-%s-歌词.txt储存' % (song_info['title'], song_info['author'], random_song_name,
                                                          song_info['author']))
            lyrics_loc = '%s/%s-%s-歌词.txt' % (songs_dir, random_song_name, song_info['author'])
            with open(lyrics_loc, 'w+') as fp:
                fp.write(song_info['lyrics'])
            print('歌词保存成功! 位置%s' % lyrics_loc)

        return True
    else:
        print('获取下载链接失败! 换首歌吧~')
        return False

    # print('程序结束...')
