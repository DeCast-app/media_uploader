#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QLabel, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui

"""
from PyQt5.QtCore import QUrl, QFile, QIODevice,  QBuffer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlaylist, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout
"""

from PyQt5 import QtMultimediaWidgets

import subprocess
from datetime import datetime, timedelta
from subprocess import Popen, PIPE, run
from threading import Thread
import time
import json
import base64
import shutil
import io
import PIL.Image as Image
import PIL.ImageQt as ImageQt
import cv2
import numpy as np
from skimage.io import imread, imsave
import os

from pathlib import Path
import signal
import psutil

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

def startA(a1,a2):
    if os.path.isfile(Path('~/.ipfs/config').expanduser()) == False:
        print('0-------- Init')
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = run(os.getcwd()+'/ipfs.exe init', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=False, startupinfo=si)
        print(result.returncode, result.stdout, result.stderr)
        time.sleep(5)
        print('1-------- Change config')
        conf_file = Path('~/.ipfs/config').expanduser()
        shutil.copy2('config', str(conf_file.as_posix())) # complete target filename given

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.video_window = VideoWindow()
        self.btnVideo = QPushButton('Play Video', self)
        self.btnVideo.move(-20, -20)
        self.btnVideo.setToolTip('Click for Play Video')
        self.btnVideo.clicked[bool].connect(self.video_window)

        self.poster_window = PosterWindow()
        self.btnPoster = QPushButton('Show Poster', self)
        self.btnPoster.move(-20, -20)
        self.btnPoster.setToolTip('Click for Show Poster')
        self.btnPoster.clicked[bool].connect(self.poster_window)
        
        ###--------------------------------------
        #Виджет CheckBox:
        #cb = QCheckBox('Show title', self)
        #cb.move(20, 20)
        #cb.toggle()
        #cb.stateChanged.connect(self.changeTitle)
        ###--------------------------------------
        """
        self.col = QColor(0, 0, 0)

        redb = QPushButton('Red', self)
        redb.setCheckable(True)
        redb.move(10, 10)
        redb.clicked[bool].connect(self.setColor)

        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)
        greenb.clicked[bool].connect(self.setColor)

        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)
        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
        """
        # informations
        info = "QmcumKT2TFivF78VUSgS4vQCMKqVEo2Q3iryyFiparbfdF"
        # setting  the geometry of window
        self.setGeometry(0, 0, 700, 720)

        self.pixmap = QPixmap()
        
        # creating a label widget
        self.label_2 = QLineEdit(info, self) #QLabel(info, self)
        # moving position
        self.label_2.move(0, 0)
        # resizing the widget
        self.label_2.resize(700, 20)
        # setting up border
        self.label_2.setStyleSheet("border: 1px solid black; background-color: lightgreen")


        # creating a label widget
        self.label_1 = QLabel('', self)
        # moving position
        self.label_1.move(0, 0)
        # resizing the widget
        self.label_1.resize(0, 0)
        # setting up border
        self.label_1.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        
        self.btn = QPushButton('Get Image', self)
        self.btn.move(-100, -100)
        self.btn.clicked.connect(self.doAction)

        # creating a label widget
        self.label_StructureNameAdd = QLineEdit('Name: <Change all text>', self)
        # moving position
        self.label_StructureNameAdd.move(200, 25)
        # resizing the widget
        self.label_StructureNameAdd.resize(400, 20)
        # setting up border
        self.label_StructureNameAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureAutorAdd = QLineEdit('Autor: <Change all text>', self)
        # moving position
        self.label_StructureAutorAdd.move(200, 50)
        # resizing the widget
        self.label_StructureAutorAdd.resize(400, 20)
        # setting up border
        self.label_StructureAutorAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureDescriptionAdd = QLineEdit('Description: <Change all text>', self)
        # moving position
        self.label_StructureDescriptionAdd.move(200, 75)
        # resizing the widget
        self.label_StructureDescriptionAdd.resize(400, 20)
        # setting up border
        self.label_StructureDescriptionAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureCommercialAdd = QLineEdit('Commercial: <Change all text>', self)
        # moving position
        self.label_StructureCommercialAdd.move(200, 100)
        # resizing the widget
        self.label_StructureCommercialAdd.resize(400, 20)
        # setting up border
        self.label_StructureCommercialAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureLanguageAdd = QLineEdit('Language: <Change all text>', self)
        # moving position
        self.label_StructureLanguageAdd.move(200, 125)
        # resizing the widget
        self.label_StructureLanguageAdd.resize(400, 20)
        # setting up border
        self.label_StructureLanguageAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructurePegiAdd = QLineEdit('Pegi: <Change all text>', self)
        # moving position
        self.label_StructurePegiAdd.move(200, 150)
        # resizing the widget
        self.label_StructurePegiAdd.resize(400, 20)
        # setting up border
        self.label_StructurePegiAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureTagsAdd = QLineEdit('Tags: <Change all text>', self)
        # moving position
        self.label_StructureTagsAdd.move(200, 175)
        # resizing the widget
        self.label_StructureTagsAdd.resize(400, 20)
        # setting up border
        self.label_StructureTagsAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        ##----------------------------------------------------------------------
        self.btnOpenFilePoster = QPushButton('Open Poster File', self)
        self.btnOpenFilePoster.move(200, 200)
        self.btnOpenFilePoster.resize(200,25)
        self.btnOpenFilePoster.clicked.connect(self.doActionOpenFilePoster)

        # creating a label widget
        self.label_OpenFilePoster = QLabel('Click on button "Open Poster File"', self)
        # moving position
        self.label_OpenFilePoster.move(200, 225)
        # resizing the widget
        self.label_OpenFilePoster.resize(400, 20)
        # setting up border
        self.label_OpenFilePoster.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        ##----------------------------------------------------------------------------------------

        ##----------------------------------------------------------------------
        self.btnOpenFileVideo = QPushButton('Open Video File', self)
        self.btnOpenFileVideo.move(200, 250)
        self.btnOpenFileVideo.resize(200,25)
        self.btnOpenFileVideo.clicked.connect(self.doActionOpenFileVideo)

        # creating a label widget
        self.label_OpenFileVideo = QLabel('Click on button "Open Video File"', self)
        # moving position
        self.label_OpenFileVideo.move(200, 275)
        # resizing the widget
        self.label_OpenFileVideo.resize(400, 20)
        # setting up border
        self.label_OpenFileVideo.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        ##----------------------------------------------------------------------------------------

        self.btnUpload = QPushButton('Upload', self)
        self.btnUpload.move(200, 300)
        self.btnUpload.resize(200,25)
        self.btnUpload.clicked.connect(self.doActionUpload)

        # creating a label widget
        self.label_ResultPosterAdd = QLineEdit('Result add Poster to IPFS', self)
        # moving position
        self.label_ResultPosterAdd.move(200, 325)
        # resizing the widget
        self.label_ResultPosterAdd.resize(400, 20)
        # setting up border
        self.label_ResultPosterAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_ResultVideoAdd = QLineEdit('Result add Video to IPFS', self)
        # moving position
        self.label_ResultVideoAdd.move(200, 350)
        # resizing the widget
        self.label_ResultVideoAdd.resize(400, 20)
        # setting up border
        self.label_ResultVideoAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_ResultStructureAdd = QLineEdit('Result add Structure to IPFS', self)
        # moving position
        self.label_ResultStructureAdd.move(200, 375)
        # resizing the widget
        self.label_ResultStructureAdd.resize(400, 20)
        # setting up border
        self.label_ResultStructureAdd.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        self.btnGetUploadedStructure = QPushButton('Get Uploaded Structure', self)
        self.btnGetUploadedStructure.move(200, 430)
        self.btnGetUploadedStructure.resize(200,25)
        self.btnGetUploadedStructure.clicked.connect(self.doActionGetUploadedStructure)

        # creating a label widget
        self.label_StructureName = QLineEdit('Structure Name: ', self)
        # moving position
        self.label_StructureName.move(200, 455)
        # resizing the widget
        self.label_StructureName.resize(400, 20)
        # setting up border
        self.label_StructureName.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureAutor = QLineEdit('Structure Autor: ', self)
        # moving position
        self.label_StructureAutor.move(200, 480)
        # resizing the widget
        self.label_StructureAutor.resize(400, 20)
        # setting up border
        self.label_StructureAutor.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureDescription = QLineEdit('Structure Description: ', self)
        # moving position
        self.label_StructureDescription.move(200, 505)
        # resizing the widget
        self.label_StructureDescription.resize(400, 20)
        # setting up border
        self.label_StructureDescription.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureCommercial = QLineEdit('Structure Commercial: ', self)
        # moving position
        self.label_StructureCommercial.move(200, 530)
        # resizing the widget
        self.label_StructureCommercial.resize(400, 20)
        # setting up border
        self.label_StructureCommercial.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureLanguage = QLineEdit('Structure Language: ', self)
        # moving position
        self.label_StructureLanguage.move(200, 555)
        # resizing the widget
        self.label_StructureLanguage.resize(400, 20)
        # setting up border
        self.label_StructureLanguage.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructurePegi = QLineEdit('Structure Pegi: ', self)
        # moving position
        self.label_StructurePegi.move(200, 580)
        # resizing the widget
        self.label_StructurePegi.resize(400, 20)
        # setting up border
        self.label_StructurePegi.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureTags = QLineEdit('Structure Tags: ', self)
        # moving position
        self.label_StructureTags.move(200, 605)
        # resizing the widget
        self.label_StructureTags.resize(400, 20)
        # setting up border
        self.label_StructureTags.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructurePoster_cid = QLineEdit('Structure Poster_cid: ', self)
        # moving position
        self.label_StructurePoster_cid.move(200, 630)
        # resizing the widget
        self.label_StructurePoster_cid.resize(400, 20)
        # setting up border
        self.label_StructurePoster_cid.setStyleSheet("border: 1px solid black; background-color: lightgreen")

        # creating a label widget
        self.label_StructureVideo_cid = QLineEdit('Structure Video_cid: ', self)
        # moving position
        self.label_StructureVideo_cid.move(200, 655)
        # resizing the widget
        self.label_StructureVideo_cid.resize(400, 20)
        # setting up border
        self.label_StructureVideo_cid.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        
        self.setWindowTitle('HoloRec Windows Desktop version - Initializing IPFS.......')
        self.setWindowIcon(QIcon('web.png'))

        self.show()
        
        if os.path.isfile(Path('~/.ipfs/config').expanduser()) == False:
            startA(100,150)
        self.btn.move(5, 25)
        self.setWindowTitle('HoloRec Windows Desktop version - IPFS Daemon Init')
        #print('5-------- End')
        
    """    
    def download_file(user0):
        print("00000000")
        client = ipfshttpclient.connect('/dns/192.168.99.100/tcp/5001/http')  # Connects to: /dns/localhost/tcp/5001/http
        print("222222222222")
        cc = client.cat(user0) #QmbvrHYWXAU1BuxMPNRtfeF4DS2oPmo5hat7ocqAkNPr74  #'QmNoXmoRbXNNMUWEU4DBPUZgCPH4MGsktFM1KPvewAWdbv')
        client.close()
        s = str(base64.b64encode(cc), encoding='utf-8')
        return {"Result":"OK","type":str(type(cc)),"cid_video":s}
    """
    def doAction(self):
        self.btn.move(-100, -100)
        
        self.btnOpenFilePoster.move(-300,-300)
        self.label_OpenFilePoster.move(-300,-300)
        self.btnOpenFileVideo.move(-300,-300)
        self.label_OpenFileVideo.move(-300,-300)
        
        self.btnUpload.move(-300,-300)
        self.label_ResultPosterAdd.move(-300,-300)
        self.label_ResultVideoAdd.move(-300,-300)
        self.label_ResultStructureAdd.move(-300,-300)
        
        self.btnGetUploadedStructure.move(-300,-300)
        self.label_StructureName.move(-300,-300)
        self.label_StructureAutor.move(-300,-300)
        self.label_StructureDescription.move(-300,-300)
        self.label_StructurePoster_cid.move(-300,-300)
        self.label_StructureVideo_cid.move(-300,-300)
        
        self.setWindowTitle('HoloRec Windows Desktop version - Download Image from IPFS.......')
        self.repaint()
        
        print('0-------- Start Daemon')
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        super_su = subprocess.Popen(os.getcwd()+'/ipfs.exe daemon', stdout=PIPE, shell=False, startupinfo=si)#, preexec_fn=os.setsid)
        print('1-------- Ok')
        time.sleep(5)

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        with Popen(os.getcwd()+'/ipfs.exe cat '+self.label_2.text(), stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si) as p:
            print('ttttt')
            output, errors = p.communicate()
            print(type(output))
            f = open('1111.jpg', 'wb')
            f.write(output)
            f.close()
            img = Image.open(io.BytesIO(output))
            imgB0 = np.asarray(img)
            # loading image
            qtImage = ImageQt.ImageQt(img)
            self.pixmap = QPixmap.fromImage(qtImage)#QPixmap('1111.jpg')
            self.pixmap_resized = self.pixmap.scaled(700, 700,QtCore.Qt.KeepAspectRatio)
            self.label_1.move(0, 20)
            # adding image to label
            self.label_1.setPixmap(self.pixmap_resized)
            # Optional, resize label to image size
            self.label_1.resize(self.pixmap_resized.width(),self.pixmap_resized.height())
        
        print('2-------- Kill Daemon')
        #subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=super_su.pid))
        if super_su.pid:
            try:
                p = psutil.Process(super_su.pid)
                p.terminate()
            except psutil.NoSuchProcess:
                print ('oops loose process')
        #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Отправляет сигнал всем группам процессов
        
        self.btn.move(-200, -100)
        self.setWindowTitle('HoloRec Windows Desktop version - Image OK!')
        print('3-------- Ok')

    def doActionGetUploadedStructure(self):
        self.setWindowTitle('HoloRec Windows Desktop version - Download Structure from IPFS.......')
        self.repaint()

        print('0-------- Start Daemon')
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        super_su = subprocess.Popen(os.getcwd()+'/ipfs.exe daemon', stdout=PIPE, shell=False, startupinfo=si)#, preexec_fn=os.setsid)
        print('1-------- Ok')
        time.sleep(5)

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = Popen(os.getcwd()+'/ipfs.exe cat '+self.label_ResultStructureAdd.text(), stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si)
        output, errors = p.communicate()
        print(type(output))
        print(output.decode('utf-8'))
        a = output.decode('utf-8')
        b = a.replace('\\','')[1:len(a)-2]
        print(b[:len(b)-1])
        jj = json.loads(b[:len(b)-1])
        #jj = json.loads(a)
        #print(a.replace('\"','"')[1:len(a)-1])
        self.label_StructureName.setText("Название видео = "+jj["name_video"])
        self.label_StructureAutor.setText("Автор видео = "+jj["avtor_video"])
        self.label_StructureDescription.setText("Описание видео = "+jj["description"])
        self.label_StructureCommercial.setText("Реклама = "+jj["commercial"])
        self.label_StructureLanguage.setText("Язык = "+jj["language"])
        self.label_StructurePegi.setText("Возрастной ценз = "+jj["pegi"])
        self.label_StructureTags.setText("Тэги = "+jj["tags"])
        self.label_StructurePoster_cid.setText(jj["poster"])
        self.label_StructureVideo_cid.setText(jj["video_file"])
        self.btnVideo.move(200, 680)
        self.btnPoster.move(410, 680)
        
        print("Название видео = "+jj["name_video"])
        print("Автор видео = "+jj["avtor_video"])
        print("Описание видео = "+jj["description"])
        print("Видео = "+jj["video_file"])
        print("Постер = "+jj["poster"])

        print('2-------- Kill Daemon')
        #subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=super_su.pid))
        if super_su.pid:
            try:
                p = psutil.Process(super_su.pid)
                p.terminate()
            except psutil.NoSuchProcess:
                print ('oops loose process')
        #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Отправляет сигнал всем группам процессов

        self.setWindowTitle('HoloRec Windows Desktop version - Download Structure OK!')
        print('3-------- Ok')
        
        """"
        self.label_2.setText(jj["poster"])
        self.repaint()
        self.btn.click()

        #
        self.btnOpenFilePoster.move(-300,-300)
        self.label_OpenFilePoster.move(-300,-300)
        self.btnOpenFileVideo.move(-300,-300)
        self.label_OpenFileVideo.move(-300,-300)
        
        self.btnUpload.move(-300,-300)
        self.label_ResultPosterAdd.move(-300,-300)
        self.label_ResultVideoAdd.move(-300,-300)
        self.label_ResultStructureAdd.move(-300,-300)
        
        self.btnGetUploadedStructure.move(-300,-300)
        self.label_StructureName.move(-300,-300)
        self.label_StructureAutor.move(-300,-300)
        self.label_StructureDescription.move(-300,-300)
        self.label_StructurePoster_cid.move(-300,-300)
        self.label_StructureVideo_cid.move(-300,-300)

        self.repaint()
        """
        
    def doActionOpenFilePoster(self):
        wb_patch = QFileDialog.getOpenFileName()[0]
        print(wb_patch)
        self.label_OpenFilePoster.setText(wb_patch)

    def doActionOpenFileVideo(self):
        wb_patch = QFileDialog.getOpenFileName()[0]
        print(wb_patch)
        self.label_OpenFileVideo.setText(wb_patch)
        
        
    def doActionUpload(self):
        wb_patchPoster = self.label_OpenFilePoster.text()
        wb_patchVideo = self.label_OpenFileVideo.text()

        filer = open(wb_patchVideo, 'rb')
        s_video = filer.read()
        filer.close()

        filer = open(wb_patchPoster, 'rb')
        s_poster = filer.read()
        filer.close()

        print('-------')

        print(wb_patchPoster)
        print(wb_patchVideo)
        
        self.setWindowTitle('HoloRec Windows Desktop version - Starting Daemon.......')
        self.repaint()
        
        print('0-------- Start Daemon')
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        super_su = subprocess.Popen(os.getcwd()+'/ipfs.exe daemon', stdout=PIPE, shell=False, startupinfo=si)#, preexec_fn=os.setsid)
        print('1-------- Ok')
        time.sleep(5)

        self.setWindowTitle('HoloRec Windows Desktop version - Upload PosterFile to IPFS.......')
        self.repaint()

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = Popen(os.getcwd()+'/ipfs.exe add '+wb_patchPoster, stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si)
        output, errors = p.communicate()
        print(output.decode('utf-8'))
        self.label_ResultPosterAdd.setText(output.decode('utf-8').split(' ')[1])
        poster_cid = output.decode('utf-8').split(' ')[1]
        print(output.decode('utf-8').split(' ')[1])

        self.setWindowTitle('HoloRec Windows Desktop version - Upload VideoFile to IPFS.......')
        self.repaint()

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = Popen(os.getcwd()+'/ipfs.exe add '+wb_patchVideo, stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si)
        output, errors = p.communicate()
        print(output.decode('utf-8'))
        self.label_ResultVideoAdd.setText(output.decode('utf-8').split(' ')[1])
        video_cid = output.decode('utf-8').split(' ')[1]
        print(output.decode('utf-8').split(' ')[1])

        files = {
            'name_video': self.label_StructureNameAdd.text(),
            'avtor_video': self.label_StructureAutorAdd.text(),
            'description': self.label_StructureDescriptionAdd.text(),
            'commercial': self.label_StructureCommercialAdd.text(),
            'language': self.label_StructureLanguageAdd.text(),
            'pegi': self.label_StructurePegiAdd.text(),
            'tags' : self.label_StructureTagsAdd.text(),
            'datetime_file': datetime.strftime(datetime.now(),"%d.%m.%Y_%H.%M.%S.%f"),
            'poster': poster_cid,
            'video_file': video_cid
            }
        json_files = json.dumps(files)
        outfile = open('json_data.json', 'w')
        json.dump(json_files, outfile)
        outfile.close()

        self.setWindowTitle('HoloRec Windows Desktop version - Upload Structure to IPFS.......')
        self.repaint()

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = Popen(os.getcwd()+'/ipfs.exe add '+'json_data.json', stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si)
        output, errors = p.communicate()
        print(output.decode('utf-8'))
        self.label_ResultStructureAdd.setText(output.decode('utf-8').split(' ')[1])
        structure_cid = output.decode('utf-8').split(' ')[1]
        print(output.decode('utf-8').split(' ')[1])


        #загружаем загруженный кусок
        
        

        print('2-------- Kill Daemon')
        #subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=super_su.pid))
        if super_su.pid:
            try:
                p = psutil.Process(super_su.pid)
                p.terminate()
            except psutil.NoSuchProcess:
                print ('oops loose process')
        #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Отправляет сигнал всем группам процессов
        
        #self.btn.move(-200, -100)
        self.setWindowTitle('HoloRec Windows Desktop version - Upload Structure OK!')
        print('3-------- Ok')
        

        
"""
    def setColor(self, pressed):
        source = self.sender()
        if pressed:
            val = 255
        else: val = 0
        if source.text() == "Red":
            self.col.setRed(val)
        elif source.text() == "Green":
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)
        self.square.setStyleSheet("QFrame { background-color: %s }" % self.col.name())
"""

class PosterWindow(QMainWindow):
    def __init__(self):
        super(PosterWindow, self).__init__()

    def __call__(self, *args, **kwargs):
        self.setWindowTitle("Poster")

        self.setGeometry(0, 0, 700, 720)
        self.pixmap2 = QPixmap()

        # creating a label widget
        self.label_1p = QLabel('', self)
        # moving position
        self.label_1p.move(0, 0)
        # resizing the widget
        self.label_1p.resize(0, 0)
        # setting up border
        self.label_1p.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        
        self.show()

        print(ex.label_StructurePoster_cid.text())

        self.setWindowTitle('HoloRec Windows Desktop version - Download Poster from IPFS.......')
        self.repaint()
        
        print('0-------- Start Daemon')
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        super_su = subprocess.Popen(os.getcwd()+'/ipfs.exe daemon', stdout=PIPE, shell=False, startupinfo=si)#, preexec_fn=os.setsid)
        print('1-------- Ok')
        time.sleep(5)

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = Popen(os.getcwd()+'/ipfs.exe cat '+ex.label_StructurePoster_cid.text(), stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si)
        output, errors = p.communicate()
        print(type(output))
        f = open('poster_cool.jpg', 'wb')
        f.write(output)
        f.close()
        
            
        print('2-------- Kill Daemon')
        #subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=super_su.pid))
        if super_su.pid:
            try:
                p = psutil.Process(super_su.pid)
                p.terminate()
            except psutil.NoSuchProcess:
                print ('oops loose process')
        #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Отправляет сигнал всем группам процессов

        img = Image.open(io.BytesIO(output))        
        #imgB0 = np.asarray(img)
        # loading image
        qtImage2 = ImageQt.ImageQt(img)
        print('55555')
        pixmap2 = QPixmap.fromImage(qtImage2)#QPixmap('1111.jpg')
        print('666')
        pixmap_resized2 = pixmap2.scaled(700, 700,QtCore.Qt.KeepAspectRatio)
        print('777777777')
        self.label_1p.move(0, 20)
        # adding image to label
        self.label_1p.setPixmap(pixmap_resized2)
        # Optional, resize label to image size
        self.label_1p.resize(pixmap_resized2.width(),pixmap_resized2.height())

        self.setWindowTitle('HoloRec Windows Desktop version - Download Poster from IPFS OK!')
        self.repaint()



class VideoWindow(QMainWindow):
    def __init__(self):
        super(VideoWindow, self).__init__()

    def __call__(self, *args, **kwargs):
        self.setGeometry(0, 0, 700, 720)
        self.setWindowTitle("Video")
        self.show()

        print(ex.label_StructureVideo_cid.text())

        self.setWindowTitle('HoloRec Windows Desktop version - Download Video from IPFS.......')
        self.repaint()
        
        print('0-------- Start Daemon')
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        super_su = subprocess.Popen(os.getcwd()+'/ipfs.exe daemon', stdout=PIPE, shell=False, startupinfo=si)#, preexec_fn=os.setsid)
        print('1-------- Ok')
        time.sleep(5)

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = Popen(os.getcwd()+'/ipfs.exe cat '+ex.label_StructureVideo_cid.text(), stdout=PIPE, stderr=PIPE, shell=False, startupinfo=si)
        output, errors = p.communicate()
        print(type(output))
        f = open('video_cool.mp4', 'wb')
        f.write(output)
        f.close()
            
        print('2-------- Kill Daemon')
        #subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=super_su.pid))
        if super_su.pid:
            try:
                p = psutil.Process(super_su.pid)
                p.terminate()
            except psutil.NoSuchProcess:
                print ('oops loose process')
        #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Отправляет сигнал всем группам процессов

        self.setWindowTitle('HoloRec Windows Desktop version - Download Video from IPFS OK!')
        self.repaint()

        self.player = QtMultimedia.QMediaPlayer(flags=QtMultimedia.QMediaPlayer.VideoSurface)
        self.buff = QtCore.QBuffer()
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.setCentralWidget(self.video_widget)
        self.player.setVideoOutput(self.video_widget)
        self.resize(640, 480)
        self.repaint()

        #filename = os.path.join(CURRENT_DIR, "video_cool.mp4")
        #self.load_from_file(filename)
        ba = QtCore.QByteArray(output)
        self.buff.setData(ba)
        print('SetData OK')
        self.buff.open(QtCore.QIODevice.ReadOnly)
        print('OpenData OK')
        self.player.setMedia(QtMultimedia.QMediaContent(), self.buff)
        print('SetMedia OK')
        self.player.play()
        print('StartPlay OK')


        self.setWindowTitle('HoloRec Windows Desktop version - Start playing video!')
        self.repaint()

    def closeEvent(self, event):
        self.player.pause()
        # do stuff
        """
        if can_exit:
            self.player.pause()
            event.accept() # let the window close
        else:
            event.ignore()
        """

    def load_from_file(self, filename):
        f = QtCore.QFile(filename)
        if f.open(QtCore.QIODevice.ReadOnly):
            ba = f.readAll()
            print('Read OK')
            self.load_from_data(ba)

    def load_from_data(self, data):
        ba = QtCore.QByteArray(data)
        self.buff.setData(ba)
        print('SetData OK')
        self.buff.open(QtCore.QIODevice.ReadOnly)
        print('OpenData OK')
        self.player.setMedia(QtMultimedia.QMediaContent(), self.buff)
        print('SetMedia OK')
        self.player.play()
        print('StartPlay OK')


        """
        # Define file variables
        self.playlist_files = ['video_cool.mp4', 'video_cool.mp4']

        # Define the QT-specific variables we're going to use
        self.vertical_box_layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.video_frame = QVideoWidget()

        # Define the media player related information
        self.playlist = QMediaPlaylist()
        self.video_player = QMediaPlayer(flags=QMediaPlayer.VideoSurface)
        self.buffer = QBuffer()

        # Connect error & media status signalsto functions that print those signals to stdout
        self.video_player.error.connect(self.print_media_player_error)
        self.video_player.mediaStatusChanged.connect(self.print_media_player_status)


        # Create the user interface, set up the player, and play the 2 videos
        self.create_user_interface()
        self.video_player_setup()
        """
        
    """
    def print_media_player_error(self, value):
        #Prints any errors media player encounters
        print(f"Error: {value}")

    def print_media_player_status(self, value):
        #Prints any status changes to media player
        print(f"Status: {value}")

    def video_player_setup(self):
        #Sets media list for the player and then sets output to the video frame
        self.video_player.setVideoOutput(self.video_frame)

        self.set_buffer()
        # self.set_playlist()
        self.video_player.play()

    def set_playlist(self):
        #Opens a single video file, puts it into a playlist which is read by the QMediaPlayer
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath(self.playlist_files[0]))))
        self.playlist.setCurrentIndex(0)
        self.video_player.setPlaylist(self.playlist)

    def set_buffer(self):
        #Opens a single video file and writes it to a buffer to be read by QMediaPlayer
        media_file_name = os.path.abspath(self.playlist_files[0])
        media_file = QFile(media_file_name)
        media_file.open(QIODevice.ReadOnly)
        print(f"The size of buffer before adding the byte_array is: {self.buffer.size()}")
        self.byte_array = media_file.readAll()
        self.buffer.setData(self.byte_array)
        self.buffer.open(QIODevice.ReadOnly)
        print(f"The size of buffer after adding the byte_array is: {self.buffer.size()}")
        self.video_player.setMedia(QMediaContent(), self.buffer)

    def create_user_interface(self):
        #Create a 1280x720 UI consisting of a vertical layout, central widget, and QLabel
        self.setCentralWidget(self.central_widget)
        self.vertical_box_layout.addWidget(self.video_frame)
        self.central_widget.setLayout(self.vertical_box_layout)

        self.resize(1280, 720)
    """


        

if __name__ == '__main__':
    #if os.path.isfile(Path('~/.ipfs/config').expanduser()) == False:
        #print("1111111")
        #t1 = Thread(target=startA,args=(100,150))
        #t1.start()
    #    startA(100,150)

    app = QApplication(sys.argv)
    ex = Example()

    #ex.btn.move(200, 100)
    #ex.setWindowTitle('HoloRec Windows Desktop version - Daemon Init')
    #print('5-------- End')
    
    sys.exit(app.exec_())

    
