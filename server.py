"""
Local backend for the YouTube Downloader UI.
Requires: pip install flask yt-dlp flask-cors
Run with: python server.py
"""

import os
import re
import tempfile
import socket
from flask import Flask, request, send_file, jsonify

app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/')
def index():
    return app.send_static_file('index.html')


def safe_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', '_', name)


@app.route('/download', methods=['POST'])
def download():
    data = request.get_json(force=True)
    url = (data.get('url') or '').strip()
    fmt = (data.get('format') or 'mp3').lower()

    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    if fmt not in ('mp3', 'mp4'):
        return jsonify({'error': 'Format must be mp3 or mp4'}), 400

    tmp_dir = tempfile.mkdtemp()

    if fmt == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
    else:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = safe_filename(info.get('title', 'download'))

        # Find the downloaded file
        files = os.listdir(tmp_dir)
        if not files:
            return jsonify({'error': 'Download produced no output file'}), 500

        filepath = os.path.join(tmp_dir, files[0])
        ext = os.path.splitext(files[0])[1].lstrip('.')
        mimetype = 'audio/mpeg' if ext == 'mp3' else 'video/mp4'
        download_name = f'{title}.{ext}'

        response = send_file(
            filepath,
            mimetype=mimetype,
            as_attachment=True,
            download_name=download_name,
        )
        response.headers['X-Filename'] = download_name
        response.headers['Access-Control-Expose-Headers'] = 'X-Filename'
        return response
    except yt_dlp.utils.DownloadError as e:
        msg = str(e)
        if 'Private video' in msg:
            return jsonify({'error': 'This video is private'}), 400
        if 'age' in msg.lower():
            return jsonify({'error': 'Age-restricted video — cannot download'}), 400
        return jsonify({'error': f'Download failed: {msg}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    local_ip = socket.gethostbyname(socket.gethostname())
    print(f'YouTube Downloader server running at:')
    print(f'  Local:   http://localhost:5000')
    print(f'  Network: http://{local_ip}:5000  <-- use this on mobile')
    app.run(host='0.0.0.0', port=5000, debug=False)
