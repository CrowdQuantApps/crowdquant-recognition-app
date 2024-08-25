<div align="center">

![App Logo](https://i.imgur.com/PF9WRIe.png)

</div>

## Installation
#### 1) Install FFMPEG (Skip this step if you already have it installed.)
- Download ```ffmpeg-master-latest-win64-gpl.zip``` from [FFMPEG](https://github.com/BtbN/FFmpeg-Builds/releases).
- Open the ZIP archive and navigate to the "**bin**" folder.
- Copy these 3 files and go to drive "**C**".
- Create a folder on drive "**C**" named "**ffmpeg**" and paste the copied files into it.
- Next, open "**Edit the system environment variables**" and click on "**Environment Variables**".
- Select "**PATH**" from the user variables and click "**Edit**".
- Next, click "**New**" and paste the given path ```C:\ffmpeg```.
- Click "**Ok**", then open cmd and type ```ffmpeg``` to check if it was installed correctly.

#### 2) Install PyCharm (Skip this step if you already have it installed.)
- Download [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/?section=windows).
- Install downloaded exe file.

#### 3) Install & Run App
First Method:
- Type ```py install.py``` in cmd to install all the necessary libraries for the application to work.
- Then type the same thing again to make sure all the libraries were installed correctly. Once you've done that, type ```py main.py```.

Second Method:
- Open the entire application folder in PyCharm.
- Then select the run mode to "**Current file**".
- Next, open the "**install.py**" file and run it, then do it again to make sure everything is installed.
- Finally, go to the "**main.py**" file, change the run mode to "**main**", and run the application.

## Changelog

Please see the [CHANGELOG](CHANGELOG.md) for more information about what has changed recently.