from crypt import methods
from stringprep import in_table_c11
import flask
import friends_map

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        if flask.request.form.get("bar"):
            friend_acc = flask.request.form.get("twitter_acc")
            return super_map(friend_acc)
    return flask.render_template("friends_start.html")

@app.route("/friends_map", methods = ["GET", "POST"])
def super_map(twitter_acc):
    friends_map.create_friends_map(friends_map.get_followings_data(twitter_acc))
    return flask.render_template('friends.html')

if __name__=="__main__":
    app.run(host="127.0.0.1", port=8080)