from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from core.config import DRIVER_PATH
from core.download_by_song_id import download_song_by_id


def get_hot_songs_by_singer_id(singer_id):
    # # 无可视化界面(无头浏览器)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # selenium规避检测
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 设置代理ip
    # chrome_options.add_argument("--proxy-server=http://211.24.105.19:47615")

    bro = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
    bro.get("https://music.163.com/#/artist?id=%s" % singer_id)
    bro.switch_to.frame('g_iframe')
    # print(bro.page_source)
    # 获取热门歌曲
    sleep(1)
    lis = bro.find_elements_by_xpath('/html/body/div[3]/div[1]/div/div/div[3]/div[2]/div/div/div/div[1]/table//tr')
    songs = []
    for li in lis:
        ele = li.find_elements_by_css_selector('td.w1 > div > span.ply')[0]
        # 歌曲id
        song_id = ele.get_attribute('data-res-id')
        # 歌曲名
        song_name = li.find_element_by_css_selector('td:nth-child(2) > div > div > div > span > a > b').get_attribute(
            'title')
        song = {'id': song_id, 'name': song_name}
        songs.append(song)
        # print('热门歌曲:: %s --- %s' % (song['id'], song['name']))

    # 打乱list
    # songs.sort(key=lambda k: k['id'], reverse=False)
    for song in songs:
        # 每次爬取间隔时间
        sleep(2)
        print('---------------------------------------------------')
        print('正在下载:: %s' % (song['name']))
        flag = download_song_by_id(song['id'])
        print('下载完成!' if flag else '下载失败!!!')
