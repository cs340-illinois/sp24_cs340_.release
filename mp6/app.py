from flask import Flask, render_template, request, jsonify
import os
import requests
from datetime import datetime, timedelta, time

app = Flask(__name__)


# Route for "/" (frontend):
@app.route('/')
def index():
  return render_template("index.html")


# Route for "/weather" (middleware):
@app.route('/weather', methods=["POST"])
def POST_weather():
  course = request.form["course"]

  # ...
  return "Not Implemented", 501


@app.route('/weatherCache')
def get_cached_weather():
  # check if the cache is valid and return the weather data as stored in the cache
  # if cache is not valid, return empty json
  
  # ...
  return "Not Implemented", 501
