import requests
from Netease_cloud_comment_capture.Encrypt import Encrypted

class search():
    '''跟歌单直接下载的不同之处，1.就是headers的referer
                              2.加密的text内容不一样！
                              3.搜索的URL也是不一样的
        输入搜索内容，可以获取歌曲ID
                                '''
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/'}
        self.main_url='http://music.163.com/'
        self.session = requests.Session()
        self.session.headers=self.headers
        self.ep = Encrypted()

    def search_song(self,  search_content, search_type=1,  limit=9):
        """
        根据音乐名搜索
      :params search_content: 音乐名
      :params search_type: 不知
      :params limit: 返回结果数量
      return: 可以得到id 再进去歌曲具体的url
        """
        url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        text = {'s': search_content,  'type': search_type,  'offset': 0,  'sub': 'false',  'limit': limit}
        data = self.ep.search(text)
        resp = self.session.post(url,  data=data)
        result = resp.json()
        if result['result']['songCount']<= 0:
            print('搜不到！！')
        else:
            songs = result['result']['songs']
            for song in songs:
                song_id = song['id']
                return song_id