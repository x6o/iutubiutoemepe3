# imports
import pafy
import sys
from progress.bar import Bar
from subprocess import call


# config
playlist_link = "https://www.youtube.com/playlist?list=PLdvNAMcKf2V_pej1VcKYao1HyGFsCUIQu"
dl_cmd = 'youtube-dl --extract-audio --audio-format mp3 --audio-quality 0'.split(' ')
playlist_object = pafy.get_playlist2(playlist_link)
iutubiu_ids = []
local_ids = []
local_db_filepath = "./local.txt"
local_music_path = "./music/"


# Get YouTube playlist IDs
print('Playlist has ' + str(len(playlist_object)) + ' vids.')

bar = Bar('Retrieving playlist info', max=len(playlist_object), suffix='%(index)d/%(max)d - %(percent).1f%%')
for vidObj in playlist_object:
        iutubiu_ids.append(vidObj.videoid)
        bar.next()
bar.finish()

print "yt ids: %s" % iutubiu_ids


# Get local ids
with open(local_db_filepath, "rw") as file:
    local_ids = file.read().splitlines()

print "local ids: %s" % local_ids


# Get differences
ids_not_on_iutubiu =  [item for item in local_ids if item not in iutubiu_ids]
ids_not_locally =  [item for item in iutubiu_ids if item not in local_ids]

print "ids_not_on_iutubiu: %s" % ids_not_on_iutubiu
print "ids_not_locally: %s" % ids_not_locally


# Download ids not available locally
for id in ids_not_locally:
    dl_cmd.append('https://www.youtube.com/watch?v=' + id)
    call(dl_cmd)

    with open(local_db_filepath, 'a') as the_file:
        the_file.write(id + '\n')

# TODO: Delete songs not on iutubiu (sync functionality)
# Final boss: add mp3 info 