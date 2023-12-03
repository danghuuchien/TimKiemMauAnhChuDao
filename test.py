import sys
from PIL import Image
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
from tkinter import filedialog

# Set the console encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class Point(object):
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

class Cluster(Point):
    def __init__(self, r, g, b, points=[]):
        self.points = points
        super().__init__(r, g, b)

    def addPoint(self, point):
        self.points.append(point)

    def clearPoints(self):
        self.points = []

    def calculateNewPosition(self):
        newR = 0
        newG = 0
        newB = 0
        count = 1
        for point in self.points:
            newR += point.r
            newG += point.g
            newB += point.b
            count += 1

        newPoint = Point(newR / count, newG / count, newB / count)
        distanceMoved = euclidian(self, newPoint)
        print(f" KHOẢNG CÁCH DI CHUYỂN: {distanceMoved}", end="\n")
        self.r = newPoint.r
        self.g = newPoint.g
        self.b = newPoint.b

        return distanceMoved

    def returnLocation(self):
        return self.r, self.g, self.b

def getColors(filename, colorsWanted, min_diff):
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size
    points = getPoints(img)
    k = colorsWanted
    min_diff = min_diff
    clusters = kmeans(points, k, min_diff)
    points = []
    for point in clusters:
        points.append(point.returnLocation())
    return points

def RGBtoHex(points):
    colors = []
    for rgb in points:
        r, g, b = rgb
        colors.append('#%02x%02x%02x' % (int(r), int(g), int(b)))
    return colors

def getPoints(img):
    points = []
    w, h = img.size
    for x in range(w):
        for y in range(h):
            r, g, b = img.getpixel((x, y))
            point = Point(r, g, b)
            points.append(point)
    return points

def kmeans(points, k, min_diff):
    clusters = []
    for _ in range(k):
        i = random.randint(0, len(points))
        rR = random.randint(0, 255)
        rG = random.randint(0, 255)
        rB = random.randint(0, 255)
        cluster = Cluster(rR, rG, rB, [])
        clusters.append(cluster)
    iteration = 0
    while True:
        for point in points:
            smallest_distance = float('Inf')
            closest_centroid = 0
            for i in range(k):
                dist = euclidian(point, clusters[i])
                if dist < smallest_distance:
                    smallest_distance = dist
                    closest_centroid = i
            clusters[closest_centroid].addPoint(point)
        diff = list(range(k))
        for index, centroid in enumerate(clusters):
            diff[index] = centroid.calculateNewPosition()
        total_diff = sum(diff)
        print(f"Iteration {iteration + 1}: Tổng khoảng cách di chuyển = {total_diff}")
        iteration += 1
        if total_diff < (min_diff * k):
            break
    return clusters

def euclidian(p1, p2):
    deltaxsquared = (p1.r - p2.r) ** 2
    deltaysquared = (p1.g - p2.g) ** 2
    deltazsquared = (p1.b - p2.b) ** 2
    return (deltaxsquared + deltaysquared + deltazsquared) ** 0.5

def drawColors(colors):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    for index, color in enumerate(colors):
        ax1.add_patch(
            patches.Rectangle(
                ((index * 1 / len(colors)) + 0, 0),
                1 / len(colors),
                1,
                facecolor=color
            )
        )
    fig1.savefig('colors.png', dpi=90, bbox_inches='tight')

def drawImageWithClusters(img, clusters):
    w, h = img.size
    new_img = Image.new("RGB", (w, h))

    for x in range(w):
        for y in range(h):
            point = Point(*img.getpixel((x, y)))
            cluster_indices = [cluster.assignPointsToClusters(clusters) for cluster in clusters]
            cluster_index = cluster_indices.index([i for i, val in enumerate(cluster_indices) if point in val][0])
            color = (int(clusters[cluster_index].r), int(clusters[cluster_index].g), int(clusters[cluster_index].b))
            new_img.putpixel((x, y), color)

    new_img.show()

def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Chọn hình ảnh", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if file_path:
        colors = getColors(file_path, 4, 0.08)
        hex_colors = RGBtoHex(colors)
        drawColors(hex_colors)

        img = Image.open(file_path)
        img.thumbnail((200, 200))
        points = getPoints(img)
        clusters = kmeans(points, 4, 0.08)



if __name__ == "__main__":
    main()
