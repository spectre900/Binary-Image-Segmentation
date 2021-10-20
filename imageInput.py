import os
import cv2
import time
import argparse
import subprocess
import numpy as np

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
        imageOrg = cv2.imread(imagefile, cv2.IMREAD_GRAYSCALE)

        self.image = cv2.cvtColor(imageOrg, cv2.COLOR_GRAY2RGB)
        self.seeds = np.zeros(imageOrg.shape, dtype="uint8")

        sfx, sfy = imageOrg.shape[0] / size[0], imageOrg.shape[1] / size[1]

        self.paintSeeds(FRG)
        self.paintSeeds(BKG)

        self.seeds = cv2.resize(self.seeds, size)

        return (sfx, sfy), cv2.resize(imageOrg, size), self.seeds


class ImageSegment:
    def __init__(self, image, seeds):

        self.edgeList = []
        self.factor = 1000
        self.image = image
        self.seeds = seeds
        self.radius = 5
        self.thickness = -1

    def similarity(self, x, y):

        x = int(x)
        y = int(y)
        diff = abs(x - y) / 255
        sim = 1 - diff
        return sim

    def convertToInt(self, value):
        return int(value * self.factor)

    def constructGraph(self):

        n = self.seeds.shape[0]
        m = self.seeds.shape[1]

        source = n * m
        sink = n * m + 1

        avgFrg = 0
        avgBkg = 0
        frgCount = 0
        bkgCount = 0

        for i in range(n):
            for j in range(m):
                if self.seeds[i][j] == FRGCODE:
                    frgCount += 1
                    avgFrg += image[i][j]
                elif self.seeds[i][j] == BKGCODE:
                    bkgCount += 1
                    avgBkg += image[i][j]

        avgBkg /= bkgCount
        avgFrg /= frgCount

        for i in range(n):
            for j in range(m):

                ai = (
                    self.similarity(self.image[i][j], avgFrg)
                    + (1 - self.similarity(self.image[i][j], avgBkg))
                ) / 2
                bi = 1 - ai

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
        genData.pop()

        return algo, list(map(int, genData))

    def displayResults(self, sf, size, imagefile):

        algos = ["fordFulkerson", "edmondKarp", "scaling"]
        start = time.time()
        algo, frg = self.getForeground(algos[0])
        end = time.time()

        image = cv2.imread(imagefile)

        for pixel in frg:
            i = int((pixel // size[0]) * sf[0])
            j = int((pixel % size[1]) * sf[1])
            cv2.circle(image, (j, i), self.radius, FRGCOLOR, self.thickness)

        cv2.imshow("Segmentation using " + algo, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        runtime = end - start
        print("Runtime:", round(runtime, 5), "Secs")


def parseArgs():

    parser = argparse.ArgumentParser()
    parser.add_argument("imagefile")
    parser.add_argument("--size", "-s", default=60, type=int, help="Defaults to 60x60")
    return parser.parse_args()


if __name__ == "__main__":

    args = parseArgs()

    imageProcess = ImageProcess()
    sf, image, seeds = imageProcess.imageInput(args.imagefile, (args.size, args.size))

    imageSegment = ImageSegment(image, seeds)
    imageSegment.constructGraph()
    imageSegment.writeData("data.txt")
    imageSegment.displayResults(sf, (args.size, args.size), args.imagefile)
