from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from pytube import YouTube
import os
import time

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'arnab' or request.form['password'] != 'admin':
            error = "Invalid credentials. Please try again."
        else:
            return redirect(url_for('download'))

    return render_template('login.html', error=error)

@app.route('/download', methods=['GET', 'POST'])
def download():

    """ actual download logic goes down here
        the POST request gets the given link and puts it 
        throught the program logic to download the youtube video 
        in the temporary folder first and then uses send_from_directory to
        download the video"""
    

    message = None
    if request.method == 'POST':
        link = request.form['videolink']
        message = "Dowloading Video"
        video_download(link)
        
        file_path = '/home/arnab/PythonProjects/Downloader/temporary'
        file_name = os.listdir(file_path)
        if len(os.listdir(file_path)) != 0:
            print('inside download for user function')
            return send_from_directory(file_path, file_name[0], as_attachment=True)
    return render_template('download.html', message=message)


def video_download(linkurl, videoPath='/home/arnab/PythonProjects/Downloader/temporary'):
    """ download logic for the youtube video 
        takes in two parameters linkurl and videoPath 
        uses pytube youtube api for downloading the file
        to the temporary folder"""
    if os.path.exists(videoPath) and len(os.listdir(videoPath)) != 0:
        print('Folder is not empty... deleting contents of folder')
        for file in os.listdir(videoPath):
            file_path = os.path.join(videoPath, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    else:
        print('Folder is empty we can download the file')

     print('Starting file download')

    yt = YouTube(linkurl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    yt.download(videoPath)
    print('Download Complete')


# def download_for_user():
#     """ downloads the file for the user"""
#     file_path = '/home/arnab/PythonProjects/Downloader/temporary'
#     file_name = os.listdir(file_path)
#     print('inside download for user function')
#     return send_from_directory(file_path, file_name[0], as_attachment=True)