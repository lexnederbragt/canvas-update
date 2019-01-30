import configparser
import os, sys
import re
from canvasapi import Canvas
from canvasapi import page

def split_url(url):
    """
    Retrieve API url, course id and page name from full url:
     <https://canvas.instance.com>/courses/<course_id>/pages/<page_name>
    """
    none, API_URL, course_id, page_name, none = re.split('(.*)/courses/(.*)/pages/(.*)', url)
    return API_URL, course_id, page_name

def get_API(config_file_name, API_URL):
    """
    Parse config file
    Extract correct API key
    """

    config = configparser.ConfigParser()
    result = config.read_file(open(os.path.expanduser(config_file_name)))
    if result == []:
        sys.exit("Error: could not open config file or config file was empty or malformed: " + config_file)
    # Canvas API key
    try:
        API_KEY = config[API_URL]['api_key']
    except KeyError:
        sys.exit("Error: could not find the entry for 'api-key' in the Canvas instance '%s' section of the config file '%s'." % (API_URL, config_file_name))

    return API_KEY

def get_course(url, config_file):
    """
    Connects to canvas and retrieves the course.
    """
    # split url into parts
    API_URL, course_id, page_name = split_url(url)

    # load configuration settings
    API_KEY = get_API(config_file, API_URL)

    # initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

    # get the course
    try:
        course = canvas.get_course(course_id)
    except:
        sys.exit("Could not connect to Canvas, check internet connection and/or API key in the config file %s" % config_file)

    return course