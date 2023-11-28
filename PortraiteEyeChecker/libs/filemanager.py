import cv2
import os
import glob
import shutil
import configparser

class FileManager():
    def __init__(self, config_path) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding="UTF-8")

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

    def get_active_files(self) -> list:
        result = []
        for extension in self.active_extension:
            result += glob.glob(f"{self.folder}\\*.{extension}")
        return result
    
    def get_passive_files(self) -> list:
        result = []
        for extension in self.passive_extension:
            result += glob.glob(f"{self.folder}\\*.{extension}")
        return result
    
    def move_to_fulleye(self, target: str):
        shutil.move(target, self.fulleye_folder)

    def move_to_someeye(self, target: str):
        shutil.move(target, self.someeye_folder)

    def move_to_noeye(self, target: str):
        shutil.move(target, self.noeye_folder)

    def move_to_noface(self, target: str):
        shutil.move(target, self.noface_folder)

    def selection_image(self, img_path: str, img_face_and_eye_list: list):
        if img_face_and_eye_list == [-1]:#中に-1が入るのは顔そのものが未検出のとき
            self.move_to_noface(img_path)
            return None
        num_of_face = len(img_face_and_eye_list)
        num_of_eye = sum(img_face_and_eye_list)
        if 2*num_of_face == num_of_eye:
            self.move_to_fulleye(img_path)
        elif num_of_eye != 0:
            self.move_to_someeye(img_path)
        elif num_of_eye == 0:
            self.move_to_noeye(img_path)