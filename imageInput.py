import os
import cv2
import argparse
import subprocess
import numpy as np

OBJ, BKG = "OBJ", "BKG"
OBJCODE, BKGCODE = 1, 2
OBJCOLOR, BKGCOLOR = (0, 0, 255), (0, 255, 0)

SF = 10

def show_image(image):

    windowname = "Segmentation"
    cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)
    cv2.startWindowThread()
    cv2.imshow(windowname, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def plantSeed(image):

    def drawLines(x, y, pixelType):
        if pixelType == OBJ:
            color, code = OBJCOLOR, OBJCODE
        else:
            color, code = BKGCOLOR, BKGCODE
        cv2.circle(image, (x, y), radius, color, thickness)
        cv2.circle(seeds, (x // SF, y // SF), radius // SF, code, thickness)

    def onMouse(event, x, y, flags, pixelType):
        global drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            drawLines(x, y, pixelType)
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            drawLines(x, y, pixelType)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False

    def paintSeeds(pixelType):

        print ("Planting", pixelType, "seeds")
        global drawing
        drawing = False
        windowname = "Plant " + pixelType + " seeds"
        cv2.namedWindow(windowname, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(windowname, onMouse, pixelType)
        while (1):
            cv2.imshow(windowname, image)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
    
    seeds = np.zeros(image.shape, dtype="uint8")
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = cv2.resize(image, (0, 0), fx=SF, fy=SF)

    radius = 5
    thickness = -1
    global drawing
    drawing = False

    paintSeeds(OBJ)
    paintSeeds(BKG)
    
    return seeds, image  

def imageInput(imagefile, size=(60, 60)):

    pathname = os.path.splitext(imagefile)[0]
    image = cv2.imread(imagefile, cv2.IMREAD_GRAYSCALE)
    sfx, sfy = image.shape[0]/60, image.shape[1]/60
    image = cv2.resize(image, size)
    seeds, _ = plantSeed(image)
    
    return (sfx, sfy), image, seeds

def parseArgs():

    parser = argparse.ArgumentParser()
    parser.add_argument("imagefile")
    parser.add_argument("--size", "-s", 
                        default=60, type=int,
                        help="Defaults to 60x60")
    return parser.parse_args()

def similarity(x, y):

    x = int(x)
    y = int(y)

    diff = abs(x-y) / 255
    sim = 1 - diff

    return sim

def convertToInt(value):
    return int(value*1000)

def constructGraph(image, seeds):

    edgeList = []
    n = seeds.shape[0]
    m = seeds.shape[1]

    source = n*m
    sink = n*m+1

    avgObj = 0
    avgBkg = 0
    objCount = 0
    bkgCount = 0

    for i in range(n):
        for j in range(m):
            if seeds[i][j] == OBJCODE:
                objCount += 1
                avgObj += image[i][j]
            elif seeds[i][j] ==  BKGCODE:
                bkgCount += 1
                avgBkg += image[i][j]
    
    avgBkg /= bkgCount  #ai
    avgObj /= objCount  #bi

    for i in range(n):
        for j in range(m):
            
            ai = (similarity(image[i][j], avgObj) + (1 - similarity(image[i][j], avgBkg)) ) / 2
            bi = 1 - ai

            edgeList.append([source, i*m + j, ai])
            edgeList.append([i*m + j, sink, bi])

            if j+1 < m:
                penalty = similarity(image[i][j], image[i][j+1])
                edgeList.append([i*m + j, i*m + j + 1, penalty])
            if i+1 < n:
                penalty = similarity(image[i][j], image[i+1][j])
                edgeList.append([i*m + j, (i+1)*m + j, penalty])
            if j > 0:
                penalty = similarity(image[i][j], image[i][j-1])
                edgeList.append([i*m + j, i*m + j - 1, penalty])
            if i > 0:
                penalty = similarity(image[i][j], image[i-1][j])
                edgeList.append([i*m + j, (i-1)*m + j, penalty])
    
    file = open('data.txt', 'w')

    v = n*m + 2
    e = len(edgeList)
    file.write(str(v) + ' ' + str(e) + '\n')
    file.write(str(source) + ' ' + str(sink) + '\n')

    for edge in edgeList:
        [u, v, weight] = edge
        text = str(u) + ' ' + str(v) + ' ' + str(convertToInt(weight)) + '\n'
        file.write(text)

    file.close()

def getObj():
    
    os.system('g++ -I ./ fordFulkerson.cpp')
    process = subprocess.Popen(['./a.out'], stdout=subprocess.PIPE)
    dataBytes = process.communicate()[0]
    dataStr   = dataBytes.decode('utf-8')
    genData = list(dataStr.split(' '))
    genData.pop()

    return list(map(int, genData))

if __name__ == "__main__":

    args = parseArgs()
    sf, image, seeds = imageInput(args.imagefile, (args.size, args.size))

    constructGraph(image, seeds)

    obj = getObj()

    image = cv2.imread(args.imagefile)

    for pixel in obj:
        i = int((pixel//60)*sf[0])
        j = int((pixel%60)*sf[1])
        cv2.circle(image, (j, i), 5, (0, 0, 255), -1)
    
    print(len(obj))
    
    cv2.imshow('Output', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()