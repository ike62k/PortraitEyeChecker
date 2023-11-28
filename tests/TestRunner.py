import cv2
import os
import glob
import sys
import shutil
import configparser
from tkinter import filedialog

sys.path.append(os.path.dirname(__file__).rsplit("\\", 1)[0])

from PortraiteEyeChecker.libs.detector import Detector
from PortraiteEyeChecker.libs.filemanager import FileManager

if __name__ == "__main__":
    os.chdir(f"{os.path.dirname(__file__).rsplit("\\", 1)[0]}")
    App = Detector(".\\config\\config.ini")
    Manager = FileManager(".\\config\\config.ini")

    photolist = glob.glob(".\\test_image\\*")

    for photo in photolist:
        App.input = photo
        result = App.detect()
        print(result)
        