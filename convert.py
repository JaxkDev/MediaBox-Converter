# Convert mediaboxHD m3u8 media to mp4.

from tkinter import Tk, ttk, filedialog
from urllib.request import urlretrieve
from threading import Event, Thread
import os, platform, sys, time
from shutil import which

def download(url, filename):
    global TEMP_1
    TEMP_1 = filename
    def reporthook(count, blocksize, totalsize):
        global start_time
        if count == 0:
            start_time = time.time()
            return
        duration = time.time() - start_time
        progress_size = int(count * blocksize)
        speed = int(progress_size / (1024 * duration))
        percent = int(count * blocksize * 100 / totalsize)
        if percent >= 100:
            if totalsize > (1024*1024):
                sys.stdout.write(("\r[%s] %i MB downloaded in %i seconds." + (" "*50) + "\n") %
                        (TEMP_1, progress_size / (1024 * 1024), duration))
            else:
                sys.stdout.write(("\r[%s] <1 MB downloaded." + (" "*50) + "\n") % (TEMP_1))
        else:
            sys.stdout.write("\r[%s] %d%%, %d MB, %d KB/s, %d seconds elapsed" %
                        (TEMP_1, percent, progress_size / (1024 * 1024), speed, duration))
        sys.stdout.flush()

    return urlretrieve(url, filename, reporthook)

system = platform.system()
cwd = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists("bin"):
    os.mkdir("bin")
if which("ffmpeg"):
    binary = "ffmpeg"
    print("Detected ffmpeg already in PATH.")
elif system == "Windows":
    if not os.path.exists(cwd+"\\bin\\ffmpeg-win64.exe"):
        print("Binary not found for windows, downloading now...")
        download('https://github.com/JaxkDev/MediaBox-Converter/raw/master/bin/ffmpeg-win64.exe', 'bin/ffmpeg-win64.exe')
        download('https://github.com/JaxkDev/MediaBox-Converter/raw/master/bin/LICENSE.txt', 'bin/LICENSE.txt')
    binary = cwd + "\\bin\\ffmpeg-win64.exe"
elif system == "Linux":
    if not os.path.exists(cwd+"\\bin\\ffmpeg-amd64"):
        print("Binary not found for linux, downloading now...")
        download('https://github.com/JaxkDev/MediaBox-Converter/raw/master/bin/ffmpeg-amd64', 'bin/ffmpeg-amd64')
        download('https://github.com/JaxkDev/MediaBox-Converter/raw/master/bin/LICENSE.txt', 'bin/LICENSE.txt')
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
