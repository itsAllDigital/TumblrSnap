# © 2018 Lukas W. (itsAllDigital)
# Rework for new design off main window
import appJar
import platform
import os
import urllib.request
# import sys

from loader import the_loader
from loader import config_rw

# Enable debugging messages?
enable_debug = True

# Automatically try to oauth with tumblr. If fails enable to configure the OAuth


def auto_oauth():
    print("Trying auto login to tumblr")

    # Lock the config button
    app.disableButton("check_button")

    # Set the check ico to loading
    app.setImage("chk_oauth", the_loader.get_paths("icon_path")+"auth_icon_checking.gif")

    if the_loader.check_auth(config_rw.read_current("consumer_key", the_loader.get_paths("config_path")),
                                 config_rw.read_current("consumer_secret", the_loader.get_paths("config_path")),
                                 config_rw.read_current("token_key", the_loader.get_paths("config_path")),
                                 config_rw.read_current("token_secret", the_loader.get_paths("config_path"))):
        # Switch to finished ico
        app.setImage("chk_oauth", the_loader.get_paths("icon_path")+"auth_icon_success.gif")

        print("Oauth successful. Unlock download button")
        app.enableButton("download_button")
    else:
        print("Not possible. OAuth failed")
        app.setImage("chk_oauth", the_loader.get_paths("icon_path")+"auth_icon_denied.gif")
        app.enableButton("check_button")


def oauth_check():
    if the_loader.check_auth(app.getEntry("consumer_key_field"),
                             app.getEntry("consumer_secret_field"),
                             app.getEntry("token_key_field"),
                             app.getEntry("token_secret_field")):
        print("OAuth check in main succeeded.")
        return True
    else:
        print("OAuth check in main failed.")
        return False


def stop_prog():
    if app.yesNoBox("Exit getMeTumblr", "Are you sure you want to exit?"):
        print("Stop here")
        return True


def placeholder():
    print("placeholder")


def show_info():
    app.showSubWindow("sub_info")


def open_config():
    app.hide()

    # Set the config fields
    if config_rw.read_current("consumer_key", the_loader.get_paths("config_path")) == "" and \
            config_rw.read_current("consumer_secret", the_loader.get_paths("config_path")) == "" and \
            config_rw.read_current("token_key", the_loader.get_paths("config_path")) == "" and \
            config_rw.read_current("token_secret", the_loader.get_paths("config_path")) == "":
        app.clearAllEntries()
    else:
        app.setEntry("consumer_key_field", config_rw.read_current("consumer_key", the_loader.get_paths("config_path")))
        app.setEntry("consumer_secret_field", config_rw.read_current("consumer_secret", the_loader.get_paths("config_path")))
        app.setEntry("token_key_field", config_rw.read_current("token_key", the_loader.get_paths("config_path")))
        app.setEntry("token_secret_field", config_rw.read_current("token_secret", the_loader.get_paths("config_path")))

    # Make the config visible
    app.showSubWindow("sub_config")


def exit_config():
    # Check for config difference in .cfg and fields
    if config_rw.chk_config(app.getEntry("consumer_key_field"),
                            app.getEntry("consumer_secret_field"),
                            app.getEntry("token_key_field"),
                            app.getEntry("token_secret_field"),
                            the_loader.get_paths("config_path")):
        if app.yesNoBox("Exit config", "There are unsaved changes.\n You really want to exit?"):
            app.hideSubWindow("sub_config")
            app.show()
    else:
        app.hideSubWindow("sub_config")
        app.show()


def close_config():

    # Save the config
    if oauth_check():
        config_rw.write_current(app.getEntry("consumer_key_field"), app.getEntry("consumer_secret_field"),
                                app.getEntry("token_key_field"), app.getEntry("token_secret_field"),
                                the_loader.get_paths("config_path"))
        app.hideSubWindow("sub_config")
        app.show()

        # Give message of success
        app.infoBox("Authentication successful", "Logged in.\nDownload can be started now")

        # Run auto-check again
        app.thread(auto_oauth)
    else:
        app.errorBox("Authentication failed", "Unable to authenticate with given credentials.\n"
                                              "Check for any typos and try again")


def init_download():
    # Check if the variable exists
    var_exist = "isDownload" in globals()

    if not var_exist:
        # Make the global var
        global isDownload

        # Set it to false (default)
        isDownload = False

        # Run the actual downloader
        app.disableButton("download_button")
        app.thread(down_tumblr)
    else:
        if not isDownload:
            # Var exists start download
            app.thread(down_tumblr)


def down_tumblr():
    # Set the variable for killing the download
    global stop_down

    # Make another check?
    chk_login = the_loader.tumblr_login(the_loader.get_paths("config_path"))
    if chk_login:
        # Get me the user and favorites count
        user = the_loader.get_username()
        fav_count = the_loader.get_user_fav_count()

        # Check for the download folder
        the_loader.chk_download_store(user, the_loader.get_images_path(user, "no_user"))

        # Counter to keep track of where we are
        my_counter = 0

        # Amounts the system can go full 20 at my_limit
        my_rounds_tot = the_loader.counter_run(fav_count / 20)

        # The current rounds taken
        my_rounds_cur = 0

        # The limit on how many images (Not more than 20)
        my_limit = 20

        # Set "stop down" to False, because we start here
        stop_down = False

        # Label text to show in download
        label_download = 1

        # Set an empty timestamp, since offset limits me to 1000 only
        after_timestamp = 0

        # Keep track value
        track_count_success = 0
        track_count_fail = 0

        while my_counter <= fav_count and not stop_down:

            # Get my like list
            if after_timestamp == 0:
                # print("First load. Going with offset")
                like_list = the_loader.get_likes("offset", my_limit, my_counter)
            else:
                # print("Switched to after. Bye bye offset")
                like_list = the_loader.get_likes("before", my_limit, after_timestamp)

            # Counter für die limit downloads
            cur = 0

            true_len = len(like_list["liked_posts"]) - 1

            # Set the current possiton up by the true_len counter (Shit my calcs don't allow that dynamic)
            if the_loader.chk_current(my_rounds_cur, my_rounds_tot):
                my_counter = my_counter + 20
            else:
                my_counter = the_loader.fav_remain(fav_count, my_counter)

            while cur < true_len and not stop_down:

                # Debug lines
                if enable_debug == True:
                    print("DEBUG:",
                          "\nfav_count amount: ", fav_count,
                          "\nMy_Counter position: ", my_counter,
                          "\nAfter_Timestamp: ", after_timestamp)
                    print("True_Len: ", true_len, "\n")

                # Get post type
                post_type = like_list["liked_posts"][cur]["type"]

                # When post type is photo
                if post_type == "photo":

                    # Check for multiple images within the same post

                    # See if it's actually more posts
                    multi = the_loader.check_multiple_ulr(likes=like_list, current=cur)

                    # Would print if multiple images are found
                    # print(multi[0])

                    if multi[0]:

                        # Set a val to count with
                        v1 = 0

                        while v1 < multi[1]:

                            # Set the current URL
                            cur_url = the_loader.gen_url(likes=like_list, current=cur, counter=v1)

                            # Split the url to get the file name to display
                            title_part = the_loader.gen_file_name(url=cur_url, part="part")

                            # Split the url to get the file name to use to download
                            title_full = the_loader.gen_file_name(url=cur_url, part="full")

                            # Set the title for the gui
                            app.setLabel("bottom_text_download", title_part)

                            # Make int into str and display (Shorted that) and apply
                            app.setLabel("bottom_text", "Downloading " + str(label_download) + " of " + str(fav_count))

                            # Check for exsisting file in folder
                            if the_loader.chk_img(user, title_full):
                                if not the_loader.download_likes(cur_url, the_loader.get_images_path(user, "with_user"), title_full):
                                    app.errorBox("Download Error", "While trying to download an image the download function could'nt connect to the server."
                                                                   "\nSkipping. Also pray it's working now again. Else you'll see me more often ;)")
                            else:
                                print("Image with same title exists already. Skipping that ;D."
                                      "\nYou don't have to thank me\n")

                            # Update the v1
                            v1 = v1 + 1
                    else:
                        # Set the current URL
                        cur_url = the_loader.gen_url(likes=like_list, current=cur, counter=0)

                        # Split the url to get the file name to display
                        title_part = the_loader.gen_file_name(url=cur_url, part="part")

                        # Split the url to get the file name to use to download
                        title_full = the_loader.gen_file_name(url=cur_url, part="full")

                        # Set the title for the gui
                        app.setLabel("bottom_text_download", title_part)

                        # Make int into str and display (Shorted that) and apply
                        app.setLabel("bottom_text", "Downloading " + str(label_download) + " of " + str(fav_count))

                        # Check for existing file in folder
                        if the_loader.chk_img(user, title_part):
                            if not the_loader.download_likes(cur_url, the_loader.get_images_path(user, "with_user"),
                                                             title_full):
                                app.errorBox("Download Error",
                                             "While trying to download an image the download function could'nt connect to the server."
                                             "\nSkipping. Also pray it's working now again. Else you'll see me more often ;)")
                                track_count_fail = track_count_fail + 1
                            else:
                                track_count_success = track_count_success + 1
                        else:
                            print("Image with same title exists already. Skipping that ;D."
                                  "\nYou don't have to thank me\n")
                else:
                    # The post isn't marked as "photo" and will be skipped right here. Happy code digging
                    print("Skipped a non photo post.\nYou don't need to thank me ;D")

                # Set the last timestamp of the post contacted
                after_timestamp = like_list["liked_posts"][cur]["liked_timestamp"]

                # Set the current pointer one up
                cur = cur + 1

                # Set the label one image counter up
                label_download = label_download + 1

            # See where we stand with the counter_cur
            if the_loader.chk_current(my_rounds_cur, my_rounds_tot):
                my_rounds_cur = my_rounds_cur + 1
            else:
                my_limit = the_loader.fav_remain(fav_count, my_counter)

        # What will happen when stop down is set before all is done and gone ;D
        if my_counter <= fav_count and stop_down:
            app.infoBox("Download aborted", "Download stopped by user before all images where downloaded")
        elif stop_down:
            print("Seems like you killed the download on the last image.\nCongrats")
        elif my_counter == fav_count:
            app.infoBox("Finished", "Your download has been finished successfully."
                                    "\nSuccessful images downloaded: " + str(track_count_success) +
                                    "\nImages failed to download: " + str(track_count_fail))
        app.enableButton("download_button")

# This my GUI here. Please I've been working hard on it.
# And yes I know it could be a lot prettier than this right now. (Talking about the GUI not the code, although...)


# def set_invisible_main():
    # app.setTitle("Init")
    # app.setSize(200, 200)
    # app.setResizable(canResize=False)
    # app.hide()


def set_tools():
    # Set frame for all the buttons and indicators
    app.startLabelFrame("", row=0, column=0)
    app.setSticky("ew")
    # app.setPadding(20, 0)
    app.addButton("check_button", open_config, row=0, column=0)
    app.setButton("check_button", "Config OAuth")
    app.addImage("chk_oauth", the_loader.get_paths("icon_path")+"auth_icon_pending.gif", row=0, column=1)
    app.addHorizontalSeparator(row=1, column=0, colspan=2)
    app.addButton("download_button", init_download, row=2, column=0)
    app.setButton("download_button", "Start Download")
    app.addImage("down_ring", the_loader.get_paths("icon_path")+"auth_icon_placeholder.gif", row=2, column=1)
    app.setImage("down_ring", the_loader.get_paths("icon_path")+"auth_icon_placeholder.gif")

    # Disable download button until unlock by auto or manual
    app.disableButton("download_button")

    # Stop this frame
    app.stopLabelFrame()

    # Set Frame for showing what is downloaded
    app.startFrame("down_section", row=0, column=1)
    app.setSticky("ew")
    # app.setPadding(0, 2)
    app.addLabel("top_text_download", "Download:", row=0, column=0)
    app.addLabel("bottom_text_download", "img_title", row=1, column=0)
    app.addHorizontalSeparator(row=2, column=0)
    app.addLabel("spacer", "", row=3, column=0)
    app.addLabel("bottom_text", "Downloading 0 of 0", row=4, column=0)

    app.setLabel("bottom_text_download", "")

    # Stop this frame too
    app.stopFrame()


def set_main():
    app.setTitle("TumblrSnap v1.2 Beta")
    app.setSize(800, 200)
    app.setResizable(canResize=False)
    app.setStopFunction(stop_prog)

    app.setSticky("news")
    # app.setPadding(20, 20)
    app.setExpand("both")
    app.setFont(14)

    # Set the menu
    app.addMenu("About", func=show_info)

    # Set up "the tools"
    set_tools()


def set_sub_config():
    app.startSubWindow("sub_config", title="Configure OAuth", modal=True)
    # app.setIcon(the_loader.get_paths("icon_path")+"app_icon.ico")
    app.setSticky("news")
    app.setExpand("both")
    app.setSize(600, 450)
    app.setResizable(canResize=False)
    app.setStopFunction(exit_config)  # Add the stop function later

    app.addLabel("Consumer Key:")
    app.addEntry("consumer_key_field")

    app.addLabel("Consumer Secret:")
    app.addEntry("consumer_secret_field")

    # Get some spacing
    app.addLabel(" ")

    app.addLabel("Token Key:")
    app.addEntry("token_key_field")

    app.addLabel("Token Secret:")
    app.addEntry("token_secret_field")

    # Get some spacing
    app.addLabel("  ")

    app.addImage("vali_img", the_loader.get_paths("icon_path")+"auth_icon_pending.gif")
    app.addLabel("vali_txt", text="Awaiting check")

    # Get some spacing
    app.addLabel("   ")

    # First placeholder is for updating oauth data in the config and the second is for discarding changes
    app.addButton("Check", close_config)

    # Set the default texts
    app.setEntryDefault("consumer_key_field", "")
    app.setEntryDefault("consumer_secret_field", "")
    app.setEntryDefault("token_key_field", "")
    app.setEntryDefault("token_secret_field", "")

    # Finalize the sub-window
    app.stopSubWindow()


def set_sub_info():
    app.startSubWindow("sub_info", title="About", modal=True)
    app.setResizable(canResize=False)
    app.setSize(500, 120)
    app.setSticky("w")
    app.setFont(10)

    app.addImage("creator_icon", the_loader.get_paths("icon_path")+"user_allDigital.gif", 0, 0)
    app.addLabel("created_who")

    app.setLabel("created_who", "TumblrSnap v1.2 BETA - Copyright (C) 2018  Lukas W.\n"
                                "----------------------------------------------------------------\n"
                                "This program comes with ABSOLUTELY NO WARRANTY\n"
                                "This is free software, and you are welcome to redistribute it "
                                "under certain conditions.")

    # Stop SubWindow
    app.stopSubWindow()


# The main start function


def main():
    set_main()
    set_sub_config()
    set_sub_info()

    # Check the config file
    config_rw.init_check(the_loader.get_paths("config_path"))

    # Auto OAuth
    app.thread(auto_oauth)

    # When all is set and done
    app.go()


if __name__ == "__main__":
    app = appJar.gui()
    main()
