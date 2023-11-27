import cv2
import os
import glob
import shutil
import configparser
from tkinter import filedialog

from lib.detector import Detector
from lib.filemanager import FileManager

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    App = Detector(".\\setting\\config.ini")
    Manager = FileManager(".\\setting\\config.ini")

    photolist = glob.glob(".\\test_image\\*")

    for photo in photolist:
        App.input = photo
        result = App.detect()
        print(result)