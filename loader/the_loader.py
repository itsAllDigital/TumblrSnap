# © 2018 Lukas W. (itsAllDigital)

import os
import platform
import pytumblr
import urllib.request
import math
from loader import config_rw

down_check = False


def tumblr_login(path):
    global myTumb
    myTumb = pytumblr.TumblrRestClient(config_rw.read_current('consumer_key', path),
                                       config_rw.read_current('consumer_secret', path),
                                       config_rw.read_current('token_key', path),
                                       config_rw.read_current('token_secret', path))
    try:
        chk = myTumb.info()["user"]["name"]
        print(chk)
        return True
    except KeyError:
        return False


def check_auth(cons_key, cons_sec, tok_key, tok_sec):
    print("Trying login")
    log = pytumblr.TumblrRestClient(
        consumer_key=cons_key,
        consumer_secret=cons_sec,
        oauth_token=tok_key,
        oauth_secret=tok_sec
    )
    user = log.info()
    try:
        chk = user["user"]["name"]
        print("Seems success", chk)
        return True
    except KeyError:
        print("Unable to login")
        return False


def chk_download_store(username, path):
    # Check if image folder exists
    if os.path.isdir(path):
        if os.path.isdir(path + username):
            return True
        else:
            os.mkdir(path + username)
            return True
    else:
        os.mkdir(path)
        os.mkdir(path + username)
        return True


def kill_download():
    global down_check
    down_check = True


def get_user_fav_count():
    all_likes = myTumb.info()['user']['likes']

    return all_likes


def get_username():
    user = myTumb.info()['user']['name']

    return user


def get_likes(down_mode, my_limit, position):
    if down_mode == "before":
        likes = myTumb.likes(limit=my_limit, before=position)
    else:
        likes = myTumb.likes(limit=my_limit, offset=position)

    return likes


def download_likes(url, path, title):
    try:
        urllib.request.urlretrieve(url, path + title)
        return True
    except ConnectionAbortedError or ConnectionError or ConnectionRefusedError or ConnectionResetError:
        try:
            urllib.request.urlretrieve(url, path + title)
            return True
        except ConnectionAbortedError or ConnectionError or ConnectionRefusedError or ConnectionResetError:
            print("Download error.")
            return False


def check_multiple_ulr(likes, current):

    # Check for multiple images in one post and return that somehow to be worked with
    list_len = len(likes["liked_posts"][current]["photos"])

    if list_len > 1:
        return True, len(likes["liked_posts"][current]["photos"])
    elif list_len <= 1:
        return False, 0


def chk_img(user, title):

    # Check image existence, her if not
    if not os.path.isfile(get_images_path(user, "with_user")+title):
        # Image isn't there enable download
        return True
    else:
        # The file is there, don't download
        return False


def gen_url(likes, current, counter):
    # Refactor likes here
    return likes["liked_posts"][current]["photos"][counter]["original_size"]["url"]


def gen_file_name(url, part):

    if part == "part":
        # Split the url first to get to the essential part
        split_1 = url.split("/")

        # Get the length of it and reduce it by one to get the last entry number for the file name
        split_len = len(split_1) - 1

        # Remove file extension to just get the file name
        split_2 = split_1[split_len].split(".")
        img_title = split_2[0]

        return img_title
    if part == "full":
        # Split the url first to get to the essential part
        split_1 = url.split("/")

        # Get the length of it and reduce it by one to get the last entry number for the file name
        split_len = len(split_1) - 1

        return split_1[split_len]


def get_paths(typ):
    # Get the platform system
    sys_chk = platform.system()

    if sys_chk == "Windows":
        if typ == "icon_path":
            ico_path = ".\\icons\\"
            return ico_path
        if typ == "config_path":
            conf_path = ".\\config\\"
            return conf_path
        if typ == "image_path":
            return False
        else:
            print("Unknown path was requested. Returning nothing")
            return

    if sys_chk == "Linux" or sys_chk == "Unix":
        if typ == "icon_path":
            ico_path = "./icons/"
            return ico_path
        if typ == "config_path":
            conf_path = "./config/"
            return conf_path
        if typ == "image_path":
            print("Needs other function. Go away")
            return
        else:
            print("Unknown path was requested. Returning nothing")
            return


def get_images_path(user, part):
    sys_chk = platform.system()

    if sys_chk == "Windows":
        if part == "with_user":
            img_path = ".\\images\\"+user+"\\"
            return img_path
        if part == "no_user":
            img_path = ".\\images\\"
            return img_path
    elif sys_chk == "Linux" or sys_chk == "Unix":
        if part == "with_user":
            img_path = "./images/"+user+"/"
            return img_path
        elif part == "no_user":
            img_path = "./images/"
            return img_path
    else:
        print("Seems I missed an OS here then :/")


def counter_run(counts):
    fl_count = counts
    fl_cur = 0.0
    while fl_cur <= fl_count:
        fl_cur = fl_cur + 1.0
    return math.floor(fl_cur)


def chk_current(rnd_cur, rnd_full):
    if rnd_cur < rnd_full:
        return True
    else:
        return False


def fav_remain(favs, counter):
    counter = favs - counter
    if not counter < 0:
        return counter
