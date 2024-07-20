from flask import Flask, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <form action="/download" method="post">
            <label for="url">YouTube Video URL:</label>
            <input type="text" id="url" name="url" required>
            <button type="submit">Download</button>
        </form>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    yt = YouTube(url)

    # Download MP4
    video = yt.streams.get_highest_resolution()
    video_file = video.download()

    # Download MP3
    audio = yt.streams.filter(only_audio=True).first()
    audio_file = audio.download(filename='audio.mp4')

    base, ext = os.path.splitext(audio_file)
    new_file = base + '.mp3'
    os.rename(audio_file, new_file)

    return f'''
        <h3>Downloads:</h3>
        <p><a href="/download-file/{os.path.basename(video_file)}">MP4 Download</a></p>
        <p><a href="/download-file/{os.path.basename(new_file)}">MP3 Download</a></p>
    '''

@app.route('/download-file/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
