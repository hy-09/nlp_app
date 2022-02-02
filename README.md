
## アプリの概要
青空文庫から取得した本に対して以下の処理を行います。
- 本の内容の感情分析
- 選択した2つの本を合成して文章を生成
![091c374f-e87d-4e16-afc3-79be6c99135d](https://user-images.githubusercontent.com/72845995/152087432-7d98441b-8ffc-422e-95d7-7ed1b7d5784a.gif)


感情分析
![image](https://user-images.githubusercontent.com/72845995/152087088-99d45f01-5b02-4c05-b3db-c493cf853032.png)

作品合成
![image](https://user-images.githubusercontent.com/72845995/152087156-311eedf3-e37c-49f9-9605-a7f32c257145.png)



## 使用技術
- Vue.js 2
- vue-charjs
- Bootstrap 5
- Django 3
- Janome（形態素解析）
- Gunicorn
- MySQL
- Docker（Docker Compose）

## こだわりポイント
本の内容と感情分析グラフを高速で表示させるため、事前に以下のファイルを作成してDjangoのディレクトリに保存しています。
- 本の内容のtxtファイル
- 感情の分析結果を格納したjsonファイル
