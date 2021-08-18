import math
import tkinter
from tkinter import *
from Netease_cloud_comment_capture.searchMusic import search
# 搜索歌曲名称
from Netease_cloud_comment_capture.tool import get_params, get_comments_json, get_encSecKey


def get_music_name():
    d = search()
    song_id = d.search_song(entry.get())
    text.insert(END, '解析到歌曲的id为：{}\n'.format(song_id))
    text.update()
    # 歌曲名字
    songname = entry.get()

    # 文件存储路径
    filepath = songname + ".txt"
    page = 1
    params = get_params(1)
    encSecKey = get_encSecKey()
    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(song_id) + '?csrf_token='
    data = {'params': params,  'encSecKey': encSecKey}
    # 获取第一页评论
    html = get_comments_json(url,  data)
    # 评论总数
    total = html['total']
    # 总页数
    pages = math.ceil(total / 20)
    if(total>5):
        pages = 5
    else:
        pages = total

    hotcomments(html,  songname,  page,  pages,  total,  filepath)
    comments(html,  songname,  page,  pages,  total,  filepath)

    # 开始获取歌曲的全部评论
    page = 2
    while page <= pages:
        params = get_params(page)
        encSecKey = get_encSecKey()

        data = {'params': params,  'encSecKey': encSecKey}
        html = get_comments_json(url,  data)
        # 从第二页开始获取评论
        comments(html,  songname,  page,  pages,  total,  filepath)
        page += 1
    tkinter.messagebox.showinfo('提示',  '评论抓取完成，请查看！')
    ########


def hotcomments(html, songname, i, pages, total, filepath):
    text.insert(END, '加载中，请稍等！\n')
    text.update()
    text.after(100)
    # 写入文件
    with open(filepath,  'a',  encoding='utf-8') as f:
        f.write("正在获取歌曲{}的第{}页评论, 总共有{}页{}条评论！\n\n".format(songname,  i,  pages,  total))
    text.insert(END, "正在获取歌曲{}的第{}页评论, 总共有{}页{}条评论！\n\n".format(songname,  i,  pages,  total))
    text.update()
    text.after(100)
    # 精彩评论
    m = 1
    # 键在字典中则返回True,  否则返回False
    if 'hotComments' in html:
        for item in html['hotComments']:
            # 提取发表热门评论的用户名
            user = item['user']
            # 写入文件
            text.insert(END, "   热门评论{}  用户名：{}  点赞次数: {}\n\n".format(m, user['nickname'],item['likedCount']))
            text.insert(END, "   评论内容：{}\n\n".format(item['content']))
            text.update()
            text.after(100)
            with open(filepath,  'a',  encoding='utf-8') as f:
                f.write("   热门评论{}  用户名：{}  点赞次数: {}\n\n".format(m, user['nickname'], item['likedCount']))
                f.write("   评论内容：{}\n\n".format(item['content']))
                text.insert(END, "\n\n")
                # 回复评论
                if len(item['beReplied']) != 0:
                    for reply in item['beReplied']:
                        # 提取发表回复评论的用户名
                        replyuser = reply['user']
                        text.insert(END, "       回复：{} : {}".format(replyuser['nickname'],  reply['content']))
                        text.insert(END, "\n\n")
                        text.update()
                        text.after(100)
                        f.write("       回复：{} : {}\n".format(replyuser['nickname'],  reply['content']))
            m += 1


def comments(html,  songname,  i,  pages,  total,  filepath):
    with open(filepath,  'a',  encoding='utf-8') as f:
        f.write("\n\n正在获取歌曲{}的第{}页评论, 总共有{}页{}条评论！\n".format(songname,  i,  pages,  total))
    text.insert(END, "\n\n正在获取歌曲{}的第{}页评论, 总共有{}页{}条评论！\n".format(songname,  i,  pages,  total))
    text.update()
    text.after(100)

    # 全部评论
    j = 1
    for item in html['comments']:
        # 提取发表评论的用户名
        user = item['user']
        text.insert(END, "   最新评论{}  用户名：{}  点赞次数: {}\n\n".format(j, user['nickname'],item['likedCount']))
        text.insert(END, "   评论内容：{}\n\n".format(item['content']))
        text.insert(END, "\n\n")
        text.update()
        text.after(10)
        with open(filepath, 'a',  encoding='utf-8') as f:
            f.write("   最新评论{}  用户名：{}  点赞次数: {}\n\n".format(j, user['nickname'], item['likedCount']))
            f.write("   评论内容：{}\n\n".format(item['content']))
            text.insert(END, "\n\n")
            # 回复评论
            if len(item['beReplied']) != 0:
                for reply in item['beReplied']:
                    # 提取发表回复评论的用户名
                    replyuser = reply['user']
                    text.insert(END, "       回复：{} : {}".format(replyuser['nickname'],  reply['content']))
                    text.insert(END, "\n\n")
                    text.update()
                    text.after(10)
                    f.write("       回复：{} : {}\n".format(replyuser['nickname'],  reply['content']))
        j += 1

# 创建界面
root = Tk()
# 标题
root.title("网易云评论爬取脚本")
# 设置窗口大小
root.geometry('1123x410')
root.configure(bg="#FFFFDF")

# 标签控件
label = Label(root, text='请输入要爬取的歌曲名称：', font=('幼圆', 15,), bg='#FAF4FF')
# 标签定位
label.grid(sticky=W)

# 输入框
entry = Entry(root, font=('幼圆', 15), bg='#ECECFF')
entry.grid(row=0, column=1, sticky=W)

# 抓取按钮
button = Button(root, text='抓取评论', font=('幼圆', 15), command=get_music_name, bg='#CEFFCE')
# 左对齐
button.grid(row=0, column=2, sticky=W)

# 列表框
text = Listbox(root, font=('幼圆', 16), width=100, height=20, bg='#E6E6F2')
text.grid(row=1, columnspan=4)

# 退出按钮
button1 = Button(root,  text='退出',  font=('幼圆',  15),  command=root.quit, bg='#CAFFFF')
button1.grid(row=0,  column=3,  sticky=E)
# 显示界面
root.mainloop()
