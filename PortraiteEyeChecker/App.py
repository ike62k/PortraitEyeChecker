import os
import configparser
import PySimpleGUI as sg
from .libs.detector import Detector
from .libs.filemanager import FileManager


class Work():
    def __init__(self, config_path) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding="UTF-8")
        self.detector = Detector(config_path)
        self.filemanager = FileManager(config_path)


class GUI():
    def __init__(self, config) -> None:

        #入力セクジョン
        self.active_set = set()
        self.passive_set = set()
        self.parts_add = sg.Column([
            [sg.Column([[sg.Text("拡張子を入力",expand_x=True, justification="LEFT")]], justification="CENTER")],
            [sg.Input(size=(18,1), key="-extension_input-", expand_x=True, enable_events=True)],
            [sg.Button("←activeに追加\nadd to active", size=(16,2), key="-add_active-"), sg.Button("passiveに追加→\nadd to passive", size=(16,2), key="-add_passive-")],
            [sg.Button("←activeから削除\ndelete from active", size=(16,2), key="-delete_active-"), sg.Button("passiveから削除→\ndelete from passive", size=(16,2), key="-delete_passive-")]
        ])
        self.extension_column = sg.Column(justification="CENTER", layout=[
            [sg.Table(self.active_set, ["検知対象とする拡張子(active)"], num_rows=8, key="-table_active-", enable_events=True),
             self.parts_add,
             sg.Table(self.passive_set, ["同時移動する拡張子(passive)"], num_rows=8, key="-table_passive-", enable_events=True),]
        ])
        self.frame_input = sg.Frame("入力 input", expand_x=True, layout=[
            [sg.Text("フォルダを選択してください"), sg.InputText(expand_x=True, key="-inputfolder-", enable_events=True), sg.FolderBrowse("参照", enable_events=True, initial_folder=os.getcwd())],
            [self.extension_column]
        ])
        #/入力セクジョン

        #設定セクション
        self.frame_setting = sg.Frame("設定 setting", expand_x=True, element_justification="CENTER", layout=[
            [sg.Text("顔認証のscaleFactor"), sg.Slider((1.01, 2.0), resolution=0.01, orientation="horizontal", default_value=float(config["face_scaleFactor"]), key="-face_scaleFactor-", enable_events=True),
            sg.Text("顔認証のminNeighbors"), sg.Slider((1, 20), resolution=1, orientation="horizontal", default_value=int(config["face_minNeighbors"]), key="-face_minNeighbors-", enable_events=True)],
            [sg.Text("目認証のscaleFactor"), sg.Slider((1.01, 2.0), resolution=0.01, orientation="horizontal", default_value=float(config["eye_scaleFactor"]), key="-eye_scaleFactor-", enable_events=True),
            sg.Text("目認証のminNeighbors"), sg.Slider((1, 20), resolution=1, orientation="horizontal", default_value=int(config["eye_minNeighbors"]), key="-eye_minNeighbors-", enable_events=True)],
        ])
        #/設定セクション

        layout = [
            [self.frame_input],
            [self.frame_setting],
        ]

        self.window = sg.Window("Portraite Eye Checker", layout, size=(800,800), resizable=False)

        

class Controller():
    def __init__(self) -> None:
        self.work = Work(".\\config\\config.ini")
        self.GUI = GUI(self.work.config["DEFAULT"])
        self.status = "home"

    def run(self):
        while True:
            self.event, self.values = self.GUI.window.read()

            if self.event == "-add_active-" and self.values["-extension_input-"] != "":
                self.GUI.active_set.add(self.values["-extension_input-"])
                self.GUI.window["-table_active-"].update(self.GUI.active_set)
                self.GUI.window["-extension_input-"].update("")
            
            if self.event == "-add_passive-" and self.values["-extension_input-"] != "":
                self.GUI.passive_set.add(self.values["-extension_input-"])
                self.GUI.window["-table_passive-"].update(self.GUI.passive_set)
                self.GUI.window["-extension_input-"].update("")

            if self.event == "-delete_active-" and self.values["-extension_input-"] != "":
                if self.values["-extension_input-"] in self.GUI.active_set:
                    self.GUI.active_set.remove(self.values["-extension_input-"])
                    self.GUI.window["-table_active-"].update(self.GUI.active_set)
                    self.GUI.window["-extension_input-"].update("")

            if self.event == "-delete_passive-" and self.values["-extension_input-"] != "":
                if self.values["-extension_input-"] in self.GUI.passive_set:
                    self.GUI.passive_set.remove(self.values["-extension_input-"])
                    self.GUI.window["-table_passive-"].update(self.GUI.passive_set)
                    self.GUI.window["-extension_input-"].update("")

            if self.event == sg.WIN_CLOSED:
                break
        
        self.GUI.window.close()