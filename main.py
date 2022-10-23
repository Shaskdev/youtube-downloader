from pytube import Stream
from pytube import YouTube
from pytube.cli import on_progress  # progress bar for download tracking
import ffmpeg  # to merge audio and video streams
import time
import os


def clean_filename(name):
    """Ensures the filename has no forbidden characters"""
    forbidden_char = "\"*\\/'.|?:<>"
    filename = (("".join([x if x not in forbidden_char else "#"
                          for x in name])).replace("  ", " ").strip())
    if len(filename) >= 176:
        filename = filename[:170] + "..."
    return filename


def cleanup():
    os.remove('/home/shask/Code/Python/youtube-downloader/video.mp4')
    print("Video File Removed")
    os.rename('/home/shask/Code/Python/youtube-downloader/audio.mp3',
              '/home/shask/audio-files/audio.mp3')
    print("Audio File moved to Audio Folder")


url = input("Enter the link: ")
ti = time.time()
yt = YouTube(url, on_progress_callback=on_progress)
print(f"Downloading {yt.title}")
print("Video Author: ", yt.author)
print("Video Length: ", yt.length, "sec")

try:
    yt.streams.filter(
        res="2160p",
        progressive=False,
    ).first().download(filename="video.mp4")
    yt.streams.filter(
        abr="160kbps",
        progressive=False,
    ).first().download(filename="audio.mp3")
    res = "2160p"
except:
    yt.streams.filter(
        res="1080p",
        progressive=False,
    ).first().download(filename="video.mp4")
    yt.streams.filter(
        abr="160kbps",
        progressive=False,
    ).first().download(filename="audio.mp3")
    res = "1080p"

audio = ffmpeg.input("audio.mp3")
video = ffmpeg.input("video.mp4")
filename = "/home/shask/video-downloads/" + clean_filename(yt.title) + ".mp4"
ffmpeg.output(audio, video, filename).run(overwrite_output=True)
print(res, "Video successfully downloaded from ", url)
print("Time taken {:.0f} sec".format(time.time() - ti))

cleanup()

#cleanup files to avoid problems from not remvoing the individual video.mp4 and audio.mp3
