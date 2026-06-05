# YouTube Downloader

## Setup (one time)

1. Install Python dependencies:
   ```
   pip install flask yt-dlp flask-cors
   ```

2. Install [FFmpeg](https://ffmpeg.org/download.html) and make sure it's on your PATH.
   - Windows: download a build, extract it, and add the `bin` folder to your system PATH.

## Running

1. Start the backend server:
   ```
   python server.py
   ```

2. Open `index.html` in your browser (double-click it).

3. Paste a YouTube URL, pick MP3 or MP4, and click Download.
