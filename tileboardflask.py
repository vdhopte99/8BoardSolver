#!/usr/bin/env python

#------------------------------------------------------------------------
# 8Board.py
# Author: Vedant Dhopte
#------------------------------------------------------------------------

from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from sys import stderr

#------------------------------------------------------------------------

app = Flask(__name__, template_folder='webpages')

#------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def home():
    html = render_template('index.html')
    response = make_response(html)
    return response