from flask import Flask

audio_dir = '/audio/'

app = Flask(__name__)

@app.route("/")
@app.route("/")

def index():
	print("tset")

if __name__ == "__main__":
	app.run()