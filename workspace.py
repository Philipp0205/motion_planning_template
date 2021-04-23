import numpy as np
from PIL import Image, ImageTk, ImageColor, ImageDraw
from io import BytesIO
from tkinter import ttk, Canvas, NW
import os

from PIL.ImageEnhance import Color

from configspace import Configspace
from utils import  isPixelWhite
from utils import  isPixelBlack


class Workspace:
    def __init__(self, robotImagePath, envImagePath, root):
        
        self.root = root
        self.envImage = Image.open(envImagePath).convert('1')
        self.envArray = np.array(self.envImage)
        self.envPhoto = ImageTk.PhotoImage(self.envImage)

        self.envImageDebug= Image.open(envImagePath)
        self.envPhotoDebug= ImageTk.PhotoImage(self.envImageDebug)

        self.robotImage = Image.open(robotImagePath).convert('1')
        self.robotArray = np.array(self.robotImage)
        self.robotPhoto = ImageTk.PhotoImage(self.robotImage)

        # self.label = ttk.Label(root, image = self.envPhoto)
        self.label = ttk.Label(root, image = self.envPhotoDebug)

        self.currentPos = (0,0)
        self.robotEdges = (0,0), (0,24), (24,24), (24,0)
        self.isInitialize = False

    def drawAll (self,xCurrent,yCurrent,xInit=-1,yInit=-1,xGoal=-1,yGoal=-1):
        self.currentPos=xCurrent,yCurrent
        self.imageToDraw = self.envImageDebug.copy()
        if xInit>-1: self.imageToDraw.paste(self.robotImage.copy(),(xInit,yInit))
        if xGoal>-1: self.imageToDraw.paste(self.robotImage.copy(),(xGoal,yGoal))

        self.imageToDraw.paste(self.robotImage.copy(),(self.currentPos[0],self.currentPos[1]))
        self.photoToDraw = ImageTk.PhotoImage(self.imageToDraw)
        self.label.configure(image=self.photoToDraw)
        self.label.image = self.photoToDraw

        self.label.pack(side = "bottom", fill = "both", expand = "yes")

    def drawWorkspace(self, xCurrent, yCurrent):
        self.currentPos=xCurrent, yCurrent
        self.imageToDraw = self.envImage.copy()
        self.photoToDraw = ImageTk.PhotoImage(self.imageToDraw)

        self.label.configure(image=self.photoToDraw)
        self.label.image = self.photoToDraw

        self.label.pack(side = "bottom", fill = "both", expand = "yes")

    def drawRobots(self, xInit, yInit, xGoal, yGoal):
        self.imageToDraw.paste(self.robotImage.copy(),(self.currentPos[0],self.currentPos[1]))
        self.photoToDraw = ImageTk.PhotoImage(self.imageToDraw)
        self.drawWorkspace(self.currentPos[0], self.currentPos[1])

        if xInit > -1: self.imageToDraw.paste(self.robotImage.copy(), (xInit, yInit))
        if xGoal > -1: self.imageToDraw.paste(self.robotImage.copy(), (xGoal, yGoal))

        self.imageToDraw.paste(self.robotImage.copy(), (self.currentPos[0], self.currentPos[1]))

    def reDrawEnviromentForDebugging(self):
        #self.label = ttk.Label(self.root, image = self.envPhotoDebug)
        self.label.image = None

        self.label.configure(image=self.photoToDraw)
        self.label.image = self.photoToDraw

        self.label.pack(side="bottom", fill="both", expand="yes")

        draw = ImageDraw.Draw(self.envImageDebug)

    def calculateRobotEdgesFromCurrentPosition(self,x,y):
        robotEdges = (x+24,y), (x, y+24), (x-24,y), (x,y-24)
        return robotEdges;


    # Checks if robot is in collision
    def isInCollision(self,x,y):
        self.reDrawEnviromentForDebugging()
        draw = ImageDraw.Draw(self.envImageDebug)
        edges = self.calculateRobotEdgesFromCurrentPosition(x,y)

        for edge in self.calculateRobotEdgesFromCurrentPosition(x,y):
            # true = in colisison
            if not self.envArray[edge[1], edge[0]]:
                return True
        return False