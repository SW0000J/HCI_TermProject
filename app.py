from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def putYoutubeLink():
    return render_template("put_youtube_link.html")

@app.route("/user/<user_name>/<int:user_id>")
def user(user_name, user_id):
    return f"Hello, {user_name}({user_id})"

if __name__ == "__main__":
    app.run(debug=True)