from flask import Flask,  render_template
import cv2
import os
import numpy as np
import base64
import requests

app = Flask(__name__)


URL = "http://192.168.57.11:5000/"

@app.route('/')
def mainfn():
    # sending get request and saving the response as response object
    r = requests.get(url = URL)
    print(r)

if __name__=="__main__":
    app.run(debug=True)

#mainfn()