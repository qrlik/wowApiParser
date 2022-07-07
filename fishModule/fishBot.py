from win32api import GetSystemMetrics
from pynput import keyboard # слушатель ввода
from enum import Enum
import numpy # поддержка многомерных массивов | поддержка высокоуровневых математических функций
import cv2 # openCV
import mss # создания скриншотов
import pyautogui # действия с клавиатурой и с мышкой
import random
import time
import math

class Status(Enum):
    NONE = 0
    PAUSE = 1
    WORK = 2
    SEARCH_COMMON = 3
    SEARCH_FISHUP = 4

bobberCommon = cv2.imread("bobber.png", cv2.IMREAD_GRAYSCALE)
bobberCommonWidth, bobberCommonHeight = bobberCommon.shape[::-1]
bobberAngle = cv2.imread("bobberAngle.png", cv2.IMREAD_GRAYSCALE)
bobberAngleWidth, bobberAngleHeight = bobberAngle.shape[::-1]
errorFrameSize = 15
monitor = {"top": 0, "left": 0, "width": 0, "height": 0}

fishingTimePoint = 0.0
fishingTime = 20.0
bigBaitTimePoint = 0.0
bigBaitTime = 1800.0
smallBaitTimePoint = 0.0
smallBaitTime = 600.0

coreStatus = Status.NONE
corePaused = False

def onPress(key):
    global corePaused
    if key == keyboard.Key.pause or key == keyboard.Key.end:
        corePaused = not corePaused
keyboardListener = keyboard.Listener(on_press=onPress)

def initialize():
    global fishingTimePoint
    global bigBaitTimePoint
    global smallBaitTimePoint
    global coreStatus
    global keyboardListener
    
    resolutionW = GetSystemMetrics(0)
    resolutionH = GetSystemMetrics(1)
    monitor['top'] = int(resolutionH / 4)
    monitor['height'] = int(resolutionH / 2)
    monitor['left'] = int(resolutionW / 4)
    monitor['width'] = int(resolutionW / 2)

    keyboardListener.start() 

    coreStatus = Status.WORK
    time.sleep(10)
    
    pyautogui.press('3')
    bigBaitTimePoint = time.time()
    pyautogui.press('4')
    time.sleep(3)
    smallBaitTimePoint = time.time()

def updateBaits():
    global bigBaitTimePoint
    global smallBaitTimePoint
    currentTime = time.time()
    _bigBaitTime = currentTime - bigBaitTimePoint
    _smallBaitTime = currentTime - smallBaitTimePoint
    if _bigBaitTime > bigBaitTime:
        pyautogui.press('3')
        bigBaitTimePoint = currentTime
    if _smallBaitTime > smallBaitTime:
        pyautogui.press('4')
        time.sleep(3)
        smallBaitTimePoint = time.time()

def startFishing():
    global coreStatus
    global fishingTimePoint

    time.sleep(random.uniform(0.25, 1.5))
    updateBaits()
    pyautogui.press('1')
    fishingTimePoint = time.time()
    time.sleep(random.uniform(0.5, 2))
    coreStatus = Status.SEARCH_COMMON

def isValid():
    global coreStatus

    if corePaused:
        coreStatus = Status.PAUSE
        return False

    _time = time.time() - fishingTimePoint
    if _time > fishingTime:
        coreStatus = Status.WORK
        return False
    return True

def detectStartPoint():
    with mss.mss() as screenshotManager:
        while "searching common bobber":
            if not isValid():
                return
            img = numpy.array(screenshotManager.grab(monitor))
            processedImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(processedImage, bobberCommon, cv2.TM_CCOEFF_NORMED)
            loc = numpy.where(res >= 0.65)

            for point in zip(*loc[::-1]):
                correctWidth = bobberCommonWidth - 2 * errorFrameSize
                correctHeight = bobberCommonHeight - 2 * errorFrameSize
                startX = monitor['left'] + point[0] + random.randint(1, correctWidth)
                startY = monitor['top'] + point[1] + random.randint(1, correctHeight)
                return (startX, startY)

def detectFishUpPoint():
    with mss.mss() as screenshotManager:
        while "waiting fish up":
            if not isValid():
                return
            img = numpy.array(screenshotManager.grab(monitor))
            processedImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(processedImage, bobberAngle, cv2.TM_CCOEFF_NORMED)
            loc = numpy.where(res >= 0.62)

            for point in zip(*loc[::-1]):
                correctWidth = bobberAngleWidth - 2 * errorFrameSize
                correctHeight = bobberAngleHeight - 2 * errorFrameSize
                fishUpX = monitor['left'] + point[0] + errorFrameSize + random.randint(1, correctWidth)
                fishUpY = monitor['top'] + point[1] + errorFrameSize + random.randint(1, correctHeight)
                return (fishUpX, fishUpY)

def handleLoop():
    global coreStatus
    initialize()
    while "Fishing":
        if coreStatus == Status.WORK:
            startFishing()
        elif coreStatus == Status.PAUSE:
            if corePaused:
                time.sleep(3)
            else:
                coreStatus = Status.WORK
        elif coreStatus == Status.SEARCH_COMMON:
            startPoint = detectStartPoint()
            if not startPoint:
                continue
            coreStatus = Status.SEARCH_FISHUP
            startX, startY = startPoint
            pyautogui.moveTo(x=startPoint[0], y=startPoint[1], duration=random.uniform(0.5, 1))
        elif coreStatus == Status.SEARCH_FISHUP:
            fishPoint = detectFishUpPoint()
            if not fishPoint:
                continue
            coreStatus = Status.WORK
            fishUpX, fishUpY = fishPoint
            if math.sqrt((startX - fishUpX) ** 2 + (startY - fishUpY) ** 2) < 50:
                fishUpX = startX
                fishUpY = startY
            pyautogui.click(x=fishUpX, y=fishUpY, button='right', duration=random.uniform(0.1, 1.0), tween=pyautogui.easeOutQuad)

def main():
    handleLoop()

if __name__ == '__main__':
    main()