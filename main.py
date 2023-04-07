""" Main application entry point """
import logging

from flask import Flask, render_template
from functions import get_random_meme_url, get_random_gif_url

logging.basicConfig(level=logging.DEBUG)
logging.debug("APPLICATION STARTUP")

app = Flask(__name__)

@app.route("/")
def index():
    """ Default route handler """
    return render_template("index.html")


@app.route("/meme")
def meme():
    """ Route handler for /meme URL """
    img_url, caption, error_code = get_random_meme_url()
    return render_template("content.html", img_url=img_url, caption=caption, error_code=error_code)

@app.route("/gif")
def gif():
    """ Route handler for /gif URL """
    img_url, caption, error_code = get_random_gif_url()
    return render_template("content.html", img_url=img_url, caption=caption, error_code=error_code)

app.run(host="0.0.0.0", port=8080)
