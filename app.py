import glob
import re
import tempfile

import yt_dlp
from flask import Flask, jsonify, request, send_file, send_from_directory

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/download", methods=["POST"])
def download():
    url = (request.get_json(silent=True) or {}).get("url", "")
    if not re.match(r"^https?://(www\.)?instagram\.com/", url):
        return jsonify(error="Invalid link"), 400
    tmp = tempfile.mkdtemp()
    opts = {"outtmpl": tmp + "/%(id)s.%(ext)s", "quiet": True}
    try:
        with yt_dlp.YoutubeDL(opts) as y:
            y.download([url])
        files = glob.glob(tmp + "/*")
        return send_file(files[0], as_attachment=True)
    except Exception:
        return jsonify(error="Download failed"), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
