try:
    from .App import Controller
    from .libs import *
except ImportError:
    print(
        "アプリケーションファイルが見つかりませんでした。",
        "再インストールなどを検討してください。"
    )
    input("Enterを押して終了します。")
    exit()

try:
    from .libs import detector
except ImportError:
    print(
        "detectorファイルが見つかりませんでした。",
        "再インストールなどを検討してください。"
    )
    input("Enterを押して終了します。")
    exit()

try:
    from .libs import filemanager
except ImportError:
    print(
        "filemanagerファイルが見つかりませんでした。",
        "再インストールなどを検討してください。"
    )
    input("Enterを押して終了します。")
    exit()    

try:
    from .VERSION import Version
except ImportError:
    print(
        "バージョンファイルが見つかりませんでした。",
        "再インストールなどを検討してください。"
    )
    input("Enterを押して終了します。")
    exit()

try:
    import cv2
except ImportError:
    print(
        "OpenCVがインストールされていません。",
        "pip install opencv-pythonでインストールしてください。"
        )
    input("Enterを押して終了します。")
    exit()

try:
    import PySimpleGUI as sg
except ImportError:
    print(
        "PySimpleGUIがインストールされていません。",
        "pip install PySimpleGUIでインストールしてください。",
        "PySimpleGUIについては以下のURLを参照してください。",
        "https://www.pysimplegui.org/en/latest/"
        )
    input("Enterを押して終了します。")
    exit()