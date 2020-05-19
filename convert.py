# Convert m3u8 playlist to mp4.

import os
from tkinter import filedialog

finalManifest = ""

mediaManifest = filedialog.askopenfilename(title="Please select the media playlist file.", filetypes=(("Media Manifest File", "*.m3u8"),))
print("Loading data from "+mediaManifest+"\n")
mediaManifestData = open(mediaManifest, "r").read().split("\n")[-2]  # TODO is this always the case ?

mediaDirectory = os.path.dirname(os.path.abspath(mediaManifest))
mediaPlaylist = os.path.join(mediaDirectory, mediaManifestData)

mediaPlaylistData = open(mediaPlaylist, "r")
for file in mediaPlaylistData:
    if file[0] != "#":
        finalManifest += "file '"+os.path.join(mediaDirectory, file).replace("\n", "")+"'\n"

finalManifest = finalManifest[:-1:]

finalManifestPath = os.path.join(mediaDirectory, "playlist.txt")
f = open(finalManifestPath, "w")
f.write(finalManifest)
f.close()

finalOutputPath = os.path.join(mediaDirectory, "media.mp4")

print("Merging into "+finalOutputPath)

# Todo better handling:
os.system("ffmpeg -safe 0 -f concat -i "+finalManifestPath+" -c copy "+finalOutputPath)
