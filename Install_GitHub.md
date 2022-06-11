# GitHubの導入
一般的なアプリやサイトなどのソフトウェア開発は作業量が膨大なため基本複数人で開発を行います.<br>
複数人で開発をしていると発生するのがバージョン問題です.<br>
そこで普段は各個人のPCでローカルで開発を行い,節目節目でGitHubというサイトにアップロードすることで全体のバージョン管理をします.<br>
新たに作業を始める際はGitHubから各個人のPCに最新バージョンのフォルダをダウンロードして作業終わりにまたアップロードを繰り返します.<br>
工業分野ではPLCなどのソフトウェアがありますが,基本ひとつのバージョンしか無いため複数人でソフトウェアを開発するイメージが付きにくいかと思いますが,
プログラマー界隈ではGitHubを使わないと仕事が出来ないと言っても過言ではないくらい全員が使っているサイトなのでこの機会に是非触って欲しいです.<br>
(慣れてくれば｢工業分野も早くPLCから脱却(DX)して情報分野の様な便利な機能が増えないかなぁ...｣と感じるはずです.多分)<br><br>

ちなみにGitHubは僕も体験程度しか触ったことがなく,本格的に使うのは今回が初めてなのであまり詳しくありません.<br>
(基本一人作業なのでローカルで十分)<br>

https://gitforwindows.org/

1. 上記URLにてGitのダウンロード
![image](https://user-images.githubusercontent.com/20737362/173197630-e69d74dc-8233-44a1-a2b1-c384e892e5c8.png)

2. チェックボックスはすべてデフォルトのまま｢次へ｣を押してインストール完了後,コマンドプロンプトで｢git --version｣と入力し｢git version 2.36.1.windows.1｣と出てくればOK
![image](https://user-images.githubusercontent.com/20737362/173197715-bcc2d13d-1eae-4b2b-8ec5-6269bea1d71d.png)

3.コマンドプロンプトに｢git config --global user.name "任意のユーザー名"｣と入力してユーザー名を決める<br>
4.コマンドプロンプトに｢git config --global email.name "メールアドレス"｣と入力してメールアドレスを登録する<br>
5.コマンドプロンプトに｢git config --list｣と入力して登録が正しいか確認する
![image](https://user-images.githubusercontent.com/20737362/173197941-5b4831d5-540b-4d1b-bcda-f2f6728c21e7.png)

6.GitHubのアカウント作成<br>

https://github.com/

上記URLにてメールアドレスを入力して｢Sign up for GitHub｣を選択する
![image](https://user-images.githubusercontent.com/20737362/173198067-971cc0db-c67e-47be-97f7-94c569de52c7.png)

7. サイトに沿って進める(6年前から登録していたので画面での説明出来ません.すみません.ググればたくさん情報出てきます)<br>
8. コマンドプロンプトでローカル作業環境を作りたい場所に移動する(僕の場合は｢cd programing/mu-ran｣)<br>
9. コマンドプロンプトに｢git init｣と入力してリポジトリを作成する
![image](https://user-images.githubusercontent.com/20737362/173198517-7b8fa53f-3bdc-4df6-9444-e40b047a7ae8.png)

## その他コマンド作成中

