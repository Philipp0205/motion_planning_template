import numpy as np
from PIL import Image, ImageTk, ImageColor
from io import BytesIO
from tkinter import ttk, Canvas, NW
import os
from configspace import Configspace
from utils import isPixelWhite


class Workspace:
    def __init__(self, robotImagePath, envImagePath, root):
        self.root = root
        self.envImage = Image.open(envImagePath).convert('1')
        self.envArray = np.array(self.envImage)
        self.envPhoto = ImageTk.PhotoImage(self.envImage)

        self.robotImage = Image.open(robotImagePath).convert('1')
        self.robotArray = np.array(self.robotImage)
        self.robotPhoto = ImageTk.PhotoImage(self.robotImage)

        self.label = ttk.Label(root, image=self.envPhoto)

        self.currentPos = (0, 0)
        self.isInitialize = False

    def drawAll(self, xCurrent, yCurrent, xInit=-1, yInit=-1, xGoal=-1, yGoal=-1):
        self.currentPos = xCurrent, yCurrent
        self.imageToDraw = self.envImage.copy()
        if xInit > -1: self.imageToDraw.paste(self.robotImage.copy(), (xInit, yInit))
        if xGoal > -1: self.imageToDraw.paste(self.robotImage.copy(), (xGoal, yGoal))
        self.imageToDraw.paste(self.robotImage.copy(), (self.currentPos[0], self.currentPos[1]))
        self.photoToDraw = ImageTk.PhotoImage(self.imageToDraw)
        self.label.configure(image=self.photoToDraw)
        self.label.image = self.photoToDraw
        self.label.pack(side="bottom", fill="both", expand="yes")

    def isRobotInCollision(self, x, y):
        difference = int(self.robotImage.size[0]/2) -10
        # width of robot
        x_edges = x - difference, x + difference
        # heigh of robot
        y_edges = y - difference, y + difference

        # Because we add to x and y out of bounce is possible
        def out_of_bounce(x, y):
            return y >= len(self.envArray) or x >= len(self.envArray[0])

        for i in range(x_edges[0], x_edges[1]):
            for j in range(y_edges[0], y_edges[1]):
                if i < len(self.envArray) or j < len(self.envArray[0]):
                    if not out_of_bounce(i, j):
                        if not self.envArray[j, i]:
                            return True
                    else:
                        return False

    def isInCollision(self, x, y):
        return self.envArray[y, x]

    def isInCollissionArea(self, x, y):
        x += 24
        y += 35

        difference = int(self.robotImage.size[0] / 2) - 10
        # width of robot
        x_edges = x - difference, x + difference
        # heigh of robot
        y_edges = y - difference, y + difference

        # Because we add to x and y out of bounce is possible
        def out_of_bounce(x, y):
            return y >= len(self.envArray) or x >= len(self.envArray[0])

        for i in range(x_edges[0], x_edges[1]):
            for j in range(y_edges[0], y_edges[1]):
                if i < len(self.envArray) or j < len(self.envArray[0]):
                    if not out_of_bounce(i, j):
                        if not self.envArray[j, i]:
                            return True
                    else:
                        return False


