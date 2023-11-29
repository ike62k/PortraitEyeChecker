import os
import configparser
import PySimpleGUI as sg
from .libs.detector import Detector
from .libs.filemanager import FileManager


class Work():
    def __init__(self, config_path) -> None:
        self.config = configparser.ConfigParser().read(config_path, encoding="UTF-8")
        self.detector = Detector(config_path)
        self.filemanager = FileManager(config_path)


class GUI():
    def __init__(self) -> None:

        self.frame_input = sg.Frame("入力 input", expand_x= True, layout=[
            [sg.Text("フォルダを選択してください"), sg.InputText(expand_x=True, key = "--inputfolder", enable_events=True), sg.FolderBrowse("参照", enable_events=True)],
            [sg.Text("")]
        ])
        
        layout = [
            []
        ]

        self.window = sg.Window("Portraite Eye Checker", layout, size=(800,600), resizable=True)

        

class Controller():
    def __init__(self) -> None:
        self.work = Work(".\\config\\config.ini")
        self.GUI = GUI()
        self.status = "home"

    def run(self):
        while True:
            self.event, self.values = self.GUI.window.read()

            if self.event == sg.WIN_CLOSED:
                break
        
        self.GUI.window.close()