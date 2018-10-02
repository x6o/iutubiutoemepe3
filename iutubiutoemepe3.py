# imports
import pafy
import sys
from progress.bar import Bar
from subprocess import call
from multiprocessing import Pool
from os import listdir, remove
from os.path import isfile, join


# config
playlist_link = "https://www.youtube.com/playlist?list=PLdvNAMcKf2V_pej1VcKYao1HyGFsCUIQu"
dl_cmd = 'youtube-dl --extract-audio --audio-format mp3 --audio-quality 0'.split(' ')
playlist_object = pafy.get_playlist2(playlist_link)
iutubiu_ids = []
local_ids = []
local_db_filepath = "./local.txt"
files_in_directory = [f for f in listdir('./') if isfile(join('./', f))]
local_paths = {}

def dl_vid(id):
    dl_cmd.append('https://www.youtube.com/watch?v=' + id)
    call(dl_cmd)

    with open(local_db_filepath, 'a') as the_file:
        the_file.write(id + '\n')

def delete_local_vid(id):
    try:
        #remove from file
        f = open(local_db_filepath,"r+")
        d = f.read().splitlines()
        f.seek(0)
        for i in d:
            if i != id:
                f.write(i + '\n')
        f.truncate()
        f.close()

        # remove from dir
        remove("./" + local_paths[id])
        print 'Deleted id: %s' % id 
    except Exception, e:
        print repr(e)

def map_paths():
    for id in local_ids:
        for filename in files_in_directory:
            curr_id = filename.split(".")[-2][-11:]
            print "curr_id: %s" % curr_id
            if id == curr_id:
                local_paths[id] = filename

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
if ids_not_locally:
    pool = Pool(processes=50)
    pool.map(dl_vid, ids_not_locally)
    pool.terminate()

# Delete songs not on iutubiu (sync functionality)
if ids_not_on_iutubiu and local_ids:
    map_paths()
    pool = Pool(processes=10)
    pool.map(delete_local_vid, ids_not_on_iutubiu)
    pool.terminate()

# Final boss: add mp3 info 
# Final final boss: sync with ipod!