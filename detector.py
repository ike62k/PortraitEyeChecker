import cv2
import os
import glob
import shutil
import configparser
from tkinter import filedialog

class Detector():
    def __init__(self,config_path: str) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.apply_config()

    @property
    def input(self) -> str:
        return self.__input
    @input.setter
    def input(self, inputfile: str):
        self.__input = cv2.cvtColor(cv2.imread(inputfile), cv2.COLOR_BGR2GRAY)
        height = self.__input.shape[0]
        width = self.__input.shape[1]
        if height > 3000 or width > 3000:
            ratio = 3000/(max(height, width))
            self.__input = cv2.resize(self.__input, dsize=None, fx=ratio, fy=ratio)

    @property
    def face_model(self) -> str:
        return self.__face_model
    @face_model.setter
    def face_model(self,model: str):
        self.__face_model = model

    @property
    def eye_model(self) -> str:
        return self.__eye_model
    @eye_model.setter
    def eye_model(self,model: str):
        self.__eye_model = model

    @property
    def face_scaleFactor(self) -> float:
        return self.__face_scaleFactor
    @face_scaleFactor.setter
    def face_scaleFactor(self,scaleFactor: float):
        self.__face_scaleFactor = scaleFactor

    @property
    def face_minNeighbors(self) -> int:
        return self.__face_minNeighbors
    @face_minNeighbors.setter
    def face_minNeighbors(self,minNeighbors: int):
        self.__face_minNeighbors = minNeighbors

    @property
    def eye_scaleFactor(self) -> float:
        return self.__eye_scaleFactor
    @eye_scaleFactor.setter
    def eye_scaleFactor(self,scaleFactor: float):
        self.__eye_scaleFactor = scaleFactor

    @property
    def eye_minNeighbors(self) -> int:
        return self.__eye_minNeighbors
    @eye_minNeighbors.setter
    def eye_minNeighbors(self,minNeighbors: int):
        self.__eye_minNeighbors = minNeighbors

    def apply_config(self):
        self.face_model = self.config["USER"]["face_model"]
        self.eye_model = self.config["USER"]["eye_model"]
        self.face_scaleFactor = float(self.config["USER"]["face_scaleFactor"])
        self.face_minNeighbors = int(self.config["USER"]["face_minNeighbors"])
        self.eye_scaleFactor = float(self.config["USER"]["eye_scaleFactor"])
        self.eye_minNeighbors = int(self.config["USER"]["eye_minNeighbors"])

    def detect(self) -> list:
        face_pos_list = []
        eye_list = []
        num_of_eye = []

        facecascade = cv2.CascadeClassifier(self.face_model)
        eyecascade = cv2.CascadeClassifier(self.eye_model)

        counter = 0
        while True:
            face_pos_list = facecascade.detectMultiScale(self.input, scaleFactor=self.face_scaleFactor, minNeighbors=self.face_minNeighbors - counter)
            if len(face_pos_list) >= 1 or self.face_minNeighbors - counter <= 0:
                break
            else:
                counter += 1
                continue

        if len(face_pos_list):
            for pos in face_pos_list:
                counter = 0
                face_img = self.input[pos[1] : pos[1] + pos[3], pos[0] : pos[0] + pos[2]]
                while True:   
                    eye_list = eyecascade.detectMultiScale(face_img, scaleFactor=self.eye_scaleFactor, minNeighbors=self.eye_minNeighbors + counter)
                    if len(eye_list) > 2:
                        counter += 1
                        continue
                    else:                 
                        num_of_eye.append(len(eye_list))
                        break
            return num_of_eye
        
        else:
            return ["No face detected."]


class fileManager():
    def __init__(self, config_path) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    @property
    def folder(self) -> str:
        return self.__folder
    @folder.setter
    def folder(self, path: str):
        self.__folder = path

    @property
    def fulleye_folder(self) -> str:
        return self.__fulleye_folder
    @fulleye_folder.setter
    def fulleye_folder(self, path: str):
        self.__fulleye_folder = path
    def fulleye_under(self, path_from_folder: str):
        self.__fulleye_folder = f"{self.folder}\\{path_from_folder}"
    def make_fulleye(self):
        os.makedirs(self.fulleye_folder, exist_ok=True)

    @property
    def someeye_folder(self) -> str:
        return self.__someeye_folder
    @someeye_folder.setter
    def someeye_folder(self, path: str):
        self.__someeye_folder = path
    def someeye_under(self, path_from_folder: str):
        self.__someeye_folder = f"{self.folder}\\{path_from_folder}"
    def make_someeye(self):
        os.makedirs(self.someeye_folder, exist_ok=True)

    @property
    def noeye_folder(self) -> str:
        return self.__noeye_folder
    @noeye_folder.setter
    def noeye_folder(self, path: str):
        self.__noeye_folder = path
    def noeye_under(self, path_from_folder: str):
        self.__noeye_folder = f"{self.folder}\\{path_from_folder}"
    def make_noeye(self):
        os.makedirs(self.noeye_folder, exist_ok=True)

    @property
    def noface_folder(self) -> str:
        return self.__noface_folder
    @noface_folder.setter
    def noface_folder(self, path: str):
        self.__noface_folder = path
    def noface_under(self, path_from_folder: str):
        self.__noface_folder = f"{self.folder}\\{path_from_folder}"
    def make_noface(self):
        os.makedirs(self.noface_folder, exist_ok=True)

    @property
    def active_extension(self) -> list:
        return self.__active_extension
    @active_extension.setter
    def active_extension(self, extension_list: list):
        self.__active_extension = extension_list.copy()
    def clear_active_extension(self):
        self.__active_extension.clear()
    def add_active_extension(self, extension: str):
        self.__active_extension.append(extension)

    @property
    def passive_extension(self) -> list:
        return self.__passive_extension
    @passive_extension.setter
    def passive_extension(self, extension_list: list):
        self.__passive_extension = extension_list.copy()
    def clear_passive_extension(self):
        self.__passive_extension.clear()
    def add_passive_extension(self, extension: str):
        self.__passive_extension.append(extension)

    def apply_config(self):
        self.fulleye_under(self.config["USER"]["fulleye_folder_relative_position_from_folder"])
        self.someeye_under(self.config["USER"]["someeye_folder_relative_position_from_folder"])
        self.noeye_under(self.config["USER"]["noeye_folder_relative_position_from_folder"])
        self.noface_under(self.config["USER"]["noface_folder_relative_position_from_folder"])

    def make_all_folder(self):
        self.make_fulleye()
        self.make_someeye()
        self.make_noeye()
        self.make_noface()


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    App = Detector(".\\setting\\cfg_detector.ini")

    photolist = glob.glob(".\\test_image\\*")

    for photo in photolist:
        App.input = photo
        result = App.detect()
        print(result)