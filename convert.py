# Convert mediaboxHD m3u8 media to mp4.

import os, platform, sys
from tkinter import filedialog

system = platform.system()
cwd = os.path.dirname(os.path.realpath(__file__))
if system == "Windows":
    binary = cwd + "\\bin\\ffmpeg-win64.exe"
elif system == "Linux":
    binary = cwd + "\\bin\\ffmpeg-amd64"
else:
    sys.stderr.write("Unsupported system: "+system)
    exit(1)

finalManifest = ""

mediaManifest = filedialog.askopenfilename(title="Please select the media playlist file.", filetypes=(("Media Manifest File", "*.m3u8"),))
if mediaManifest == "":
    sys.stderr.write("No input.")
    exit(1)
print("Loading data from "+mediaManifest)
mediaName = os.path.basename(mediaManifest)[:-5:]
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

finalOutputPath = os.path.join(mediaDirectory, mediaName+".mp4")

print("Merging into "+finalOutputPath)

# Todo better handling:
os.system(binary+" -safe 0 -f concat -i "+finalManifestPath+" -c copy "+finalOutputPath)
