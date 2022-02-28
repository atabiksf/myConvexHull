import numpy as np
import copy
from math import atan2, pi

def myConvexHull(bucket):
    # arr return initialization
    arrOut = []
    arrUpper = []
    arrOutUpper = []
    arrBottom = []
    arrOutBottom = []
    # sort element of bucket
    bucket = bucket[np.lexsort(np.transpose(bucket)[::-1])]
    # initialize pExtreme
    pMin = bucket[0]
    pMax = bucket[len(bucket)-1]
    # move upper and bottom point
    for point in bucket:
        det = getDeterminant(pMin,pMax,point)
        if(det > 0):
            arrUpper.append(point)
        elif(det < 0):
            arrBottom.append(point)
    # find max in upper and subHullUpper
    maxUpper = pMax
    distance = 0
    idx = 1
    while idx < len(arrUpper)-1:
        point = arrUpper[idx]
        tempDist = getDistance(pMin,pMax,point)
        if (tempDist > distance):
            maxUpper = point
            distance = tempDist
        elif (tempDist == distance):
            if(getAngle(pMin,point,pMax)>getAngle(pMin,maxUpper,pMax)):
                maxUpper = point
        idx += 1
    if(np.all(maxUpper != pMax)):
        arrUpper.insert(0,pMin)
        arrUpper.insert(len(arrUpper),pMax)
        arrOutUpper.append(pMin)
        arrOutUpper.extend(subHull(arrUpper,maxUpper,True))
        arrOutUpper.append(pMax)
    else:
        arrOut.append(maxUpper)
    # find max in bottom and subHullBottom
    maxBottom = pMin
    distance = 0
    idx = 1
    while idx < len(arrBottom)-1:
        point = arrBottom[idx]
        tempDist = getDistance(pMin,pMax,point)
        if (tempDist > distance):
            maxBottom = point
            distance = tempDist
        elif (tempDist == distance):
            if(getAngle(pMin,point,pMax)>getAngle(pMin,maxBottom,pMax)):
                maxBottom = point
        idx += 1
    if(np.all(maxBottom != pMin)):
        arrBottom.insert(0,pMin)
        arrBottom.insert(len(arrBottom),pMax)
        arrOutBottom.append(pMin)
        arrOutBottom.extend(subHull(arrBottom,maxBottom,False))
        arrOutBottom.append(pMax)
    else:
        arrOut.append(maxBottom)
    
    return arrOutUpper, arrOutBottom

def subHull(arr, pIn, boolean): #boolean true if subHullUpper and false if subHullBottom
    arrLeft = []
    arrRight = []
    arrOut = []

    # split arr at pIn
    pIdx = 0
    while (not(arr[pIdx][0] == pIn[0] and arr[pIdx][1] == pIn[1])):
        arrLeft.append(arr[pIdx])
        pIdx += 1
    arrLeft.append(arr[pIdx])
    while (pIdx < len(arr)):
        arrRight.append(arr[pIdx])
        pIdx += 1
    # do arrLeft
    pMin = arrLeft[0]
    pMax = arrLeft[len(arrLeft)-1]
    maxLeft = pMax
    distance = 0
    # remove point above the line
    if(boolean):
        idx = 1
        while idx < len(arrLeft)-1:
            point = arrLeft[idx]
            det = getDeterminant(pMin,pMax,point)
            if(det <= 0):
                arrLeft = np.delete(arrLeft,idx,axis=0)
                idx -= 1
            idx += 1
    else:
        idx = 1
        while idx < len(arrLeft)-1:
            point = arrLeft[idx]
            det = getDeterminant(pMin,pMax,point)
            if(det >= 0):
                arrLeft = np.delete(arrLeft,idx,axis=0)
                idx -= 1
            idx += 1
    # find max
    idx = 1
    while idx < len(arrLeft)-1:
        point = arrLeft[idx]
        tempDist = getDistance(pMin,pMax,point)
        if (tempDist > distance):
            maxLeft = point
            distance = tempDist
        elif (tempDist == distance):
            if(getAngle(pMin,point,pMax)>getAngle(pMin,maxLeft,pMax)):
                maxLeft = point
        idx += 1
    # subHull
    if(np.all(maxLeft != pMax)):
        if(boolean) : arrOut.extend(subHull(arrLeft,maxLeft,True))
        else : arrOut.extend(subHull(arrLeft,maxLeft,False))
        arrOut.append(pMax)
    else:
        arrOut.append(maxLeft)
    # do arrRight
    pMin = arrRight[0]
    pMax = arrRight[len(arrRight)-1]
    maxRight = pMin
    distance = 0
    # remove point above the line
    if(boolean) :
        idx = 1
        while idx < len(arrRight)-1:
            point = arrRight[idx]
            det = getDeterminant(pMin,pMax,point)
            if(det <= 0):
                arrRight = np.delete(arrRight,idx, axis = 0)
                idx -= 1
            idx += 1
    else:
        idx = 1
        while idx < len(arrRight)-1:
            point = arrRight[idx]
            det = getDeterminant(pMin,pMax,point)
            if(det >= 0):
                arrRight = np.delete(arrRight,idx, axis = 0)
                idx -= 1
            idx += 1
    # find max
    idx = 1
    while idx < len(arrRight)-1:
        point = arrRight[idx]
        tempDist = getDistance(pMin,pMax,point)
        if (tempDist > distance):
            maxRight = point
            distance = tempDist
        elif (tempDist == distance):
            if(getAngle(pMin,point,pMax)>getAngle(pMin,maxRight,pMax)):
                maxRight = point
        idx += 1
    # subHull
    if(np.all(maxRight != pMin)):
        if(boolean) : arrOut.extend(subHull(arrRight,maxRight,True))
        else : arrOut.extend(subHull(arrRight,maxRight,False))
        arrOut.append(pMin)
    else:
        arrOut.append(maxRight)
    # make results
    res = np.unique(arrOut,axis = 0)

    return res

def getAngle(A,B,C):
    # Mengembalikan besar sudut ABC pada titik B dalam derajat
    Ax, Ay = A[0]-B[0], A[1]-B[1]
    Cx, Cy = C[0]-B[0], C[1]-B[1]
    a = atan2(Ay, Ax)
    c = atan2(Cy, Cx)
    if a < 0: a += pi*2
    if c < 0: c += pi*2

    return (pi*2 + c - a) if a > c else (c - a)

def getDeterminant(A,B,C):
    # Mengembalikan determinan [[Ax,Ay,1],[Bx,By,1],[Cx,Cy,1]]
    aCopy = np.append(A,[1])
    bCopy = np.append(B,[1])
    cCopy = np.append(C,[1])

    matrix = np.array([aCopy,bCopy,cCopy])
    det = np.linalg.det(matrix)

    return det

def getDistance(A,B,C):
    # Mengembalikan jarak dari titik C ke garis AB secara tegak lurus
    p = copy.deepcopy(A)
    q = copy.deepcopy(B)
    r = copy.deepcopy(C)
    p = np.array(p)
    q = np.array(q)
    r = np.array(r)

    dist = np.cross(q-p,r-p)/np.linalg.norm(q-p)

    return abs(dist)
