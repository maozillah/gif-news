from flask import Flask, render_template, jsonify, Response, request
import json
from datascraper import get_article_data, localtime
import Queue as queue
import os

app = Flask(__name__)

@app.route("/data")
def data():

	with open('article_meta.json', 'r') as file:
		meta = json.loads(file.read())

	# if current data isn't from today, update it
	if not meta["time_updated"] == localtime:
		get_article_data()

		with open('article_meta.json', 'r') as file:
			new_meta = json.loads(file.read())

		print("updated")
		return jsonify(new_meta)
	else:
		print("no changes")
		return jsonify(meta)

@app.route("/")
def index():
    return render_template("index.html")

def main():
    data()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # main()
