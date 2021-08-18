import requests, base64
from Crypto.Cipher import AES
from Netease_cloud_comment_capture.Encrypt import forth_param

def get_params(page): # page为传入页数
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1): # 如果为第一页
        first_param = '{rid:"",  offset:"0",  total:"true",  limit:"20",  csrf_token:""}'
        h_encText = AES_encrypt(first_param,  first_key,  iv)
    else:
        offset = str((page - 1) * 20)
        first_param = '{rid:"",  offset:"%s",  total:"%s",  limit:"20",  csrf_token:""}' %(offset, 'false')
        h_encText = AES_encrypt(first_param,  first_key,  iv)
    h_encText = AES_encrypt(h_encText,  second_key,  iv)
    return h_encText

def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey

def AES_encrypt(text,  key,  iv):
    if type(text) == type(b'123'):
        text = text.decode('utf-8')
    # text=text.decode('utf-8')
    pad = 16 - len(text) % 16

    text = text + pad * chr(pad)

    iv = iv.encode('utf-8')
    key = key.encode('utf-8')
    encryptor = AES.new((key),  AES.MODE_CBC,  (iv))
    text = text.encode('utf-8')
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

# 构造函数获取歌手信息
def get_comments_json(url,  data):
    headers={'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, image/apng, */*;q=0.8',
             'Accept-Encoding': 'gzip,  deflate',
             'Accept-Language': 'zh-CN, zh;q=0.9',
             'Connection': 'keep-alive',
             'Cookie': 'WM_TID=36fj4OhQ7NdU9DhsEbdKFbVmy9tNk1KM; _iuqxldmzr_=32; _ntes_nnid=26fc3120577a92f179a3743269d8d0d9, 1536048184013; _ntes_nuid=26fc3120577a92f179a3743269d8d0d9; __utmc=94650624; __utmz=94650624.1536199016.26.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); WM_NI=2Uy%2FbtqzhAuF6WR544z5u96yPa%2BfNHlrtTBCGhkg7oAHeZje7SJiXAoA5YNCbyP6gcJ5NYTs5IAJHQBjiFt561sfsS5Xg%2BvZx1OW9mPzJ49pU7Voono9gXq9H0RpP5HTclE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed5cb8085b2ab83ee7b87ac8c87cb60f78da2dac5439b9ca4b1d621f3e900b4b82af0fea7c3b92af28bb7d0e180b3a6a8a2f84ef6899ed6b740baebbbdab57394bfe587cd44b0aebcb5c14985b8a588b6658398abbbe96ff58d868adb4bad9ffbbacd49a2a7a0d7e6698aeb82bad779f7978fabcb5b82b6a7a7f73ff6efbd87f259f788a9ccf552bcef81b8bc6794a686d5bc7c97e99a90ee66ade7a9b9f4338cf09e91d33f8c8cad8dc837e2a3; JSESSIONID-WYYY=G%5CSvabx1X1F0JTg8HK5Z%2BIATVQdgwh77oo%2BDOXuG2CpwvoKPnNTKOGH91AkCHVdm0t6XKQEEnAFP%2BQ35cF49Y%2BAviwQKVN04%2B6ZbeKc2tNOeeC5vfTZ4Cme%2BwZVk7zGkwHJbfjgp1J9Y30o1fMKHOE5rxyhwQw%2B%5CDH6Md%5CpJZAAh2xkZ%3A1536204296617; __utma=94650624.1052021654.1536048185.1536199016.1536203113.27; __utmb=94650624.12.10.1536203113',
             'Host': 'music.163.com',
             'Referer': 'http://music.163.com/',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,  like Gecko) '
                           'Chrome/66.0.3359.181 Safari/537.36'}

    try:
        r = requests.post(url,  headers=headers,  data=data)

        r.encoding = "utf-8"
        if r.status_code == 200:  # 状态码 200代表服务器正常响应

            # 返回json格式的数据
            return r.json()
    except:
        print("爬取失败!")


