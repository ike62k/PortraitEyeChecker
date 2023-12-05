# PortraitEyeChecker
人物写真から目瞑り写真を除外するツール Tool to exclude photos of people with their eyes closed from portraits photos

## はじめに
本ソフトウェアは趣味の一環として作成されたものです。このソフトウェアはMITライセンスの元配布されます。このソフトウェアを使用したいかなる結果にも、著者は責任を負いません。

## 動作確認済環境
- Windows 10 or 11 (x64)
- [Python3.12](https://www.python.org/) (これより前のバージョンでは動作確認はしていません)
- [PySimpleGUI](https://www.pysimplegui.org/en/latest/)　`pip install PySimpleGUI`でインストールできます。
- [OpenCV(CV2)](https://opencv.org/)　`pip install opencv-python`でインストールできます

## 概要
Python及びPythonのライブラリOpenCVのカスケード分類器を使用して写真を分類するソフトウェアです。<br>
カスケード分類器のうち、顔の検出および瞳の検出を用いて、写真を四種類にフォルダ分類します。<br>
OpenCVの瞳カスケード分類器が、閉じている目を検出しないことを利用して、顔の数と瞳の数の比から目を開いているか閉じているか検知します。<br>
$(face), (eye)$は顔,目の検知された個数
1. 顔が検知され、瞳が全て検知されている $2(face)=(eye), 0<(face)$
2. 顔が検知され、瞳が一部検知されている $0<(eye)<2(face), 0<(face)$
3. 顔が検知され、瞳が検知されていない $(eye)=0, 0<(face)$
4. 顔が検知されていない $(face)=0$

子供などを被写体とする、枚数を多く撮る撮影では写真の編集等をする以前に、写真の選別を行わなければならないことがあります。しかし、一枚一枚写真の選別をすることは時間のかかる作業であると考えます。そこで、一般的にミスとされる目瞑り写真を除外することで、選別作業の効率化を図ることがこのツールの目的です。<br>
カスケード分類器が検知できるファイルはJPG,PNGなどの一般的なファイル形式のみとなっていますが、RAWファイルにおいても
1. JPGファイルと同名
2. 同じフォルダ内に存在する

という条件を満たすものに関しては、JPGファイルの検知結果に合わせて移動することが可能です。
そのためJPG+RAWなどで撮影したデータにも対応する様になっています。

## 起動方法
1. [Python](https://www.python.org/)をインストールします。
2. [PySimpleGUI](https://www.pysimplegui.org/en/latest/)をインストールします。 `pip install PySimpleGUI`
3. [OpenCV(CV2)](https://opencv.org/)をインストールします。 `pip install opencv-python`

2,3の行程はrequirement.txtを利用して `pip install -r requirements.txt`でも可能です。

4. [Release](https://github.com/ike62k/PortraityeChecker/releases)から、ソースコードをダウンロードし、適当な場所で展開します。
5. コマンドで`Python -m PortraitEyeChecker`を実行するか、AppStart.batを実行します。

## GUIの操作方法

## configについて
本ソフトウェアにはconfigファイルが存在します。configファイルはアプリを起動した際の初期値を変更する他、内部処理での数値を変更することができます。