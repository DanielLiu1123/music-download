from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from core.config import DRIVER_PATH
from core.download_50hot_songs_by_artist_id import get_hot_songs_by_singer_id


def getSingersByKw(kw):
    # # 无可视化界面(无头浏览器)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # selenium规避检测
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 设置代理ip
    # chrome_options.add_argument("--proxy-server=http://211.24.105.19:47615")

    bro = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
    bro.get("https://music.163.com/#/search/m/?id=6452&s=%s&type=100" % kw)
    bro.switch_to.frame('g_iframe')
    # print(bro.page_source)
    # 获取热门歌曲
    sleep(1)
    lis = bro.find_elements_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div/div/ul/li')
    # 只提取根据关键字搜索出的5个歌手
    if len(lis) > 5:
        lis = lis[:5]

    # 列出五个歌手
    singers = []
    for li in lis:
        ele = li.find_element_by_css_selector('p > a')
        singer_name = ele.text
        singer_id = ele.get_attribute('href').split('=')[1]
        # print(singer_name)
        # print(singer_id)
        singer = {'id': singer_id, 'name': singer_name}
        singers.append(singer)
    return singers


print('--------------------------------------------------------------------')
kw = input('请输入搜索歌手: ')
singers = getSingersByKw(kw)
i = 1
print('--------------------------------------------------------------------')
for singer in singers:
    print('按 %d 选择---> %s' % (i, singer['name']))
    i += 1

while True:
    print('--------------------------------------------------------------------')
    n = input('请选择歌手:')
    try:
        if 1 <= int(n) <= len(singers):
            singer = singers[int(n) - 1]
            singer_id = singer['id']
            print('--------------------------------------------------------------------')
            print('正在下载 %s 热门歌曲......' % (singer['name']))
            get_hot_songs_by_singer_id(singer_id)
            print('下载完成!')
            break
    except Exception as e:
        print(e)
        continue
