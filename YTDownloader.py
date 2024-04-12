import os
from pytube import YouTube
from googleapiclient.discovery import build
import tkinter as tk
from tkinter import messagebox, filedialog

API_KEY = 'AIzaSyB8bwL7RWovJKLJU-CeiDEukdxDRjuSYRU'  # ここに取得したAPIキーを入力
youtube = build('youtube', 'v3', developerKey=API_KEY)

def download_video_and_comments(url):
    try:
        # ダウンロード先のディレクトリを選択
        directory = filedialog.askdirectory()
        if not directory:
            return

        # 動画のダウンロード
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(directory)
        video_title = yt.title.replace("/", "|")  # ファイル名に使用できない文字を置き換え

        # コメントとチャットの取得
        comments = []
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=yt.video_id,
            maxResults=100,  # 最大100件のコメントを取得
            textFormat="plainText"
        )
        response = request.execute()

        for item in response['items']:
         author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
         comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
         comments.append(f"{author}: {comment}")


        # コメントをファイルに保存
        comments_file_path = os.path.join(directory, f"{video_title}_comments.txt")
        with open(comments_file_path, 'w', encoding='utf-8') as f:
            for comment in comments:
                f.write(comment + "\n")

        messagebox.showinfo("成功", f"ダウンロード完了: {video_title}\nコメントが保存されました。")
    except Exception as e:
        messagebox.showerror("エラー", str(e))

# GUIアプリの作成
app = tk.Tk()
app.title("YouTube Video and Comments Downloader")

# ラベルの追加
label = tk.Label(app, text="YouTube URL:")
label.pack(pady=10)

# テキストエントリーの追加
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=10)

# ダウンロードボタンの追加
download_button = tk.Button(app, text="Download Video and Comments", command=lambda: download_video_and_comments(url_entry.get()))
download_button.pack(pady=20)

# アプリケーションの実行
app.mainloop()
