#!/usr/bin/python
#Title:Support file to generate features 
#Inspired from https://github.com/avisingh599/face-rating
#Date:25/10/2015

import math,itertools,numpy

def findRatio(points):

    ''' Function to find ratios '''

    x=[0]*4
    y=[0]*4
    for i in range(4):
        x[i]=points[(2*i)] 
        y[i]=points[(2*i)+1]

    dist1 = math.sqrt((x[0]-x[1])**2 + (y[0]-y[1])**2)
    dist2 = math.sqrt((x[2]-x[3])**2 + (y[2]-y[3])**2)
    ratio = dist1/dist2

    return ratio


def generateFeatures(landmarkCoordinates):

    ''' Function to generate features '''

    keyPoints = [18, 22, 23, 27, 37, 40, 43, 46, 28, 32, 34, 36, 5, 9, 13, 49, 55, 52, 58,61,63,65,67]
    combinations = itertools.combinations(keyPoints, 4)
    pointIndices1 = []
    pointIndices2 = []
    pointIndices3 = []
    pointIndices4 = []

    for combination in combinations:
        pointIndices1.append(combination[0])
        pointIndices2.append(combination[1])
        pointIndices3.append(combination[2])
        pointIndices4.append(combination[3])

        pointIndices1.append(combination[0])
        pointIndices2.append(combination[2])
        pointIndices3.append(combination[1])
        pointIndices4.append(combination[3])

        pointIndices1.append(combination[0])
        pointIndices2.append(combination[3])
        pointIndices3.append(combination[1])
        pointIndices4.append(combination[2])

    Features = numpy.zeros((1, len(pointIndices1)))
    ratios = [];

    for i in range(0, len(pointIndices1)):
        x1 = landmarkCoordinates[2*(pointIndices1[i]-1)]
        y1 = landmarkCoordinates[2*pointIndices1[i] - 1]
        x2 = landmarkCoordinates[2*(pointIndices2[i]-1)]
        y2 = landmarkCoordinates[2*pointIndices2[i] - 1]

        x3 = landmarkCoordinates[2*(pointIndices3[i]-1)]
        y3 = landmarkCoordinates[2*pointIndices3[i] - 1]
        x4 = landmarkCoordinates[2*(pointIndices4[i]-1)]
        y4 = landmarkCoordinates[2*pointIndices4[i] - 1]

        points = [x1, y1, x2, y2, x3, y3, x4, y4]
        ratios.append(findRatio(points))

    Features = numpy.asarray(ratios)

    return Features
