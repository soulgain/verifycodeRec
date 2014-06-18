from flask import Flask
from flask import request
from base64 import b64decode
import os
import sys
import socket
from verifycodeRec import Recognizer

app = Flask(__name__)

rec = Recognizer('template')

@app.route('/verify', methods=['POST'])
def verify():
	cap = request.form['captcha'].replace(' ', '+')
	r = rec.recognizeB64(cap)

	return r


if __name__ == '__main__':
	app.run(host=socket.gethostbyname(socket.gethostname()), debug=True)
