import os
import cv2
import time
import shutil
import argparse
import subprocess
import numpy as np
import matplotlib.pyplot as plt

FRG, BKG = "FRG", "BKG"
FRGCODE, BKGCODE = 1, 2
FRGCOLOR, BKGCOLOR = (0, 0, 255), (0, 255, 0)


class ImageProcess:
    def __init__(self):

        self.radius = 5
        self.thickness = -1
        self.drawing = False

    def drawLines(self, x, y, pixelType):

        if pixelType == FRG:
            color, code = FRGCOLOR, FRGCODE
        else:
            color, code = BKGCOLOR, BKGCODE
        cv2.circle(self.image, (x, y), self.radius, color, self.thickness)
        cv2.circle(self.seeds, (x, y), self.radius, code, self.thickness)

    def onMouse(self, event, x, y, flags, pixelType):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.drawLines(x, y, pixelType)
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            self.drawLines(x, y, pixelType)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False

    def paintSeeds(self, pixelType):

        print("Planting", pixelType, "seeds")
        self.drawing = False
        windowname = "Plant " + pixelType + " seeds"
        cv2.namedWindow(windowname, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(windowname, self.onMouse, pixelType)
        while 1:
            cv2.imshow(windowname, self.image)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

    def imageInput(self, imagefile, size):

        pathname = os.path.splitext(imagefile)[0]

        self.image = cv2.imread(imagefile)
        imageOrg = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.seeds = np.zeros(imageOrg.shape, dtype="uint8")

        sfx, sfy = imageOrg.shape[0] / size[0], imageOrg.shape[1] / size[1]

        self.paintSeeds(FRG)
        self.paintSeeds(BKG)

        self.seeds = cv2.resize(self.seeds, size)

        return (sfx, sfy), cv2.resize(cv2.imread(imagefile), size), self.seeds 


class ImageSegment:
    def __init__(self, image, seeds):

        self.edgeList = []
        self.factor = 1000
        self.image = image
        self.seeds = seeds
        self.radius = 5
        self.thickness = -1

    def similarity(self, x, y):

        sim = 0
        for i in range(3):
            X = int(x[i])
            Y = int(y[i])
            diff = abs(X - Y) / 255
            sim += 1 - diff
        sim /= 3

        return sim

    def convertToInt(self, value):
        return int(value * self.factor)

    def constructGraph(self):

        n = self.seeds.shape[0]
        m = self.seeds.shape[1]

        source = n * m
        sink = n * m + 1

        frgSeeds = []
        bkgSeeds = []

        for i in range(n):
            for j in range(m):
                if self.seeds[i][j] == FRGCODE:
                    frgSeeds.append(self.image[i][j])
                elif self.seeds[i][j] == BKGCODE:
                    bkgSeeds.append(self.image[i][j])

        for i in range(n):
            for j in range(m):

                ai = 0
                ai1 = ai2 = 0
                for seed in frgSeeds:
                    ai1 += (
                        self.similarity(self.image[i][j], seed)
                    )
                ai1 /= len(frgSeeds)

                for seed in bkgSeeds:
                    ai2 += (
                        1 - self.similarity(self.image[i][j], seed)
                    )
                ai2 /= len(bkgSeeds)

                ai = (ai1 + ai2) / 2
                bi = 1 - ai

                if (i + j) % 10 == 0:
                    print(ai, bi)

                self.edgeList.append([source, i * m + j, ai])
                self.edgeList.append([i * m + j, sink, bi])

                if j + 1 < m:
                    penalty = self.similarity(self.image[i][j], self.image[i][j + 1])
                    self.edgeList.append([i * m + j, i * m + j + 1, penalty])
                if i + 1 < n:
                    penalty = self.similarity(self.image[i][j], self.image[i + 1][j])
                    self.edgeList.append([i * m + j, (i + 1) * m + j, penalty])
                if j > 0:
                    penalty = self.similarity(self.image[i][j], self.image[i][j - 1])
                    self.edgeList.append([i * m + j, i * m + j - 1, penalty])
                if i > 0:
                    penalty = self.similarity(self.image[i][j], self.image[i - 1][j])
                    self.edgeList.append([i * m + j, (i - 1) * m + j, penalty])

    def writeData(self, fileName):

        file = open(fileName, "w")

        n = self.seeds.shape[0]
        m = self.seeds.shape[1]

        source = n * m
        sink = n * m + 1

        v = n * m + 2
        e = len(self.edgeList)

        file.write(str(v) + " " + str(e) + "\n")
        file.write(str(source) + " " + str(sink) + "\n")

        for edge in self.edgeList:
            [u, v, weight] = edge
            text = str(u) + " " + str(v) + " " + str(self.convertToInt(weight)) + "\n"
            file.write(text)

        file.close()

    def getForeground(self, algo="fordFulkerson"):

        os.system("g++ -I ./ " + algo + ".cpp")
        process = subprocess.Popen(["./a.out"], stdout=subprocess.PIPE)
        dataBytes = process.communicate()[0]
        dataStr = dataBytes.decode("utf-8")
        genData = list(dataStr.split(" "))

        runtime = float(genData[-1])
        genData.pop()

        return algo, list(map(int, genData)), runtime

    def createBarPlot(self, algos, runtimes):
        plt.bar(algos, runtimes, width = 0.4)
        plt.xlabel('Algorithms used')
        plt.ylabel('Runtime')
        plt.title('Execution times of different algorithms for Binary Image Segmentation')
        plt.savefig('./Results/plot.jpg')

    def displayResults(self, sf, size, imagefile):

        algos = ["fordFulkerson", "edmondKarp", "scaling", "dinic"]
        runtimes = []

        directory = './Results'
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

        file = open("./Results/results.txt", "w")

        image = cv2.imread(imagefile)
        cv2.imwrite("./Results/image.jpg", image)

        for algo in algos:
            algo, frg, runtime = self.getForeground(algo)

            image = cv2.imread(imagefile)

            for pixel in frg:
                i = int((pixel // size[0]) * sf[0])
                j = int((pixel % size[1]) * sf[1])
                cv2.circle(image, (j, i), self.radius, FRGCOLOR, self.thickness)

            cv2.imshow("Segmentation using " + algo, image)
            cv2.imwrite("./Results/" + str(algo) + ".jpg", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            print(
                "Maxflow Runtime using " + str(algo) + ": ", round(runtime, 5), "Secs"
            )

            file.write(str(round(runtime, 5)) + "\n")
            runtimes.append(runtime)

        file.close()
        self.createBarPlot(algos, runtimes)
        subprocess.Popen(["python3", "gui2.py"])


def parseArgs():

    parser = argparse.ArgumentParser()
    parser.add_argument("--size", "-s", default=60, type=int, help="Defaults to 60x60")
    return parser.parse_args()


def getFilename():

    process = subprocess.Popen(["python3", "gui1.py"], stdout=subprocess.PIPE)
    dataBytes = process.communicate()[0]
    dataStr = dataBytes.decode("utf-8")
    filename = dataStr.strip()

    return filename


if __name__ == "__main__":

    args = parseArgs()

    imageProcess = ImageProcess()

    imagefile = getFilename()

    sf, image, seeds = imageProcess.imageInput(imagefile, (args.size, args.size))

    imageSegment = ImageSegment(image, seeds)
    imageSegment.constructGraph()
    imageSegment.writeData("data.txt")
    imageSegment.displayResults(sf, (args.size, args.size), imagefile)
