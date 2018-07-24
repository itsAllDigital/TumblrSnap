TumblrSnap (getMeTumblr)
========================
This is a small tool, I build mainly for downloading and saving all favs on Tumblr.

Currently it only supports image posts and will ignore any posts containing text.

**Importand Notice:** Your credentials will be stored in plain text. So anyone with access to your files can potentialy use them to post, edit, delete posts, mess around with your liked posts, so on. Continue if you're aware of the potential risks.

Oh and keep in mind that you won't be able to send more than 2000 requests within an hour and 5000 within one day. It's a limit set by Tumblr to redouce server load (I have no ability to bypass that). If you want to be able to have more requests per hour/day you'll have to ask Tumblr to lift the restrictions on your application (Which will probably won't happen :/).

## How to use

Since this program is writen in Python you'll need Python to make the file usable <strike>or you'll donwload the all in one EXE file</strike>.

<strike>**Using the pre-build executable**</strike>

<strike>From [here](https://github.com/itsAllDigital/TumblrSnap/releases) you can download the TumblrSnap_v.X.X.exe (The X.X will be the current Version number).</strike>

<strike>After that just double click the executable which in turn will start. On first startup it you will have to click the "Config OAuth" button to enter your OAuth-Credentials to be able to download your liked images.</strike>

<strike>If you don't have your credentials and are unsure how to get them, follow this link in [how to get your OAuth-Credentials](https://gitlab.com/itsAllDigital/getmetumblr#how-to-get-your-oauth-credentials).</strike>

<strike>Otherwhise you can now enter them into the empty fields and after letting the program check if they are valid you can then click the "Start Download" button.</strike>

<strike>All images will be saved into the images folder under your username.</strike>

**Using the python file directly**

If you want to use the python file to run the program you have to download the packed ZIP file from [here](https://github.com/itsAllDigital/TumblrSnap/releases) or download the repository as a ZIP. Then unpack it inside the folder you want to run the program from.

Python is a needed program to run .py files so you need to download and install said program from here: [LINK](https://www.python.org/downloads/)

**Notice:** You need to tick the "Add to PATH" as well or your command promt wont recognize the "python" command and you'll either will have to reinstall the program (to then tick the checkbox) or manually add Python to your PATH. 
When the installer shows that the setup was successful, click on the disable path length limit to avoid any potential problems.

After that start a command prompt and enter the follwoing command to get the missing depenencies because those are not included in Python itself.

```
pip install pytumblr appjar
```

After that navigate to the folder you stored the extracted content of the downloaded ZIP in and issue the following command:
```
python main_remastered.py
```

Alternatively you can also use the .bat file to run the program with. All you need to to there is to double-click it like a normal program.

The program will load up. If this is your first time loading the program you will have to setup your OAuth-Credentials by clicking "Config OAuth".


If you don't have your credentials and are unsure how to get them, follow this link in [how to get your OAuth-Credentials](https://github.com/itsAllDigital/TumblrSnap#how-to-get-your-oauth-credentials).

Otherwhise you can now enter them into the empty fields and after letting the program check if they are valid you can then click the "Start Download" button.

All images will be saved into the images folder under your username.

### How to get your OAuth-Credentials

The credentials you need to optain are:

* Consumer key

* Consumer secret

* Token key

* Token secret

**1 - Get your consumer key and secret**

Open this [LINK](https://www.tumblr.com/oauth/register) to create an application.

**Notice:** Only fill out the fields marked with a star. For the callback-URL just enter a random URL as it doesn't matter for you. An example would be: https://empyt.gurl

When everything worked out you'll be taken to your application page where you can see your consumer key directly next unter your application name you did enter.

One below you can click "Show consumer secret" to also show the consumer secret.

You can either enter them both directly into the program or write them down for now.

**2 - Get your token key and secret**

Open this [LINK](https://api.tumblr.com/console/calls/user/info)

You'll be asked to enter your consumer key and token. After you enter them both and click the button bellow to continue you'll be asked if you want to grant the application access. Confirm to continue.

You'll be taken to a page were you only need to click the top button labled "Show keys". Which in turn will show you your consumer key and secret as well as both the token key and secret.

Copy your token key and secret and either enter them or write them down.

**3 - Enter your credentials**

When you have all your credentials enter them into the fields given withen the program after you hit "Config OAuth". Press "Check" to let the program confirm that your entered credentials are correct.

If so it will automaticaly save them and close the config window. Afterwards it will unlock the "Start Download" button with which you now can start your download ;D

## Issues

**Please use the function from github to report any issues.**

## What was used

Python - It's the programming language so... ;D

pytumblr - A module writen and maintained by Tumblr itself

appjar - The module that helped me make my GUI (Read more on their website [HERE](https://appjar.info))

As well as two modules writen from me for this purpose (the_loader and config_rw).

## Who made this

© 2018 Lukas W. (itsAllDigital)
(Ported over from my gitlab repo https://gitlab.com/itsAllDigital/getmetumblr)
