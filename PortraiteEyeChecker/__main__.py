try:
    from .App import Controller
except ImportError:
    print(
        "アプリケーションファイルが見つかりませんでした。",
        "再インストールなどを検討してください。"
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

App = Controller(".\\config\\config.ini")
App.run()