from collections import namedtuple
from math import sqrt
import random
try:
    import Image
except ImportError:
    from PIL import Image

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(filename, n=3):
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
import glob
import os
import time
import subprocess
import shutil
from time import sleep
file_name=raw_input("Enter file name : ");
newpath = './' + file_name[:5] 
print file_name
print newpath
bashCommand = "ffmpeg -i " + newpath + "/" + file_name + " -r 0.1 -s vga " + newpath + "/image-%1d.jpeg"
print bashCommand
if not os.path.exists(newpath): os.makedirs(newpath)
shutil.move(file_name, newpath)
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]
r=0
b=0
g=0
count=0
os.chdir(newpath)
fo=open("color_result.txt","w")
for files in glob.glob("*.jpeg"):
    print files
    print(colorz(files,3))
    count = count + 3
    li=colorz(files,3)
    for j in li :
	fo.write(j)
	fo.write(", ")
        x,y,z=hex_to_rgb(j)
        r = r+x
        g = g+y
        b = b+z
    fo.write("\n")

r=r/count
g=g/count
b=b/count
fo.write("Final dominant color : ")
fo.write(rgb_to_hex((r,g,b)))
blah = rgb_to_hex((r,g,b))
if(blah[0]=='#'):
    blah = blah[1:]
bla = (blah[0:2], blah[2:4], blah[4:6])
bl = ['02%X' % (255 - int(a, 16)) for a in bla]
bl = '#'+bl
fo.write("The color you need for thr subtitles is : ")
fo.write(bl)
fo.close()
sleep(2)
