# read from .env file
from dotenv import load_dotenv
load_dotenv()

# import Cloudinary libraries
import cloudinary
from cloudinary import uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url

# import other libraries
import os
import threading
from collections import Counter
from urllib.request import urlopen
import ssl
import json

# get reference to config instance
config = cloudinary.Config()
print("Your Cloudinary Credentials:")
print(config.cloud_name, config.api_key)

from flask import Flask, render_template, request
import json

app = Flask(__name__, static_url_path='/static')


@app.route("/", methods=['GET'])
def index():
  concatenatedOrig=getOriginal("docs/video_features_tutorial/hair.mp4")
  concatenatedURL=concatenated()
  overlayOrig=getOriginal("docs/sdk/go/exercise1")
  overlayURL=overlay()
  backgroundOrig=getOriginal("docs/bluescreen_watches")
  removeBackgroundURL=removeBackground()
  gAutoOrig=getGAutoOrig()
  gAutoURL=gAuto()
  fqAutoURL=fqAuto()
  autoStreamingURL=autoStreaming()      
  return render_template('index.html', concatenatedOrig=concatenatedOrig, 
                         concatenatedURL=concatenatedURL, 
                         overlayOrig=overlayOrig,
                         overlayURL=overlayURL,
                         backgroundOrig=backgroundOrig,
                         removeBackgroundURL=removeBackgroundURL,
                         gAutoOrig=gAutoOrig,
                         gAutoURL=gAutoURL,
                         fqAutoURL=fqAutoURL,
                         autoStreamingURL=autoStreamingURL)

def getOriginal(publicId):
  originalURL=cloudinary.CloudinaryVideo(publicId).build_url()
  return originalURL

def concatenated():
  videoURL = cloudinary.CloudinaryVideo("docs/video_features_tutorial/hair").build_url(transformation=[
    {"aspect_ratio":"4:3", "crop":"fill", "y":"100", "width":"400"},
    {"duration": "5"},
    {"duration": "5", "flags": "splice", "overlay": "video:docs:video_features_tutorial:makeup"},
    {"aspect_ratio": "4:3", "crop": "fill", "y":"130", "width": "400"},
    {"flags": "layer_apply" },
    {"overlay": "video:docs:video_features_tutorial:romeo_and_juliet"},
    {"flags": "layer_apply"},
    {"overlay": "cloudinary_icon"},
    {"width": "40", "x":"10", "y":"10" },
    {"flags": "layer_apply", "gravity": "north_east"},
    {"overlay": {"resource_type": "subtitles", "public_id": "docs/video_features_tutorial/captions.srt"}},
    {"flag": "layer_apply" }])
  return videoURL


def overlay():
  videoURL = cloudinary.CloudinaryVideo("docs/sdk/go/exercise1").build_url(transformation=[
    {"crop":"scale","width":"300"},
    {"overlay": "video:exercise2"},
    {"crop":"fit","width":"80","border":"1px_solid_white"},
    {"flags": "layer_apply","gravity":"north_east","start_offset":"2.0"}
    ])
  return videoURL



def removeBackground():
  videoURL=cloudinary.CloudinaryVideo("docs/sunset_waves").build_url(transformation=[
  {'width': 500, 'crop': "scale"},
  {'overlay': "video:docs:bluescreen_watches"},
  {'flags': "relative", 'width': "0.6", 'crop': "scale"},
  {'color': "#0e80d8", 'effect': "make_transparent:20"},
  {'flags': "layer_apply", 'gravity': "north"},
  {'duration': "15.0"}
  ])
  return videoURL

def getGAutoOrig():
  videoURL = cloudinary.CloudinaryVideo("olympic_gymnast.mp4").build_url(transformation=[
    {"crop":"fill","width":"120","height":"300"}])
  return videoURL

def gAuto():
  videoURL = cloudinary.CloudinaryVideo("olympic_gymnast.mp4").build_url(transformation=[
    {"crop":"fill","gravity":"auto","width":"120","height":"300"}])
  return videoURL

def fqAuto():
  videoURL = cloudinary.CloudinaryVideo("docs/sunglasses").build_url(transformation=[
    {"fetch_format":"auto","quality":"auto"}])
  return videoURL

def autoStreaming():
  videoURL=cloudinary.utils.cloudinary_url("docs/waterfall.m3u8", streaming_profile="auto", resource_type="video")
  return videoURL[0]

if __name__ == "__main__":
  app.run()