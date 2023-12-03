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
def printDominantColor(clusters):
    dominant_color = max(clusters, key=lambda x: len(x.points))
    print(f"Màu chủ đạo - Cụm {clusters.index(dominant_color) + 1}: {dominant_color.returnLocation()}")

def getColors(filename, colorsWanted, min_diff):
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size
    points = getPoints(img)
    k = colorsWanted
    # khoảng cách tối thiểu để dừng kmeans
    min_diff = min_diff
    clusters = kmeans(points, k, min_diff)
    points = []
    for point in clusters:
        points.append(point.returnLocation())
    printDominantColor(clusters)
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
    # tạo các cụm
    for _ in range(k):
        i = random.randint(0, len(points))
        rR = random.randint(0, 255)
        rG = random.randint(0, 255)
        rB = random.randint(0, 255)
        cluster = Cluster(rR, rG, rB, [])
        clusters.append(cluster)
    iteration = 0
    # bắt đầu thuật toán kmeans
    while True:
        for point in points:
            smallest_distance = float('Inf')
            closest_centroid = 0
            # duyệt qua từng cụm
            for i in range(k):
                dist = euclidian(point, clusters[i])

                if dist < smallest_distance:
                    smallest_distance = dist
                    closest_centroid = i
            # thêm điểm vào cụm gần nhất của nó
            clusters[closest_centroid].addPoint(point)
        # tính sự khác biệt cho tất cả các trọng tâm
        diff = list(range(k))
        # tính toán vị trí trọng tâm mới
        for index, centroid in enumerate(clusters):
            diff[index] = centroid.calculateNewPosition()
        total_diff = sum(diff)
        print(f"Iteration {iteration + 1}: Tổng khoảng cách di chuyển = {total_diff}")
        iteration += 1
        # dừng kmeans
        if total_diff < (min_diff * k):
            break
    # trả về vị trí cuối cùng của trọng tâm
    return clusters
def euclidian(p1, p2):
    deltaxsquared = (p1.r - p2.r) ** 2
    deltaysquared = (p1.g - p2.g) ** 2
    deltazsquared = (p1.b - p2.b) ** 2
    return (deltaxsquared + deltaysquared + deltazsquared) ** 0.5
def drawColors(colors):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    # vẽ màu
    for index, color in enumerate(colors):
        ax1.add_patch(
            patches.Rectangle(
                ((index * 1 / len(colors)) + 0, 0),  # x, y
                1 / len(colors),  # chiều rộng
                1,  # chiều cao
                facecolor=color
            )
        )
    fig1.savefig('colors2.png', dpi=90, bbox_inches='tight')
# Hàm main để chạy ứng dụng
def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Chọn hình ảnh", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if file_path:
        colors = getColors(file_path, 3, 0.08)
        hex_colors = RGBtoHex(colors)
        drawColors(hex_colors)

if __name__ == "__main__":
    main()
