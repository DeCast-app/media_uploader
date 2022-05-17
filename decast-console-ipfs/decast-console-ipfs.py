#!/usr/bin/python
# -*- coding: UTF-8 -*-
     
import sys
import argparse
import os
import io
import shutil
import time
from threading import Thread
from pathlib import Path
import subprocess
from subprocess import Popen, PIPE, run
import psutil
import math
import base64
import json

from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.resize import resize
     
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-c', '--command', default='ping')
    parser.add_argument ('-d', '--ipfs_dirrectory', default='~/.ipfs')
    parser.add_argument ('-i', '--ipfs_id', default='QmWXShtJXt6Mw3FH7hVCQvR56xPcaEtSj4YFSGjp2QxA4v')
    parser.add_argument ('-fld', '--file_load_dir', default='~/.ipfs')
    parser.add_argument ('-fsd', '--file_save_dir', default='~/.ipfs')
    parser.add_argument ('-fsn', '--file_save_name', default='001.mp4')
    parser.add_argument ('-fst', '--file_save_type', default='json')

    parser.add_argument ('-vn', '--video_name', default='Name')
    parser.add_argument ('-va', '--video_avtor', default='Avtor')
    parser.add_argument ('-vd', '--video_description', default='Description')
    parser.add_argument ('-vc', '--video_commercial', default='Yes')
    parser.add_argument ('-vl', '--video_language', default='eng')
    parser.add_argument ('-vp', '--video_pegi', default='18+')
    parser.add_argument ('-vo', '--video_tags', default='Funny')
    parser.add_argument ('-vt', '--video_time', default='07.05.2022 00:00:00.000000')
    parser.add_argument ('-v', '--video_file', default='~/.ipfs')
    parser.add_argument ('-p', '--poster_file', default='~/.ipfs')
    parser.add_argument ('-vr', '--video_resize_width', default=None)
    return parser

def pong():
    return {"Result": "pong!"}

def initIPFS(ipfs_dirrectory):
    os.environ['IPFS_PATH'] = str(ipfs_dirrectory)
    #output = subprocess.check_output(['bash','-c', 'echo $IPFS_PATH:$(hadoop classpath):'+str(ipfs_dirrectory)])
    #output = subprocess.run(['sh','-c', f"SetEnvironmentVariable('IPFS_PATH','{ipfs_dirrectory}')"])
    #os.environ.setdefault('IPFS_PATH', str(ipfs_dirrectory))
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    result = subprocess.run(os.getcwd()+'/ipfs.exe init', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=False, startupinfo=si)
    print(result.returncode, result.stdout, result.stderr)
    time.sleep(5)
    #conf_file = Path('~/.ipfs/config').expanduser()
    conf_file = Path(os.environ['IPFS_PATH']+'/config').expanduser()
    shutil.copy2('config', str(conf_file.as_posix())) # complete target filename given

def daemon(ipfs_dirrectory):
    os.environ['IPFS_PATH'] = str(ipfs_dirrectory)
    subprocess.run(os.getcwd()+'/ipfs.exe daemon')

def daemon_background(ipfs_dirrectory):
    os.environ['IPFS_PATH'] = str(ipfs_dirrectory)
    super_su = subprocess.Popen(os.getcwd()+'/ipfs.exe daemon', stdout=PIPE)#, shell=False, startupinfo=si)#, preexec_fn=os.setsid)
    print(super_su.pid)

def kill_daemon_background(pid):
    cmd = 'kill '+str(pid)
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    print(completed.returncode)    

def upload(ipfs_dirrectory,video_name,video_avtor,video_description,video_commercial,video_language,video_pegi,video_tags,video_time,video_file,poster_file,video_resize_width):
    #print(os.environ["IPFS_PATH"])
    #print(Path(os.path.abspath(video_file)).parent)
    name = os.path.basename(video_file)
    path_to_cut = Path(Path(os.path.abspath(video_file)).parent,name+'_cut_video')
    if not os.path.isdir(path_to_cut):
        os.mkdir(path_to_cut)
    #print(path_to_cut)
    
    os.environ['IPFS_PATH'] = str(ipfs_dirrectory)
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    super_su = subprocess.Popen(os.getcwd()+'/ipfs.exe daemon', stdout=PIPE, shell=False, startupinfo=si)#, preexec_fn=os.setsid)    
    #time.sleep(3)

    
    resVideo = []
    resPoster = []
    #resVideo2 = []
    i = 0
    sec = 5

    if video_resize_width == None:
        video = VideoFileClip(video_file)
        s = "/"+name+"_"+f'{i:05}'+".webm"
    else:
        video = VideoFileClip(video_file).fx(resize, width=video_resize) # resize (keep aspect ratio)
        s = "/"+name+"_(width=320)_"+f'{i:05}'+".webm"
    for i in range(math.trunc(video.duration/sec)):
        t1 =i*sec
        t2 = t1+sec
        if t2 > video.duration:
            t2 = video.duration
        #print(f"t1 = {t1}, t2 = {t2}")
        #Обрезаем видео с 15 секунд до его конца округляя длину исходного видео 
        video2 = video.subclip(t1, t2)#cutout(i*sec,(i+1)*sec)
        #Сохранение
        
        video2.write_videofile(str(path_to_cut)+s, codec='libvpx', fps=30, verbose=False, logger=None) # default codec: 'libx264', 24 fps
        with open(str(path_to_cut)+s, 'rb') as filer:
            s_video = filer.read()
        s_video_str = str(base64.b64encode(s_video), encoding='utf-8')

        output2 = ['']
        while output2 == ['']:
            with Popen(os.getcwd()+'/ipfs.exe add '+str(path_to_cut)+s, stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si) as p:
                output, errors = p.communicate()
                output2 = output.decode('utf-8').split(' ')
                print(output.decode('utf-8').split(' '))
                if output.decode('utf-8').split(' ') != ['']:
                    resVideo.append(output.decode('utf-8').split(' ')[1])
                    with Popen(os.getcwd()+'/ipfs.exe pin '+output.decode('utf-8').split(' ')[1], stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si) as p:
                        output1, errors = p.communicate()
                        #print(output.decode('utf-8'))
                
    print(f"Видео разделено на {len(resVideo)} кусочков")

    with Popen(os.getcwd()+'/ipfs.exe add '+poster_file, stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si) as p:
        output, errors = p.communicate()
        #print(output.decode('utf-8').split(' ')[1])
        resPoster.append(output.decode('utf-8').split(' ')[1])

        with Popen(os.getcwd()+'/ipfs.exe pin '+output.decode('utf-8').split(' ')[1], stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si) as p:
            output, errors = p.communicate()
            #print(output.decode('utf-8'))
            
    conf_file = Path(path_to_cut).expanduser()
    shutil.copy2(poster_file, str(conf_file.as_posix())) # complete target filename given

    files = {
            'name_video': video_name,
            'avtor_video': video_avtor,
            'description': video_description,
            'commercial': video_commercial,
            'language': video_language,
            'pegi': video_pegi,
            'tags' : video_tags,
            'datetime_file': video_time, #datetime.strftime(datetime.now(),"%d.%m.%Y_%H.%M.%S.%f"),
            'poster': resPoster,
            'video_file': resVideo
            }

    with open(str(path_to_cut)+'/json_data.json', 'w', encoding='utf-8') as f:
        json.dump(files, f, ensure_ascii=False, indent=4)

    with Popen(os.getcwd()+'/ipfs.exe add '+str(path_to_cut)+'/json_data.json', stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si) as p:
        output, errors = p.communicate()
        print(output.decode('utf-8').split(' ')[1])
        #resPoster.append(output.decode('utf-8'))

        with Popen(os.getcwd()+'/ipfs.exe pin '+output.decode('utf-8').split(' ')[1], stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si) as p:
            output, errors = p.communicate()
            #print(output.decode('utf-8'))
            
    if super_su.pid:
        try:
            p = psutil.Process(super_su.pid)
            p.terminate()
            #print('0-------- Kill Daemon')
        except psutil.NoSuchProcess:
            print({"Result": "oops loose process"})

def download(ipfs_dirrectory,ipfs_id,file_save_dir,file_save_name,file_save_type):
    os.environ['IPFS_PATH'] = str(ipfs_dirrectory)
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    super_su = subprocess.Popen(os.getcwd()+'/ipfs.exe daemon', stdout=PIPE, shell=False, startupinfo=si)#, preexec_fn=os.setsid)    
    #time.sleep(5)

    output2 = b''
    while output2 == b'':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        with Popen(os.getcwd()+'/ipfs.exe cat '+ipfs_id, stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si) as p:
            output, errors = p.communicate()
            output2 = output#.decode('utf-8').split(' ')
    
    if super_su.pid:
        try:
            p = psutil.Process(super_su.pid)
            p.terminate()
        except psutil.NoSuchProcess:
            print({"Result": "oops loose process"})
        
    if file_save_dir != None and file_save_name != None:
        f = io.BytesIO(output)
        FILE_OUTPUT = file_save_dir + "\\" + file_save_name + "." + file_save_type
        out_file = open(FILE_OUTPUT, "wb") # open for [w]riting as [b]inary
        out_file.write(f.read())
        out_file.close()
    print('{"Result": "Ok"}')

def concatenate(ipfs_dirrectory, file_load_dir, file_save_dir, file_save_name, file_save_type):
    all_files = []
    for files in os.listdir(path=file_load_dir):
        filename, file_extension = os.path.splitext(files)
        if file_extension == "."+file_save_type:
            all_files.append(VideoFileClip(file_load_dir+"\\"+files))
            #print(files)
    final_clip = concatenate_videoclips(all_files)
    final_clip.write_videofile(file_save_dir + "\\" + file_save_name + "." + file_save_type)
    print('{"Result": "Ok"}')

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    ipfs_dirrectory = ''
    if namespace.ipfs_dirrectory == None:
        ipfs_dirrectory = '~/.ipfs'
    else:
        ipfs_dirrectory = namespace.ipfs_dirrectory

    if namespace.command == 'ping':
        print(pong())

    if namespace.command == 'init':
        initIPFS(ipfs_dirrectory)

    if namespace.command == 'daemon':
        daemon(ipfs_dirrectory)

    if namespace.command == 'daemon_background':
        daemon_background(ipfs_dirrectory)

    if namespace.command == 'kill_daemon_background':
        kill_daemon_background(int(ipfs_dirrectory))

    if namespace.command == 'download':
        download(ipfs_dirrectory, namespace.ipfs_id, namespace.file_save_dir, namespace.file_save_name, namespace.file_save_type)

    if namespace.command == 'concatenate':
        concatenate(ipfs_dirrectory, namespace.file_load_dir, namespace.file_save_dir, namespace.file_save_name, namespace.file_save_type)

    if namespace.command == 'upload':
        upload(ipfs_dirrectory,
               namespace.video_name, namespace.video_avtor, namespace.video_description,
               namespace.video_commercial, namespace.video_language, namespace.video_pegi,
               namespace.video_tags, namespace.video_time, namespace.video_file, namespace.poster_file,
               namespace.video_resize_width)
