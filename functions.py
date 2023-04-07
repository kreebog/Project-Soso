""" A colleciton of simple functions that scrape content from different web sites"""

import logging
import json
import random
import requests

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logging.debug('APPLICATION STARTUP')

def get_random_gif_url():
    """Returns the url to a random .gif from the imgur homepage. """

    # request the imgur home page
    response = request_url('https://boards.4channel.org/wsg/')

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the GIFs on the page
    gifs = soup.find_all('img')

    # Choose a random GIF URL from the list
    try:
        gif_url = 'https:' + random.choice(gifs)['src']
    except IndexError as error:
        logging.error('get_random_gif_url() : ERROR, %s', str(error))
        logging.error('get_random_gif_url() : ERROR, %s', str(response.content))
        return '/static/sad.jpg', 'No img tags found?', response.status_code

    return gif_url, 'An image', None


def get_random_meme_url():
    """Returns the url to a random image from some broken meme service scraping a subreddit. """
    error_code = None

    response = request_url('https://meme-api.herokuapp.com/gimme')
    if response.status_code != 200:
        meme_large = '/static/sad.jpg'
        subreddit = 'My Broken Heart'
        error_code = response.status_code
        return meme_large, subreddit, error_code
    else:
        logging.debug('RAW RESPONSE --> %s', response.text)
        json_data = json.loads(response.text)

        meme_large = json_data['preview'][-2]
        subreddit = json_data['subreddit']

        return meme_large, subreddit, error_code

def request_url(url):
    """ Requests a url and returns the response object """
    logging.debug('request_url("%s") : ENTERING', url)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx responses
    except requests.exceptions.RequestException as error:
        logging.error('request_url("%s") : ERROR, %s', url, str(error))
        return None

    logging.debug('request_url("%s") : SUCCESS, %d bytes returned.', url, len(response.content))

    return response
