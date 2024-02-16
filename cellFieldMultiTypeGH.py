import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import math
import Grasshopper as gh
import random

#convert inColor from a tree into a 2D List
grid = th.tree_to_list(inType, lambda inType: inType)

#global lists for output
posList = []
aimList = []
connectList = []
typeList = []



#loop through and find neighbor counts for our pts
for x in range(len(grid)):
    for y in range(len(grid[x])):
        if grid[x][y] != 0:
            #create a position vector and put in posList
            pos = rs.CreateVector([x*cellSize, y*cellSize, 0])
            posList.append(pos)
            #create an integer for storing the number of neighbors
            neighborCnt = 0
            vec = [0,0,0]  
            #0 = [-1,0,0], 1 = [0,-1,0], 2 = [0,1,0], 3 = [1,0,0]
            # horizontal line = [1,0,0,1], vertical line = [0,1,1,0]
            onTest = [0,0,0,0]
            testCnt = 0
            #loop through our neighbors
            for i in range(-1,2):
                for j in range(-1,2):
                    #check only the cross
                    if abs(i) != abs(j):
                        x1 = x+i
                        y1 = y+j
                        if x1 >= 0 and x1 < len(grid) and y1 >= 0 and y1 < len(grid[x]):
                            if grid[x1][y1] != 0:
                                neighborCnt+=1
                                vec = rs.VectorAdd(vec,[i,j,0])
                                onTest[testCnt] = 1
                        testCnt += 1
            if neighborCnt == 0:
                connectList.append(0)
                vec = [1,0,0]
                
            if neighborCnt == 1:
                connectList.append(0)
                
            #calculate my aim vector based on my neighborCnt
            if neighborCnt == 2:
                if abs(vec[0]) >.5 and abs(vec[1]) > .5:
                    vec = rs.VectorUnitize(vec)
                    vec = rs.VectorRotate(vec, -45, [0,0,1])
                    vec = rs.VectorUnitize(vec)
                    connectList.append(2)
                else:
                    # horizontal line = [1,0,0,1], vertical line = [0,1,1,0]
                    neighborCnt = 1
                    if onTest[0] == 1:
                        vec = [1,0,0]
                    else:
                        vec = [0,1,0]
                    connectList.append(1)
            if neighborCnt == 3:
                vec = rs.VectorScale(vec,1/3)
                vec = rs.VectorUnitize(vec)
                connectList.append(3)
            if neighborCnt == 4:                
                vec = [1,0,0]
                connectList.append(4)            
            outVec = rs.CreateVector(vec)
            aimList.append(outVec)
            typeList.append(grid[x][y]-1)

