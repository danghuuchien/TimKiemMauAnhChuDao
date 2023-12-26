import sys
from PIL import Image, ImageTk
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

sys.stdout.reconfigure(encoding='utf-8')
#Một điểm trong không gian màu RGB với r (đỏ), g (xanh lá cây), và b (xanh dương). 
class Point(object):
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b
#lớp Cluster kế thừa từ lớp Point
class Cluster(Point):
    #khởi tạo nhận vào các giá trị r, g, b và points
    def __init__(self, r, g, b, points=[]):
        self.points = points
        super().__init__(r, g, b)
    #thêm một điểm vào cụm.
    def addPoint(self, point):
        self.points.append(point)
    #xóa tất cả các điểm khỏi cụm.
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
        #tính vị trí mới cho trung tâm của cụm dựa trên trung bình cộng của tất cả các điểm trong cụm. 
        newPoint = Point(newR / count, newG / count, newB / count)
        distanceMoved = euclidian(self, newPoint)
        print(f" KHOẢNG CÁCH DI CHUYỂN: {distanceMoved}", end="\n")
        self.r = newPoint.r
        self.g = newPoint.g
        self.b = newPoint.b
         #trả về khoảng cách mà trung tâm cụm đã di chuyển.
        return distanceMoved
    #trả về vị trí trung tâm cụm dưới ở dạng bộ ba giá trị r, g, b.
    def returnLocation(self):
        return self.r, self.g, self.b
#tìm và in ra màu chủ đạo trong hình ảnh, 
def printDominantColor(clusters):
    dominant_color = max(clusters, key=lambda x: len(x.points))
    print(f"Màu chủ đạo - Cụm {clusters.index(dominant_color) + 1}: {dominant_color.returnLocation()}")
#in ra màu trung tâm của mỗi cụm.
def printClusterColors(clusters):
    for i, cluster in enumerate(clusters):
        print(f"Cụm {i + 1}: {cluster.returnLocation()}")
# trả về danh sách các màu trung tâm của các cụm và hình ảnh gốc.
def getColors(filename, colorsWanted, min_diff):
    #mở hình ảnh,lấy tất cả các điểm từ hình ảnh 
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size
    points = getPoints(img)
    k = colorsWanted
    min_diff = min_diff
    #thực hiện k-means để phân cụm các điểm
    clusters = kmeans(points, k, min_diff)
    points = []
    for point in clusters:
        points.append(point.returnLocation())
    #sau đó in ra màu trung tâm của mỗi cụm và màu chủ đạo. 
    printClusterColors(clusters)
    printDominantColor(clusters)  
    return points, img
#chuyển đổi RGB thành định dạng mã màu hex.
def RGBtoHex(points):
    colors = []
    for rgb in points:
        r, g, b = rgb
        colors.append('#%02x%02x%02x' % (int(r), int(g), int(b)))
    return colors
#lấy tất cả các điểm từ hình ảnh và trả về dưới dạng danh sách các điểm.
def getPoints(img):
    points = []
    w, h = img.size
    for x in range(w):
        for y in range(h):
            r, g, b = img.getpixel((x, y))
            point = Point(r, g, b)
            points.append(point)
    return points
#theo dõi tổng số di chuyển của các trung tâm cụm sau mỗi vòng lặp của thuật toán k-means.
total_movement = 0 
#lưu trữ các cụm sau khi thực hiện thuật toán k-means.
clusters = [] 

def kmeans(points, k, min_diff):
    global total_movement, clusters
     # nhận vào một danh sách các điểm points
    clusters = []
    # tạo các cụm với số lượng cụm k mong muốn
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
        #Gán từng điểm dữ liệu vào cụm gần nhất (cụm có trung tâm gần điểm đó nhất).
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
            #Cập nhật vị trí trung tâm của mỗi cụm dựa trên trung bình cộng vị trí của tất cả các điểm trong cụm:
            diff[index] = centroid.calculateNewPosition()
        total_diff = sum(diff)
        total_movement += total_diff  
        print(f"Iteration {iteration + 1}: Tổng khoảng cách di chuyển = {total_diff}")
        iteration += 1
        # dừng kmeans giá trị min_diff để xác định khi nào thuật toán nên dừng lại.
        if total_diff < (min_diff * k):
            break
    # trả về vị trí cuối cùng của trọng tâm
    return clusters

def euclidian(p1, p2):
    deltaxsquared = (p1.r - p2.r) ** 2
    deltaysquared = (p1.g - p2.g) ** 2
    deltazsquared = (p1.b - p2.b) ** 2
    return (deltaxsquared + deltaysquared + deltazsquared) ** 0.5

#vẽ các màu sắc từ danh sách colors và hiển thị hình ảnh img
def drawColors(colors, img):
    fig1, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 4]})
    
    for index, color in enumerate(colors):
        ax1.add_patch(
            patches.Rectangle(
                ((index * 1 / len(colors)) + 0, 0),  # x, y
                1 / len(colors),  # chiều rộng
                1,  # chiều cao
                facecolor=color
            )
        )
        ax1.text((index + 0.5) / len(colors), -0.1, f"{index + 1}", ha='center', va='center', transform=ax1.transAxes)

    ax2.imshow(img)
    ax2.axis('off')
    
    plt.show()
#xóa dữ liệu từ các cụm
def clearData(img_label, result_text_var):
    global total_movement, clusters
    total_movement = 0  # Reset the total movement
    for cluster in clusters:
        cluster.clearPoints()
    img_label.config(image='')
    result_text_var.set('')  
#cập nhật hộp văn bản result_text_var với tổng khoảng cách di chuyển total_movement
def update_textbox(result_text_var):
    result_text_var.set(f'Tổng khoảng cách di chuyển: {total_movement:.2f}')

def main():
    root = tk.Tk()
    root.title("Phân Cụm Màu Sắc")
    root.geometry("600x400")

    file_path_var = tk.StringVar()
    num_clusters_var = tk.StringVar() 
    result_text_var = tk.StringVar()

    img_label = ttk.Label(root)
    img_label.grid(row=5, column=0, columnspan=3)

    def open_file_dialog():
        file_path = filedialog.askopenfilename()
        file_path_var.set(file_path)
        img_label.config(image='')
        result_text_var.set('')  
    #quá trình phân cụm màu sắc trong một hình ảnh
    def perform_clustering():
        file_path = file_path_var.get()
        num_clusters = num_clusters_var.get() 
        if not file_path or not num_clusters:
            return
        global total_movement, clusters
        total_movement = 0  
        # Gọi hàm getColors,số lượng cụm, min_diff là 1 
        # thực hiện K-means trên hình ảnh
        # trả về danh sách các màu trung tâm của các cụm và hình ảnh gốc.
        colors, img = getColors(file_path, int(num_clusters), 1) 
        hex_colors = RGBtoHex(colors)
        drawColors(hex_colors, img)
        update_textbox(result_text_var)  

    file_label = ttk.Label(root, text="Chọn ảnh:")
    #file_entry = ttk.Entry(root, textvariable=file_path_var, state="readonly")
    browse_button = ttk.Button(root, text="Duyệt", command=open_file_dialog)
    
    num_clusters_label = ttk.Label(root, text="Số nhóm muốn tạo:")  
    num_clusters_entry = ttk.Entry(root, textvariable=num_clusters_var)  

    cluster_button = ttk.Button(root, text="Phân Cụm", command=perform_clustering)
    clear_button = ttk.Button(root, text="Xóa Dữ Liệu", command=lambda: clearData(img_label, result_text_var))
    result_label = ttk.Label(root, textvariable=result_text_var)

    file_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    
    browse_button.grid(row=0, column=1, padx=5, pady=5)
    
    num_clusters_label.grid(row=1, column=0, padx=5, pady=5, sticky="e") 
    num_clusters_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")  

    cluster_button.grid(row=2, column=1, columnspan=3, pady=20)
    clear_button.grid(row=3, column=1, columnspan=3, pady=10)
    result_label.grid(row=4, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()