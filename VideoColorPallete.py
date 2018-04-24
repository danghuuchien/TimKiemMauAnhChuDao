from KClusteringColors import (getColors, drawColors, Point, Cluster, kmeans, RGBtoHex)
import cv2
import os

def splitVideoToImageFiles(file, folderName, frameSplit):

    if not os.path.exists(folderName):
        os.makedirs(folderName)

        video = cv2.VideoCapture(file)
        success, image = video.read()
        success = True
        frames = 0
        i = 0
        while success:
            #only saves every 10th frame to save time
            if i%frameSplit == 0:
                cv2.imwrite(folderName+"/frame%d.jpg" % (i/frameSplit), image)
                frames += 1
                print("Splitting Frame: " + str(i/frameSplit))
            success, image = video.read()
            i += 1
        return frames

def getColorsFromVideo(dir, frameCount):
    colors = []
    for i in range(frameCount):
        colors.append(getColors(filename=dir+"/frame%d.jpg" % (i), colorsWanted=6, min_diff=1))
    return colors


folderName = "Space"
frames = splitVideoToImageFiles("space.mp4", folderName, 120)
videoColors = getColorsFromVideo(folderName, frameCount=frames)

# rerun kmeans algorithim for total colors in video to determine most popular ones
points = []
for colorArr in videoColors:
    r,g,b = colorArr[0]
    point = Point(r,g,b)
    points.append(point)

clusters = kmeans(points, k=6, min_diff=0.1)

colorPointsMovie = []

for point in clusters:
    colorPointsMovie.append(point.returnLocation())

drawColors(RGBtoHex(colorPointsMovie))
