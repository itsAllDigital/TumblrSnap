# © 2018 Lukas W. (itsAllDigital)
import json
import os


def exist_check_dir(path):
    if os.path.isdir(path):
        # print("Directory exists")
        return True
    else:
        # print("It doesn't")
        return False


def exist_check_file(path):
    if os.path.isfile(path+"authentic.cfg"):
        # print("File is there")
        return True
    else:
        # print("File not there or renamed")
        return False


def init_check(path):
    if exist_check_dir(path):
        if exist_check_file(path):
            print("Done")
        else:
            f = open(path+"authentic.cfg", "w")
            f.write('{"consumer_key": "", "consumer_secret": "", "token_key": "", "token_secret": ""}')
            f.close()

            print("Made the default config")
    else:
        os.mkdir(path)
        f = open(path+"authentic.cfg", "w")
        f.write('{"consumer_key": "", "consumer_secret": "", "token_key": "", "token_secret": ""}')
        f.close()

        print("Made the folder and config")


def read_current(get_me, path):
    # Preload check
    # Both the folder and the correct file exist
    if exist_check_dir(path) and exist_check_file(path):
        # Open the config file and read into data var
        conf = open(path+"authentic.cfg", "r")
        data = conf.read()
        conf.close()

        # Convert it into a dict
        x = json.loads(data)
        # Return the vars needed

        # print(x[get_me])

        return x[get_me]

    # Only folder exists
    elif exist_check_dir(path) and not exist_check_file(path):
        with open(path+"authentic.cfg", "w") as outfile:
            dic = {"consumer_key": "", "consumer_secret": "", "token_key": "", "token_secret": ""}
            json.dump(dic, outfile)
        outfile.close()
        read_current(get_me, path)

    # Nothing exists
    else:
        os.mkdir(path)
        with open(path+"authentic.cfg", "w") as outfile:
            dic = {"consumer_key": "", "consumer_secret": "", "token_key": "", "token_secret": ""}
            json.dump(dic, outfile)
        outfile.close()
        read_current(get_me, path)


def write_current(con_key, con_sec, tok_key, tok_sec, path):
    with open(path+"authentic.cfg", "w") as outfile:
        dic = {"consumer_key": con_key, "consumer_secret": con_sec, "token_key": tok_key, "token_secret": tok_sec}
        json.dump(dic, outfile)
    outfile.close()
    return True


def chk_config(con_key, con_sec, tok_key, tok_sec, path):
    print(con_key, con_sec, tok_key, tok_sec)
    if read_current("consumer_key", path) == con_key and read_current("consumer_secret", path) == con_sec and \
            read_current("token_key", path) == tok_key and read_current("token_secret", path) == tok_sec and not \
            read_current("consumer_key", path) == "" and not read_current("consumer_secret", path) == "" and not \
            read_current("token_key", path) == "" and not read_current("token_secret", path) == "":
        print("Both sides are the same")
        return False
    else:
        print("They are not the same")
        return True
