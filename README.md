# 概要
ログイン画面を想定してSQLインジェクションの起こるサイトを作成してみる．

# 例
name欄に **' or 2=2 --** などと入力するとログインできてしまう．

# 起動方法
```
$ python run.py
```

# 環境
- Python3.5
- Flask
- SQLite
