# Command line interface script that uses the YouTube-DL library
# Run script and give URL of a YouTube video to get an mp3 file output
# I use this for anything on YT when I want to save the audio only


from __future__ import unicode_literals
import youtube_dl
import os
import glob

url = input('Enter YouTube URL: ')
new_name = input('Name file: ')
print('Processing...')


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

# YouTubeDL gives us a file name that is usually long and not very neat
# rename file by grabbing all the mp3 files and finding the newest created

list_of_files = glob.glob('*.mp3')
latest_file = max(list_of_files, key=os.path.getctime)
given_name = latest_file

# add the mp3 file type if user did not
# make sure the filename will not overwrite another file
while True:
    if new_name.endswith('.mp3') == False:
        new_name = new_name + '.mp3'
    if new_name not in list_of_files:
        break
    else:
        new_name = input('File name taken, enter valid filename: ')
        continue

os.rename(given_name, new_name)

print(new_name, 'has finished downloading.')
