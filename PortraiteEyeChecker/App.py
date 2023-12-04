import os
import configparser
import PySimpleGUI as sg
from .libs.detector import Detector
from .libs.filemanager import FileManager
from .VERSION import Version


class Work():
    def __init__(self, config_path) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding="UTF-8")
        self.detector = Detector(config_path)
        self.filemanager = FileManager(config_path)

class GUI():
    def __init__(self, config) -> None:
        self.version_info = Version()

        #入力セクジョン
        self.active_ext_list = []
        self.passive_ext_list = []
        self.parts_add = sg.Column([
            [sg.Column([[sg.Text("拡張子を入力",expand_x=True, justification="LEFT")]], justification="CENTER")],
            [sg.Input(size=(18,1), key="-extension_input-", expand_x=True, enable_events=True)],
            [sg.Button("←activeに追加\nadd to active", size=(16,2), key="-add_active-"), sg.Button("passiveに追加→\nadd to passive", size=(16,2), key="-add_passive-")],
            [sg.Button("←activeから削除\ndelete from active", size=(16,2), key="-delete_active-", mouseover_colors="tomato"), sg.Button("passiveから削除→\ndelete from passive", size=(16,2), key="-delete_passive-", mouseover_colors="tomato")]
        ])
        self.extension_column = sg.Column(justification="CENTER", layout=[
            [sg.Table(self.active_ext_list, ["検知対象とする拡張子(active)"], num_rows=8, key="-table_active-", enable_click_events=True),
             self.parts_add,
             sg.Table(self.passive_ext_list, ["同時移動する拡張子(passive)"], num_rows=8, key="-table_passive-", enable_click_events=True)]
        ])
        self.frame_input = sg.Frame("入力 input", expand_x=True, layout=[
            [sg.Text("フォルダを選択してください"), sg.InputText(expand_x=True, key="-inputfolder-", enable_events=True), sg.FolderBrowse("参照", enable_events=True, initial_folder=os.getcwd())],
            [self.extension_column]
        ])

        #設定セクション
        self.frame_setting = sg.Frame("設定 setting", expand_x=True, element_justification="CENTER", layout=[
            [sg.Text("顔認証のscaleFactor"), sg.Slider((1.01, 2.0), resolution=0.01, orientation="horizontal", default_value=float(config["face_scaleFactor"]), key="-face_scaleFactor-", enable_events=True) ,sg.Button("reset", key="-reset_face_scaleFactor-"),
            sg.Text("顔認証のminNeighbors"), sg.Slider((1, 20), resolution=1, orientation="horizontal", default_value=int(config["face_minNeighbors"]), key="-face_minNeighbors-", enable_events=True), sg.Button("reset", key="-reset_face_minNeighbors-")],
            [sg.Text("目認証のscaleFactor"), sg.Slider((1.01, 2.0), resolution=0.01, orientation="horizontal", default_value=float(config["eye_scaleFactor"]), key="-eye_scaleFactor-", enable_events=True), sg.Button("reset", key="-reset_eye_scaleFactor-"),
            sg.Text("目認証のminNeighbors"), sg.Slider((1, 20), resolution=1, orientation="horizontal", default_value=int(config["eye_minNeighbors"]), key="-eye_minNeighbors-", enable_events=True), sg.Button("reset", key="-reset_eye_minNeighbors-")],
        ])

        #コンソールセクション
        self.console = sg.Multiline(size=(100, 10), key="-console-", disabled=True, autoscroll=True, expand_x=True, expand_y=True)

        #バージョン情報セクション
        self.version_section = sg.Column([
            [sg.Text(f"Version: {self.version_info.version}.{self.version_info.subver}")]
        ])

        #プログレスバーセクション
        self.prog_max = 100
        self.prog_bar = sg.ProgressBar(self.prog_max ,size=(4,16), key="-prog_bar-", orientation="horisontal", expand_x=True)

        #アクションボタンセクション
        self.action_button_column = sg.Column(justification="RIGHT", layout=[
            [sg.Button("取り消し Cancel", size=(16,2), key="-cancel-", disabled=True, mouseover_colors="tomato"), sg.Button("実行 Run", size=(16,2), key="-run-", mouseover_colors="lightskyblue")]
        ])

        #レイアウト
        layout = [
            [self.frame_input],
            [self.frame_setting],
            [self.console],
            [self.version_section, self.prog_bar, self.action_button_column]
        ]

        #ウィンドウ定義
        self.window = sg.Window("Portraite Eye Checker", layout, size=(800,800), resizable=False)


class Controller():
    def __init__(self, __config_path) -> None:
        self.work = Work(__config_path)
        self.GUI = GUI(self.work.config["DEFAULT"])
        self.status = "home"

    def run_process(self):
        if not self.status == "running_start":
            return None
        #running_preprocess_start
        self.work.filemanager.folder = self.values["-inputfolder-"]
        self.work.filemanager.apply_config()
        self.work.filemanager.make_all_folder()
        self.active_list = self.work.filemanager.get_active_files()
        self.status = "running_preprocess_end"
        #runnning_process_start
        self.active_list = self.work.filemanager.get_active_files()
        self.GUI.prog_max = len(self.active_list)
        self.GUI.prog_bar.update(0, self.GUI.prog_max)
        for i, active_file in enumerate(self.active_list):
            if self.status == "running_preprocess_end":
                self.GUI.console.update(f"現在処理中のファイル: {active_file}\n")
                self.GUI.prog_bar.update(i+1, self.GUI.prog_max)
                self.work.detector.input = active_file
                self.work.filemanager.selection_image(self.work.filemanager.get_full_files(active_file), self.work.detector.detect())

            if self.status == "cancel":
                return None
        self.status = "running_process_end"
        return None

    def run(self):
        while True:
            self.event, self.values = self.GUI.window.read()

            if self.event != None and self.event[0] == "-table_active-": #self.eventは("-table_active-", "+CLICKED+", (0,0))といったような値で帰ってくる
                self.GUI.window["-extension_input-"].update(self.GUI.active_ext_list[self.event[2][0]])#(0,0)のうち0番目が選択された行の番号 valueには値が入らないので、self.GUI.active_ext_listから値を取得して入力欄に入れる

            if self.event != None and self.event[0] == "-table_passive-":
                self.GUI.window["-extension_input-"].update(self.GUI.passive_ext_list[self.event[2][0]])

            if self.event == "-add_active-" and self.values["-extension_input-"] != "" and self.values["-extension_input-"] not in self.GUI.active_ext_list:
                self.GUI.active_ext_list.append(self.values["-extension_input-"].lower())
                self.GUI.window["-table_active-"].update(self.GUI.active_ext_list)
                self.GUI.window["-extension_input-"].update("")
            
            if self.event == "-add_passive-" and self.values["-extension_input-"] != "" and self.values["-extension_input-"] not in self.GUI.passive_ext_list:
                self.GUI.passive_ext_list.append(self.values["-extension_input-"].lower())
                self.GUI.window["-table_passive-"].update(self.GUI.passive_ext_list)
                self.GUI.window["-extension_input-"].update("")

            if self.event == "-delete_active-" and self.values["-extension_input-"] != "":
                if self.values["-extension_input-"] in self.GUI.active_ext_list:
                    self.GUI.active_ext_list.remove(self.values["-extension_input-"].lower())
                    self.GUI.window["-table_active-"].update(self.GUI.active_ext_list)
                    self.GUI.window["-extension_input-"].update("")

            if self.event == "-delete_passive-" and self.values["-extension_input-"] != "":
                if self.values["-extension_input-"] in self.GUI.passive_ext_list:
                    self.GUI.passive_ext_list.remove(self.values["-extension_input-"].lower())
                    self.GUI.window["-table_passive-"].update(self.GUI.passive_ext_list)
                    self.GUI.window["-extension_input-"].update("")

            if self.event == "-reset_face_scaleFactor-":
                self.GUI.window["-face_scaleFactor-"].update(self.work.config["DEFAULT"]["face_scaleFactor"])

            if self.event == "-reset_face_minNeighbors-":
                self.GUI.window["-face_minNeighbors-"].update(self.work.config["DEFAULT"]["face_minNeighbors"])

            if self.event == "-reset_eye_scaleFactor-":
                self.GUI.window["-eye_scaleFactor-"].update(self.work.config["DEFAULT"]["eye_scaleFactor"])

            if self.event == "-reset_eye_minNeighbors-":
                self.GUI.window["-eye_minNeighbors-"].update(self.work.config["DEFAULT"]["eye_minNeighbors"])

            if self.event  == "-run-" and self.status == "home":
                self.GUI.window["-console-"].update("処理を開始します。\n")
                self.status = "running_start"
                self.GUI.window["-run-"].update(disabled=True)
                self.GUI.window["-cancel-"].update(disabled=False)
                if not os.path.isdir(self.values["-inputfolder-"]):
                    self.status = "err_inputfolder"
                    sg.PopupError("入力フォルダが存在しません")
                if self.GUI.active_ext_list != []:
                    self.work.filemanager.active_extension = self.GUI.active_ext_list
                else:
                    self.status = "err_self.active_list"
                    sg.PopupError("検知対象とする拡張子が入力されていません")
                self.work.filemanager.passive_extension = self.GUI.passive_ext_list
                self.work.detector.face_scaleFactor = self.values["-face_scaleFactor-"]
                self.work.detector.face_minNeighbors = self.values["-face_minNeighbors-"]
                self.work.detector.eye_scaleFactor = self.values["-eye_scaleFactor-"]
                self.work.detector.eye_minNeighbors = self.values["-eye_minNeighbors-"]
                self.GUI.window.start_thread(lambda: self.run_process(), end_key="-running_process_end-")

            if self.event == "-running_process_end-":
                if self.status == "running_process_end":
                    self.GUI.window["-console-"].update("処理が終了しました。\n")
                elif self.status == "cancel":
                    self.GUI.window["-console-"].update("処理が中断されました。\n")
                else:
                    self.GUI.window["-console-"].update("処理が終了しましたが、エラーが発生しました。\n")
                self.GUI.window["-run-"].update(disabled=False)
                self.GUI.window["-cancel-"].update(disabled=True)
                self.GUI.window["-prog_bar-"].update(0, self.GUI.prog_max)
                self.status = "home"

            if self.event == "-cancel-":
                self.status = "cancel"
                self.GUI.window["-run-"].update(disabled=False)
                self.GUI.window["-cancel-"].update(disabled=True)
                self.GUI.window["-prog_bar-"].update(0, self.GUI.prog_max)
                self.GUI.window["-console-"].update("Cancelボタンが押されました。\n")
                self.status = "home"

            if self.event == sg.WIN_CLOSED:
                self.status = "home"

                break
        
        self.GUI.window.close()