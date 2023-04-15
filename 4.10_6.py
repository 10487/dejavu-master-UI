import tkinter

from dejavu import Dejavu
import ast
from tkinter.filedialog import askdirectory
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import pyaudio
import wave
import mysql.connector
import eyed3
from pydub.playback import play
import datetime
from pydub import AudioSegment
import pygame
import threading
import shutil

from tkinter import *
import time

config = {
    "database": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "zxh-0524",
        "database": "dejavu"
    },
}
djv = Dejavu(config)

# 存储音乐信息的数据库
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="zxh-0524",
    database="music",
    buffered=True
)


# 创建主窗口
root = tk.Tk()
root.title("音乐教学辅助系统")

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# root.geometry(f"{screen_width}x{screen_height}+0+0")
# root.resizable(False, False)  # 窗口大小不可变
# 计算窗口宽度和高度
win_width = 1000
win_height = 650

# 计算窗口左上角的坐标
x = (screen_width - win_width) // 2
y = (screen_height - win_height) // 2

# 设置窗口位置和大小
root.geometry(f"{win_width}x{win_height}+{x}+{y}")


menubar = tkinter.Menu(root)

# 上传目录函数
def upload_file():
    folder_path = askdirectory()
    if folder_path:
        djv.fingerprint_directory(folder_path, [".mp3"], 3)
        print(djv.db.get_num_fingerprints())

# # 上传单个音乐文件
# def upload_signal(song_name):
#     # 打开文件对话框，让用户选择要上传的音乐文件
#     # 需要将其改成输入歌名
#     file_path = "mp3/{}.mp3".format(song_name)
#     # file_path = filedialog.askopenfilename(parent=root)
#     # if file_path:
#     #     djv.fingerprint_file(file_path)
#     if file_path:
#         djv.fingerprint_file(file_path)

##################################################################
def upload_signal():
    # 打开文件对话框，让用户选择要上传的音乐文件
    # 需要将其改成输入歌名
    # file_path = "mp3/{}.mp3".format(song_name)
    file_path = "E:/音乐辅助上传目录"
    # file_path = filedialog.askopenfilename(parent=root)
    # if file_path:
    #     djv.fingerprint_file(file_path)

    # mycursor = mydb.cursor()

    if file_path:
        # djv.fingerprint_file(file_path)  # 音频信息导入数据库
        djv.fingerprint_directory(file_path, [".mp3"], 1)
        # audiofile = eyed3.load(file_path)  # 处理音频
        # title = audiofile.tag.title  # 获取音频标题
        # query = "SELECT * FROM songs WHERE title LIKE %s"
        # mycursor.execute(query, ('%' + title + '%',))

        # info_str = "\n".join("{}".format(value) for value in mycursor)
        # return info_str
        # for (id, title, artist, duration) in mycursor:
        #     mycursor.close()
        #     return "歌名：{}\n\n\n歌手：{}".format(title, artist)

def daoruxinxi():
    # 创建一个游标对象
    mycursor = mydb.cursor()

    # 指定音频文件所在目录
    directory = "E:/音乐辅助上传目录"

    mycursor.execute("SHOW TABLES LIKE 'songs'")
    result = mycursor.fetchone()
    if not result:
        mycursor.execute("CREATE TABLE songs (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), artist VARCHAR(255), duration VARCHAR(20))")
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):  # 只处理mp3格式的音频文件
            # 获取音频文件的元数据信息
            # 这里可以使用第三方库，比如mutagen等等
            filepath = os.path.join(directory, filename)
            try:
                # 打开MP3文件
                audiofile = eyed3.load(filepath)

                # 获取标题、艺术家和时长等信息
                title = audiofile.tag.title
                artist = audiofile.tag.artist
                duration = audiofile.info.time_secs

                # 输出信息
                # print("Title:", title)
                # print("Artist:", artist)
                # print("Duration:", duration, "seconds")

                # 构造SQL语句并执行
                sql = "INSERT INTO songs (title, artist, duration) VALUES (%s, %s, %s)"
                val = (title, artist, duration)
                mycursor.execute(sql, val)

            except (AttributeError, ValueError):
                # 处理文件标签为空或者格式不正确的情况
                print("Unable to process file:", filepath)
    # 提交更改
    mydb.commit()

# 创建按钮并绑定事件
def on_button_click():
    # 获取文本框中输入的歌曲名
    # song_name = song_name_entry1.get()
    # dis_dir = "./mp3"

    # with open("E:/music/VipSongsDownload/".format(song_name), 'rb') as src_file:
    #     content = src_file.read() # 打开song_name文件
    #
    # file_name = os.path.basename(song_name)
    # dis_file_path = os.path.join(dis_dir, file_name) # 在MP3文件夹下创建了文件
    #
    # with open(dis_file_path, 'wb') as dst_file:
    #     dst_file.write(content)# 写入内容

    source_file = filedialog.askopenfilename(title="Select an audio file")

    #source_file = "path/to/your/source/audio/file.mp3"
    #
    audiofile = eyed3.load(source_file)  # 处理音频

    title = audiofile.tag.title  # 获取音频标题
    destination_file = "E:/音乐辅助上传目录/{}.mp3".format(title)
    shutil.copy(source_file, destination_file)
    # 调用处理函数
    # song_str = upload_signal()
    file_path = "E:/音乐辅助上传目录"

    upload_signal()
    daoruxinxi()

    # 获取返回值
    # global result_text2
    # result_text2.delete("1.0", tk.END)  # 清空文本框内容
    # result_text2.insert(tk.END, song_str)
    #     upload_signal上传单个文件函数


###############################################################
#  检索歌名
def get_song_info(song_name):
    mycursor = mydb.cursor()
    query = "SELECT * FROM songs WHERE title LIKE %s"
    mycursor.execute(query, ('%' + song_name + '%',))

    info_str = ""
    for (id, title, artist, duration) in mycursor:
        info_str = "1"
        mycursor.close()
        return "歌名：{}\n\n\n歌手：{}\n\n\n".format(title, artist)

    if not info_str:
        info_str = 0
        return "未找到该歌曲信息。"

#  创建搜索按钮绑定事件
def select_song():
    # global song_name_entry1  # 全局的按钮
    songname = song_name_entry1.get()
    song_str = get_song_info(songname)

    global result_text2
    result_text2.delete("1.0", tk.END)  # 清空文本框内容
    result_text2.insert(tk.END, song_str)
############################################################

# 播放函数
def play_audio(file_path):
    audio = AudioSegment.from_file(file_path) #存放的是路径
    play(audio)

# def on_button_click2():
#     # 获取文本框中输入的歌曲名
#     song_name = song_name_entry1.get()
#     # 调用处理函数
#     play_audio("mp3/{}".format(song_name))
#     # 获取返回值

    #     upload_signal上传单个文件函数
###############################################################

# 检索函数
def recognize_file():
    # 获取当前py文件所在的目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 打开指定文件夹test
    file_path = filedialog.askopenfilename(initialdir=current_dir + '/test', parent=root)

    if file_path:
        try:
            # 调用 dejavu.py 脚本进行音乐识别
            result = subprocess.check_output(
                ['python', 'dejavu.py', '--recognize', 'file', file_path])

            # 将bytes类型的字符串转换为str类型
            result_str = result.decode("utf-8")

            # 将字符串解析为字典
            result_dict = ast.literal_eval(result_str.replace("'", '"'))

            # 获取歌曲名列表
            songs = []
            for item in result_dict["results"]:
                songs.append(item["song_name"].decode("utf-8"))

            # 将歌曲名列表转换为字符串
            song_str = "\n".join([f"第{i + 1}首：{song}" for i, song in enumerate(songs)])

            # 创建新窗口显示检索结果
            # result_window = tk.Toplevel(root)
            # result_window.title("识别结果")

            # 创建Text组件用于显示检索结果
            # result_text = tk.Text(root, height=10, width=60, font=("Arial", 12))
            # result_text.grid(row=5, column=0, padx=10, pady=(10, 20))

            # 添加检索结果到Text组件中
            result_text.delete("1.0", tk.END)  # 清空文本框内容
            result_text.insert(tk.END, song_str)

        except subprocess.CalledProcessError as e:
            recognize_file()
###################################################

# 录音参数
def get_recording_params():
    return {
        'chunk': 1024,
        'format': pyaudio.paInt16,
        'channels': 2,
        'rate': 44100,
        'record_seconds': 5,
        'output_filename': "./test/output.wav"
    }

def record(params):
    global is_recording
    global frames
    p = pyaudio.PyAudio()
    stream = p.open(format=params['format'],
                    channels=params['channels'],
                    rate=params['rate'],
                    input=True,
                    frames_per_buffer=params['chunk'])

    print("开始录音...")

    while is_recording:
        data = stream.read(params['chunk'])
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    save_recording(params)

def start_recording(params):
    global is_recording
    if not is_recording:
        is_recording = True
        record_thread = threading.Thread(target=record, args=(params,))
        record_thread.start()

def pause_and_save_recording():
    global is_recording
    if is_recording:
        is_recording = False
        print("暂停并保存录音")

def save_recording(params):
    global frames

    print("保存录音")
    wf = wave.open(params['output_filename'], 'wb')
    wf.setnchannels(params['channels'])
    wf.setsampwidth(pyaudio.get_sample_size(params['format']))
    wf.setframerate(params['rate'])
    wf.writeframes(b''.join(frames))
    wf.close()
    frames = []


# 录音函数
def record_audio(duration_seconds):
    # 配置录音参数
    CHUNK = 1024  # 每个音频块的大小
    FORMAT = pyaudio.paInt16  # 音频格式
    CHANNELS = 1  # 声道数
    RATE = 44100  # 采样率（每秒采集的样本数）

    # 创建PyAudio对象
    audio = pyaudio.PyAudio()

    # 打开音频流
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * duration_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    # 停止录音并保存音频文件
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 生成文件名
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"test/{now}.wav"


    wave_file = wave.open(file_path, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

    print(f"Recording saved as {file_path}.")
    return file_path

#
# def start_recording():
#     record_time = 10  # 录音时长（单位：秒）
#     record_audio(record_time)

################################################
# 创建按钮并绑定事件
# def on_button_click():
#     # 获取文本框中输入的歌曲名
#
#     song_name = song_name_entry.get()
#     # 调用处理函数
#     process_song_name(song_name)

# 将默认的文本框自动删除
def on_entry_click1(event):
    """当鼠标单击Entry小部件时，删除默认标签"""
    if song_name_entry1.get() == '请输入音乐音频名...':
        song_name_entry1.delete(0, tk.END)  # 删除整个文本框的内容
        song_name_entry1.insert(0, '')  # 确保将焦点移动到文本框的开头

def on_entry_click2(event):
    """当鼠标单击Entry小部件时，删除默认标签"""
    if song_name_entry2.get() == '请输入音乐短片名...':
        song_name_entry2.delete(0, tk.END)  # 删除整个文本框的内容
        song_name_entry2.insert(0, '')  # 确保将焦点移动到文本框的开头
###############################4.1#####################################
def record_and_recognize():
    record_time = 10  # 录音时长（单位：秒）
    file_path = record_audio(record_time)
    # 对保存的音频文件进行检索
    recognize_audio(file_path)
    # 删除保存的音频文件
    os.remove(file_path)


#检索录音文件
def recognize_audio(file_path):
    try:
        # 调用 dejavu.py 脚本进行音乐识别
        result = subprocess.check_output(
            ['python', 'dejavu.py', '--recognize', 'file', file_path])
        # 将bytes类型的字符串转换为str类型
        result_str = result.decode("utf-8")
        # 将字符串解析为字典
        result_dict = ast.literal_eval(result_str.replace("'", '"'))
        # 获取歌曲名列表
        songs = []
        for item in result_dict["results"]:
            songs.append(item["song_name"].decode("utf-8"))
        # 将歌曲名列表转换为字符串
        song_str = "\n".join([f"第{i + 1}首：{song}" for i, song in enumerate(songs)])

        # 在Text组件中显示检索结果
        if song_str:
            result_text.config(state=tk.NORMAL)  # 将文本框显示出来
            result_text.delete('1.0', tk.END)  # 删除原有内容
            result_text.insert(tk.END, song_str)  # 插入新的检索结果
        else:
            tk.messagebox.showinfo("提示", "没有匹配的音乐片段！")
    except Exception as e:
        # 如果检索失败，则弹出消息框提示用户
        tk.messagebox.showerror("错误", "检索失败，请检查录音文件格式是否正确！")

############################4.4##############################################

#音频播放
def play_audio():
    # 初始化pygame
    pygame.mixer.init()
    # audio_file = "./mp3/Brad-Sucks--Total-Breakdown.mp3"
    audio_file = AddressEntry.get()
    pygame.mixer.music.load("./mp3/{}".format(audio_file))  # 加载音频文件
    pygame.mixer.music.play()  # 播放音频

    audio_length = pygame.mixer.Sound("./mp3/{}".format(audio_file)).get_length()
    progress.configure(to=audio_length)


#播放/暂停
def pause_audio():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

#进度条
def update_audio_position(val):
    global user_changed
    user_changed = True
    new_pos = float(val)
    pygame.mixer.music.set_pos(new_pos)

##############################4.9##########################################
'''
# 定义一些变量
folder = '' #歌曲文件夹路径
res = [] #存放歌曲路径
ret = [] #存放歌曲名称
num = 0
now_music = ''
one_start = True
# 功能
# 添加文件
def buttonChooseFile():
    global folder
    global res
    global ret
    folder = tkinter.filedialog.askdirectory()
    if folder:
        musics = [folder + '\\' + music
                  for music in os.listdir(folder)\
\
                  if music.endswith(('.mp3','.wav','.ogg'))]
        for i in musics:
            ret.append(i.split('\\')[1:])
            res.append(i.replace('\\','/'))
        var2 = tkinter.StringVar()
        var2.set(ret)
        global lb
        lb = tkinter.Listbox(root,listvariable=var2)

        lb.place(x=860,y=100,width=380,height=400)
        lb.bind("<Double-Button-1>", playActive) #绑定单击事件

    if not folder:
        return
    global playing
    playing = True
    # 根据情况禁用和启用相应的按钮
    button_play['state'] = 'normal'
    button_delete['state'] = 'normal'
    voice_bar['state'] = 'normal'
    pause_resume.set('播放')
# 删除音乐
def buttonDeleteClick():
    music = lb.get('active')[0]
    list_temp = [music]
    ret.remove(list_temp)
    for i in res:
        if i.split("/")[-1] == music:
            res.remove(i)
    lb.delete('active')

# 播放音乐
def play():
    global one_start
    if len(res):
        # 初始化
        pygame.mixer.init()
        global num
        while playing:
            if not pygame.mixer.music.get_busy():
                nextMusic = res[num]
                if one_start:
                    # 播放选中的那首歌
                    nextMusic = lb.get('active')
                    temp_list = [nextMusic[0]]
                    current_index = ret.index(temp_list)
                    num = current_index
                    nextMusic = res[current_index]
                pygame.mixer.music.load(nextMusic.encode())
                # 播放一次
                pygame.mixer.music.play(1)

                if len(res) - 1 == num:
                    num = 0
                else:
                    num = num + 1
                nextMusic = nextMusic.split('/')[-1]
                play_state.set('playing...')
                musicName.set(nextMusic)
                one_start = False
            else:
                time.sleep(0.1)
# 响应双击事件的
def playActive(self):
    global playing,one_start,num
    if not one_start:
        playing = False
        pygame.mixer.init()
        pygame.mixer.music.stop()

        nextMusic = lb.get('active')
        temp_list = [nextMusic[0]]
        current_index = ret.index(temp_list)
        num = current_index

        playing = True
        # 创建线程播放音乐
        t = threading.Thread(target=play)
        t.start()

# 点击播放
def buttonPlayClick():
    button_next['state'] = 'normal'
    button_prev['state'] = 'normal'
    # 选择要播放的音乐文件夹
    if pause_resume.get() == '播放':
        pause_resume.set('暂停')
        play_state.set('playing...')
        global folder
        if not folder:
            folder = tkinter.filedialog.askdirectory()
        if not folder:
            return
        global playing
        playing = True
        # 创建一个线程来播放音乐，当前主线程用来接收用户操作
        t = threading.Thread(target=play)
        t.start()
    elif pause_resume.get() == '暂停':
        # pygame.mixer.init()
        pygame.mixer.music.pause()
        pause_resume.set("继续")
        play_state.set('paused...')
    elif pause_resume.get() == '继续':
        # pygame.mixer.init()
        pygame.mixer.music.unpause()
        pause_resume.set('暂停')
        play_state.set('playing...')
# 上一首
def buttonPrevClick():
    global playing
    playing = False
    pygame.mixer.init()
    pygame.mixer.music.stop()
    global num
    if num == 0:
        num = len(res) - 2
    elif num == len(res) - 1:
        num -= 2
    else:
        num -= 2
    lb.activate(num)
    lb.see(num)
    playing = True
    # 创建线程播放音乐
    t = threading.Thread(target=play)
    t.start()
# 下一首
def buttonNextClick():
    global playing
    playing = False
    pygame.mixer.music.stop()
    global num
    if len(res) == num:
        num = 0
    playing = True
    lb.activate(num)
    lb.see(num)

    # 创建线程播放音乐
    t = threading.Thread(target=play)
    t.start()
# 关闭窗口
def closeWindow():
    global playing
    playing = False
    time.sleep(0.3)
    try:
        # 停止播放，如果已经停止
        # 再次停止时会抛出异常，所以需要异常捕获
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
    root.destroy() # 整个界面退出
# 音量控制，默认是一半的音量值
def control_voice(value=0.5):
    try:
        pygame.mixer.music.set_volume(float(value))
    except:
        pass
'''




if __name__ == '__main__':
    # 创建标签
    label = tk.Label(root,
                     text="欢迎使用音乐教学辅助系统！",font=("宋体", 14,'bold'),anchor="center")#width=105, height=2,,relief="groove",
    label.place(x=380, y=20)
    # pady=20, padx=10,#label.grid(row=0, column=0, pady=00, padx=00, sticky="nsew")
    #label.grid(row=0, column=0, columnspan=6)
    #label.grid(sticky="nsew")
    # （ui版本）创建标签
    label = tk.Label(root,text="( UI版本 )",font=("宋体", 10),anchor="center",justify="center")#width=105, height=1,
    label.place(x=475, y=50)
    # pady=20, padx=10,# label.grid(row=0, column=0, pady=00, padx=00, sticky="nsew")
    #label.grid(row=1, column=0, columnspan=6)



    #文本框1
    global song_name_entry1
    song_name_entry1 = tk.Entry(root)
    song_name_entry1.insert(0, "请输入音乐音频名...")
    song_name_entry1.bind('<FocusIn>', on_entry_click1)
    #song_name_entry1.grid(row=2, column=0, columnspan=1,pady=20, padx=10)
    song_name_entry1.place(x=170,y=105)

    # 检索按钮
    search_button = tk.Button(root, text="信息检索",  font=('宋体', 14),width=8, height=1,
                              command=select_song)#width=8, height=1,
    #search_button.grid(row=2, column=2, padx=10, pady=20)
    search_button.place(x=400,y=100)
    # 上传音乐——创建上传目录按钮*上传音乐目录到数据库
    button_upload = tk.Button(root, text="上传音乐", font=('宋体', 14),width=8, height=1,
                              command=on_button_click)  # width=8, height=1,
    # button_upload.grid(row=2, column=1, padx=10, pady=(10, 20))  # pady=(10, 20)
    button_upload.place(x=400, y=160)



    # 录音
    params = get_recording_params()
    # 录音和暂停状态
    is_recording = False
    frames = []

    button_upload = tk.Button(root, text="开始录音", font=('宋体', 14),width=8, height=1,
                              command=lambda: start_recording(params))#width=8, height=1,
    #button_upload.grid(row=4, column=0, padx=10, pady=(10, 20))  # pady=(10, 20)
    button_upload.place(x=550,y=100)
    # 结束（录音）
    search_button = tk.Button(root, text="录音结束", font=('宋体', 14),width=8, height=1,
                              command=pause_and_save_recording)
    search_button.grid(row=4, column=2)
    search_button.place(x=550, y=160)


    # 听曲识别
    button_recognize = tk.Button(root, text="听曲识别", width=8, height=1, font=('宋体', 14),
                                 command=record_and_recognize)
    #button_recognize.grid(row=3, column=1, padx=10, pady=(10, 20))
    button_recognize.place(x=700,y=100)


    # 片段识别
    button_recognize = tk.Button(root, text="片段识别",width=8, height=1,  font=('宋体', 14),
                                 command=recognize_file)
    #button_recognize.grid(row=3, column=2, padx=10, pady=(10, 20))
    button_recognize.place(x=700, y=160)

    #标签：音乐音频/音乐短片
    label = tk.Label(root, text="音乐信息显示", font=('Arial', 11, 'bold'))#relief='groove'
    #label.grid(row=5, column=0,sticky="nsew")
    label.place(x=610, y=390)
    # 出结果1——创建显示“识别"文本框
    result_text2 = tk.Text(root, height=10, width=35, font=("Arial", 12))
    #result_text2.grid(row=6, column=0,padx=50, pady=10)#padx=10, pady=(10, 20)
    result_text2.place(x=500,y=420)


    # 标签：检索结果/音乐播放
    label = tk.Label(root, text="听曲识别 / 片段识别结果", font=('Arial', 11, 'bold'))#, relief='groove'
    #label.grid(row=5, column=2,sticky="nsew")
    label.place(x=150, y=390)

    # 出结果2——创建显示“识别"文本框
    result_text = tk.Text(root, height=10, width=35, font=("Arial", 12))
    #result_text.grid(row=6, column=2,padx=50, pady=10)#, padx=10, pady=(10, 20)
    result_text.place(x=80,y=420)


    # 输入框-输入音频地址
    AddressEntry = tkinter.Entry(root, width=20)
    AddressEntry.place(x=170, y=160)

    #播放音乐——确认键
    confirmButton = tkinter.Button(root, text="播放音乐",font=('宋体', 14), width=8, height=1,command=play_audio)#, width=2
    confirmButton.place(x=550, y=225)


    # 进度条
    progress = ttk.Scale(root,orient="horizontal",length=200,command=update_audio_position)#
    progress.place(x=170,y=230)

    #秒数
    entry_var1 = tk.StringVar()
    entry_var1.set('00:00')
    en2 = tk.Entry(root, textvariable=entry_var1, justify=CENTER)#, justify=CENTER
    en2.place(x=405, y=235, width=80, height=15)#, width=80, height=15

    #开始/暂停
    CtrlButton = tk.Button(root, text="开始暂停", font=('宋体', 14),width=8, height=1,command=pause_audio)
    CtrlButton.place(x=700, y=225)


    # 创建一个播放的显示部分
    # 显示窗口  启动主循环
    root.mainloop()



#
    # #菜单
    # menu = tkinter.Menu(menubar, tearoff=False)
    # for item in ["单文件上传", "多文件上传"]:
    #     menu.add_command(label=item)
    #
    # menubar.add_cascade(label="上传文件", menu=menu)
    #
    #
    # def showMeun(e):
    #     menubar.post(e.x_root, e.y_root)
    #
    # root.bind("<Button-3>", showMeun)