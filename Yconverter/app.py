from flask import Flask, request, jsonify, send_file
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Descargar el video
        yt = YouTube(url)
        stream = yt.streams.filter(only_video=True).first()
        video_file = stream.download(filename='video.mp4')

        # Convertir el video a MP3
        video_clip = VideoFileClip(video_file)
        audio_file = 'audio.mp3'
        video_clip.audio.write_audiofile(audio_file)

        # Limpiar el archivo de video
        os.remove(video_file)

        return send_file(audio_file, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
