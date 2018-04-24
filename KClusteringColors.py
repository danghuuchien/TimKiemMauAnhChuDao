from PIL import Image
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Point(object):
    def __init__(self, r=0, g=0, b=0):
        self.r=r
        self.g=g
        self.b=b

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

        newPoint = Point(newR/count, newG/count, newB/count)
        distanceMoved = euclidian(self, newPoint)
        print("DISTANCE MOVED: " + str(distanceMoved))
        self.r = newPoint.r
        self.g = newPoint.g
        self.b = newPoint.b

        return distanceMoved

    def returnLocation(self):
        return self.r, self.g, self.b



##################################

def getColors(filename, colorsWanted, min_diff):
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size

    points = getPoints(img)

    k = colorsWanted

    #min diff to stop kmeans
    min_diff = min_diff

    clusters = kmeans(points, k, min_diff)

    points = []

    for point in clusters:
        points.append(point.returnLocation())
    return points

##################################

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
            r, g, b = img.getpixel((x,y))
            point = Point(r, g, b)
            points.append(point)

    return points


def kmeans(points, k, min_diff):
    clusters = []

    #make the clusters
    for _ in range(k):
        i = random.randint(0, len(points))
        rR = random.randint(0, 355)
        rG = random.randint(0, 355)
        rB = random.randint(0, 355)
        cluster = Cluster(rR, rG, rB, [])
        clusters.append(cluster)



    #begin kmeans algorithm
    while True:
        for point in points:

            smallest_distance = float('Inf')
            closest_centroid = 0
            #loops through each cluster
            for i in range(k):
                dist = euclidian(point, clusters[i])

                if dist < smallest_distance:
                    smallest_distance = dist
                    closest_centroid = i

            #add the point to its closest centroid
            clusters[closest_centroid].addPoint(point)

        #differences for all centroids
        diff = list(range(k))
        #calculate new centroid position
        for index, centroid in enumerate(clusters):
            diff[index] = centroid.calculateNewPosition()

        #stop kmeans
        if sum(diff) < (min_diff*k):
            break

    #return final positions of centroids
    return clusters


def euclidian(p1, p2):
    deltaxsquared = (p1.r - p2.r) ** 2
    deltaysquared = (p1.g - p2.g) ** 2
    deltazsquared = (p1.b - p2.b) ** 2
    return (deltaxsquared + deltaysquared + deltazsquared) ** 0.5

def drawColors(colors):

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    #plot colors
    for index, color in enumerate(colors):
        ax1.add_patch(
            patches.Rectangle(
                ((index * 1/len(colors)) + 0, 0), #x, y
                1/len(colors), #width
                1, #height
                facecolor=color
            )
        )
    fig1.savefig('colors.png', dpi=90, bbox_inches='tight')

#drawColors(RGBtoHex(getColors("zissou.jpg", 4, 0.08)))
