from flask import Flask, jsonify #, render_template
from flask_restx import Api, Resource

import analyze_youtube_comment.analyze_main as an

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello"

@app.route("/<string:youtube_link>")
def getYoutubeLink(youtube_link):
    videoInfo, commentInfo = an.Train(youtube_link)
    return jsonify({"VideoInfo" : videoInfo, "CommentInfo" : commentInfo})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)