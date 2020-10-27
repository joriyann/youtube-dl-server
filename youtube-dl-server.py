from __future__ import unicode_literals
import json
import os
import subprocess
from queue import Queue
from bottle import route, run, Bottle, request, static_file, view
from threading import Thread
import youtube_dl
from pathlib import Path
from collections import ChainMap

app_defaults = {
    'YDL_FORMAT': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    'YDL_EXTRACT_AUDIO_FORMAT': None,
    'YDL_EXTRACT_AUDIO_QUALITY': '192',
    'YDL_RECODE_VIDEO_FORMAT': None,
    'YDL_OUTPUT_TEMPLATE': '/Users/Cha/Yannick/-server/downloads/%(title)s [%(id)s].%(ext)s',
    'YDL_ARCHIVE_FILE': None,
    'YDL_SERVER_HOST': 'localhost',
    'YDL_SERVER_PORT': 8080,
}

empty_sample = []

sample = [
    {
        'id': 1,
        'filename': 'toto',
        'filesize': '3 Mo',
        'progress': 0.6,
        'speed': 15
    }
]

@route('/')
def dl_queue_list():
    return static_file('index.html', root='./')

@route('/new')
@view('index.tpl')
def get():
    return dict(downloads=empty_sample)

@route('/', method='POST')
@view('index.tpl')
def create_dl():
    url = request.forms.get("url")
    if not url:
        return {"success": False, "error": "/q called without a 'url' query param"}

    options = {
        'format': request.forms.get("format")
    }

    dl_q.put((url, options))
    print("Added url " + url + " to the download queue")
    
    return dict(downloads=sample)

@route('/static/:filename#.*#')
def server_static(filename):
    return static_file(filename, root='./static')

@route('/q', method='GET')
def q_size():
    return {"success": True, "size": json.dumps(list(dl_q.queue))}

@route('/q', method='POST')
def q_put():
    url = request.forms.get("url")
    options = {
        'format': request.forms.get("format")
    }

    if not url:
        return {"success": False, "error": "/q called without a 'url' query param"}

    dl_q.put((url, options))
    print("Added url " + url + " to the download queue")
    return {"success": True, "url": url, "options": options}

@route("/update", method="GET")
def update():
    command = ["pip", "install", "--upgrade", ""]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = proc.communicate()
    return {
        "output": output.decode('ascii'),
        "error":  error.decode('ascii')
    }

def dl_worker():
    while not done:
        url, options = dl_q.get()
        download(url, options)
        dl_q.task_done()

def get_ydl_options(request_options):
    request_vars = {
        'YDL_EXTRACT_AUDIO_FORMAT': None,
        'YDL_RECODE_VIDEO_FORMAT': None,
    }

    requested_format = request_options.get('format', 'bestvideo')

    if requested_format in ['aac', 'flac', 'mp3', 'm4a', 'opus', 'vorbis', 'wav']:
        request_vars['YDL_EXTRACT_AUDIO_FORMAT'] = requested_format
    elif requested_format == 'bestaudio':
        request_vars['YDL_EXTRACT_AUDIO_FORMAT'] = 'best'
    elif requested_format in ['mp4', 'flv', 'webm', 'ogg', 'mkv', 'avi']:
        request_vars['YDL_RECODE_VIDEO_FORMAT'] = requested_format

    ydl_vars = ChainMap(request_vars, os.environ, app_defaults)

    postprocessors = []

    if(ydl_vars['YDL_EXTRACT_AUDIO_FORMAT']):
        postprocessors.append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': ydl_vars['YDL_EXTRACT_AUDIO_FORMAT'],
            'preferredquality': ydl_vars['YDL_EXTRACT_AUDIO_QUALITY'],
        })

    if(ydl_vars['YDL_RECODE_VIDEO_FORMAT']):
        postprocessors.append({
            'key': 'FFmpegVideoConvertor',
            'preferedformat': ydl_vars['YDL_RECODE_VIDEO_FORMAT'],
        })

    return {
        'format': ydl_vars['YDL_FORMAT'],
        'postprocessors': postprocessors,
        'outtmpl': ydl_vars['YDL_OUTPUT_TEMPLATE'],
        'download_archive': ydl_vars['YDL_ARCHIVE_FILE'],
        'ratelimit': '50K'
    }

def download(url, request_options):
    with youtube_dl.YoutubeDL(get_ydl_options(request_options)) as ydl:
        ydl.download([url])

dl_q = Queue()
done = False
dl_thread = Thread(target=dl_worker)
dl_thread.start()

# print("Updating  to the newest version")
# updateResult = update()
# print(updateResult["output"])
# print(updateResult["error"])

print("Started download thread")

app_vars = ChainMap(os.environ, app_defaults)

run(host=app_vars['YDL_SERVER_HOST'], port=app_vars['YDL_SERVER_PORT'], debug=True)
done = True
dl_thread.join()
