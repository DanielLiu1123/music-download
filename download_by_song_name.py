from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from core.config import DRIVER_PATH
from core.download_by_song_id import download_song_by_id


def getSongsByKw(kw):
    # # 无可视化界面(无头浏览器)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # selenium规避检测
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 设置代理ip
    # chrome_options.add_argument("--proxy-server=http://211.24.105.19:47615")

    bro = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
    bro.get("https://music.163.com/#/search/m/?s=%s&type=1" % kw)
    bro.switch_to.frame('g_iframe')
    # print(bro.page_source)
    # 获取热门歌曲
    sleep(1)
    divs = bro.find_elements_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div/div/div')
    # 只提取根据关键字搜索出的前10首歌
    if len(divs) > 10:
        divs = divs[:10]

    # 列出10首歌
    songs = []
    for div in divs:
        # 歌曲id
        song_id = \
            div.find_element_by_css_selector('div.td.w0 > div > div > a:nth-child(1)').get_attribute('href').split('=')[
                1]
        # 歌曲名称
        song_name = div.find_element_by_css_selector('div.td.w0 > div > div > a:nth-child(1) > b').get_attribute(
            'title')
        # 歌手
        artists = div.find_element_by_css_selector('div.td.w1 > div').find_elements_by_tag_name('a')
        song_singer = ''
        for artist in artists:
            if artist.text:
                song_singer = '%s%s/' % (song_singer, artist.text)
        song_singer = song_singer[0:len(song_singer) - 1]
        # print(song_id + '----' + song_name + '----' + song_singer)
        song = {'id': song_id, 'name': song_name, 'singer': song_singer}
        songs.append(song)
    bro.close()
    return songs


print('--------------------------------------------------------------------')
kw = input('请输入搜索歌曲: ')
songs = getSongsByKw(kw)
i = 1
print('--------------------------------------------------------------------')
for song in songs:
    print('按 %d 选择---> %s --- %s' % (i, song['name'], song['singer']))
    i += 1

while True:
    print('--------------------------------------------------------------------')
    n = input('请选择歌曲:')
    try:
        if 1 <= int(n) <= len(songs):
            song = songs[int(n) - 1]
            print('--------------------------------------------------------------------')
            print('正在下载:: %s (%s) ......' % (song['name'], song['singer']))
            flag = download_song_by_id(song['id'])
            print('下载完成!' if flag else '下载失败!!!')
            break
    except Exception as e:
        print(e)
        continue
