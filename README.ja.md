# recognize-pieces-color

## 
テトリス~~廃人~~ガチ勢向けのネクスト認識練習ツールです。 　


## デモ
スペースキーを押すと画面が以下のように切り替わります。色の種類は設定可能。  
![Demo GIF animation](https://github.com/k-rakko/recognize-pieces-color/blob/master/media/demo.gif)    

## 動作環境
- python 3.x
- wxpython

## インストール方法
#### Windows
[ココ](https://www.python.org/downloads/) からpython３のインストーラをダウンロードしてきて実行した後に、コマンドプロンプトを管理者権限で起動して以下を実行してください。

```
pip3 install wxpython
```

#### Mac, Linux
[ココ](https://www.python.org/downloads/) からpython3 のインストーラをダウンロードして実行するなりapt なりhomebrew なりyum なりで入れてください。Arch など一部のOS ではすでにpython3がデフォルトらしいのでこのステップはいらないです。  

python3が用意できたら、お好みのターミナルエミュレータで以下を実行してください。エラーが出たら適宜がんばってください。
```
pip3 install wxpython
```

## 起動方法
まず、[ここ](https://github.com/k-rakko/Stackers-toolbox/releases)をクリックしてファイルをダウンロードしてください。(git でclone してもおーけー)    

zip解凍後にlaunchersに移動して、windowsなら"recognize-piece-color.bat"を、それ以外のOSでは.shのほうをダブルクリックすれば起動するはずです。（多分。起動しなかったら[@rikurakko](https://twitter.com/rikurakko)に文句をいってください。）


## 使い方
スペースキーで開始、さらにスペースキーで次の問題を表示します。以上です。  
もしコンフィグをしたければスパナマークをクリックしてください。  以下の項目を設定できます。

- どの色を出現させるか  
- ゴミブロックの平均の高さをいくつにするか  
- ネクストをいくつにするか  
- 目隠しテトリス練習用のネクストのみアップデートされて地形が変わらないモード

## バグレポート
強制終了やうまく起動しないなどあったら、[@rikurakko](https://twitter.com/rikurakko) まで連絡するかissueに書いてくれると助かります。

