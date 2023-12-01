import cv2
import os
import glob
import shutil
import configparser

class Detector():
    def __init__(self,config_path: str) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding="UTF-8")
        self.apply_config()

    @property
    def input(self) -> str:
        return self.__input
    @input.setter
    def input(self, inputfile: str):
        self.__input = cv2.cvtColor(cv2.imread(inputfile), cv2.COLOR_BGR2GRAY)
        height = self.__input.shape[0]
        width = self.__input.shape[1]
        if height > self.resize_border or width > self.resize_border:
            ratio = self.resize_border/(max(height, width))
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
        self.__face_scaleFactor = float(scaleFactor)

    @property
    def face_minNeighbors(self) -> int:
        return self.__face_minNeighbors
    @face_minNeighbors.setter
    def face_minNeighbors(self,minNeighbors: int):
        self.__face_minNeighbors =int(minNeighbors)

    @property
    def eye_scaleFactor(self) -> float:
        return self.__eye_scaleFactor
    @eye_scaleFactor.setter
    def eye_scaleFactor(self,scaleFactor: float):
        self.__eye_scaleFactor = float(scaleFactor)

    @property
    def eye_minNeighbors(self) -> int:
        return self.__eye_minNeighbors
    @eye_minNeighbors.setter
    def eye_minNeighbors(self,minNeighbors: int):
        self.__eye_minNeighbors = int(minNeighbors)

    @property
    def resize_border(self) -> int:
        return self.__resize_border
    @resize_border.setter
    def resize_border(self, resolution: int):
        self.__resize_border = int(resolution)

    def apply_config(self):
        self.face_model = self.config["USER"]["face_model"]
        self.eye_model = self.config["USER"]["eye_model"]
        self.face_scaleFactor = float(self.config["USER"]["face_scaleFactor"])
        self.face_minNeighbors = int(self.config["USER"]["face_minNeighbors"])
        self.eye_scaleFactor = float(self.config["USER"]["eye_scaleFactor"])
        self.eye_minNeighbors = int(self.config["USER"]["eye_minNeighbors"])
        self.resize_border = int(self.config["USER"]["resize_border"])

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
            return [-1]