# エディタの導入(Visual Studio Code)

エディタはプログラムやテキストを記述するアプリです.
エディタはWindows標準でメモ帳などが入っていますが,多くの文字を記述するプログラミングではより楽に文字が記述できるように
様々な機能が付与されたフリーソフトのエディタを用いるのが一般的です.<br><br>
プログラミングをする際,一番多く用いるのがエディタである為,エディタは各個人の使いやすいものをオススメします.<br>
(各個人で信仰しているエディタが違うためプログラミング界隈では頻繁にエディタ戦争という名の宗教戦争が起こります)<br><br>
僕もEmacs→Atomと使ってきましたが2022/12/末を持ってAtomの開発が停止されるため,今回からはVisual Studio Codeを使用します.<br>

https://code.visualstudio.com/

1. 上記URLにてV1.68をダウンロード(2022/6/11時点最新)
※先にpythonをインストールしてください
![image](https://user-images.githubusercontent.com/20737362/173195143-06e86fd4-0dfd-47e6-88dd-aebffa9a8f2b.png)

2. 画面に沿って｢次へ｣を押していく.追加タスクの箇所では｢PATHへの追加｣にチェックを入れておく
![image](https://user-images.githubusercontent.com/20737362/173195489-42dfb29a-dd2c-4361-8c3d-6c7dcc206146.png)

3. ｢完了｣まで行ってVisual Studio Codeが立ち上がったら,｢Ctrl + N｣を押して新規プログラムを書く
![image](https://user-images.githubusercontent.com/20737362/173195700-4d4d0334-1330-42ba-8d90-19231234e37a.png)

4.プログラムを書いたら｢Ctrl + S｣でファイル名をつけて保存(pythonを書く時はファイル名の拡張子は｢.py｣にしておくこと)
![image](https://user-images.githubusercontent.com/20737362/173196052-8cf2e22a-8dcf-4e9f-b6ff-1f44d065484a.png)

5.コマンドプロンプトを開いて｢cd フォルダ名/フォルダ名/.../フォルダ名｣でpythonを保存したフォルダまで移動<br><br>

例:<br>
今回は｢C:\Users\ashir\programing\mu-ran｣のフォルダ内に｢test.py｣というファイルを作成した<br>
コマンドプロンプトを立ち上げると｢C:\Users\ashir>｣と出ているので現在｢ashir｣のフォルダ内にいることが分かる<br>
｢test.py｣はさらに｢programing\mu-ran｣という2階層下のフォルダ内にあるので｢cd programing/mu-ran｣で移動する<br>
![image](https://user-images.githubusercontent.com/20737362/173196215-7e665dd5-2f76-4d41-a09a-8e18708a69be.png)

![image](https://user-images.githubusercontent.com/20737362/173196125-040f8b0a-dac1-4e9d-abbe-9a4972204cd3.png)

6. コマンドプロンプトで｢dir｣を実行してフォルダ内に｢test.py｣があることを確認
![image](https://user-images.githubusercontent.com/20737362/173196472-bbeca9a4-98a2-41d0-9aad-741e0022e69c.png)

7. コマンドプロンプトで｢python test.py｣を実行して｢Hello World｣が実行されたら成功
![image](https://user-images.githubusercontent.com/20737362/173196564-30e8c58d-e184-4fdf-9b5b-7a7a966f1472.png)

コマンドプロンプトなどは普段あまり使わないと思いますが,プログラマーは基本マウスを使わずにコマンドプロンプト上にキーボードでコマンドを打ち込んでPCを操作しています.<br>
仕事でもエクセルなどはキーボードでショートカットキーを使う方がマウス操作より早いと実感していると思いますが,コマンド操作も慣れればマウスより早くなるのでこの機会に是非触って欲しいです.

