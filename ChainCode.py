import os,sys,math

class CCimage:
    zeroFramedAry=[]
    numRows=numCols=0
    def __init__(self, input_file_name):
        order=0
        with open(input_file_name, 'r') as input_file:
            for line in input_file:
                if order==0:
                    header = (list(map(str, line.split(' '))))
                    self.numRows = int(header[0])
                    self.numCols = int(header[1])
                    minVal = int(header[2])
                    maxVal = int(header[3])
                    self.zeroFramedAry = [[0] * (self.numCols+2) for i in range(self.numRows+2)]
                else:
                    temp_data = list(map(str, line.split(' ')))
                    for i in range(self.numCols):
                        self.zeroFramedAry[order][i+1] = int(temp_data[i])
                order += 1
        input_file.close()

class CCproperty:
    maxCC=0
    property = []
    def __init__(self, input_file_name):
        with open(input_file_name, 'r') as input_file:
            for line in input_file:
                temp_data =(list(map(int, line.split(' '))))
                self.property.append(temp_data)
                self.maxCC += 1
        input_file.close()


class point(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def equal(self, p):
        if(self.row==p.row and self.col==p.col):
            return True
        else:
            return False

class Chain:
    __neighborAry = [[0] for i in range(8)]
    __neighborCoord = [point(0,0) for i in range(8)]
    __nextDirTable = [6,0,0,2,2,4,4,6]
    __currentCC=lastQ=nextQ=0
    chain_data = []

    def __init__(self,image, pp):
        self.chain_data = [[] * (pp.maxCC + 1)]
        for i in range(pp.maxCC):
            self.currentCC=i+1
            minRowOffset = pp.property[i][2]
            maxRowOffset = pp.property[i][4]
            minColOffset = pp.property[i][3]
            maxColOffset = pp.property[i][5]
            startRow = minRowOffset
            startCol = minColOffset
            while(image.zeroFramedAry[startRow][startCol]!=self.currentCC):
                startCol+=1
            self.chain_data.append(str(startRow)+" "+str(startCol)+" "+str(self.currentCC)+" ")
            startP = point(startRow, startCol)
            currentP = startP
            nextP = point(0,0)
            lastQ = 4
            while(not(startP.equal(nextP))):
                self.loadNeighbors(image, currentP.row, currentP.col)
                nextQ = (lastQ+1)%8
                Pchain = self.findNextP(currentP,nextQ)
                nextP = self.__neighborCoord[Pchain]
                self.chain_data[self.currentCC]+=str(Pchain)+" "
                currentP=nextP
                lastQ=self.__nextDirTable[(Pchain+7)%8]

    def loadNeighborCoord(self, r, c):
        self.__neighborCoord[0].row = r
        self.__neighborCoord[0].col = c+1
        self.__neighborCoord[1].row = r-1
        self.__neighborCoord[1].col = c+1
        self.__neighborCoord[2].row = r-1
        self.__neighborCoord[2].col = c
        self.__neighborCoord[3].row = r-1
        self.__neighborCoord[3].col = c-1
        self.__neighborCoord[4].row = r
        self.__neighborCoord[4].col = c-1
        self.__neighborCoord[5].row = r+1
        self.__neighborCoord[5].col = c-1
        self.__neighborCoord[6].row = r+1
        self.__neighborCoord[6].col = c
        self.__neighborCoord[7].row = r+1
        self.__neighborCoord[7].col = c+1

    def findNextP(self, p, q):
        row=p.row
        col=p.col
        self.loadNeighborCoord(row,col)
        for i in range(8):
            if(self.__neighborAry[(q+i)%8]==self.currentCC):
                return (q+i)%8
        return 0

    def loadNeighbors(self, image, row, col):
        self.__neighborAry[0] = image.zeroFramedAry[row][col + 1]
        self.__neighborAry[1] = image.zeroFramedAry[row - 1][col + 1]
        self.__neighborAry[2] = image.zeroFramedAry[row - 1][col]
        self.__neighborAry[3] = image.zeroFramedAry[row - 1][col - 1]
        self.__neighborAry[4] = image.zeroFramedAry[row][col - 1]
        self.__neighborAry[5] = image.zeroFramedAry[row + 1][col - 1]
        self.__neighborAry[6] = image.zeroFramedAry[row + 1][col]
        self.__neighborAry[7] = image.zeroFramedAry[row + 1][col + 1]

image = CCimage(sys.argv[1])
pp = CCproperty(sys.argv[2])
mychaincode = Chain(image,pp)
output_file=open(sys.argv[3],'w')
for i in range(1, pp.maxCC+1):
    output_file.write(mychaincode.chain_data[i])
    output_file.write('\n')
output_file.close()
print("All work done!")



