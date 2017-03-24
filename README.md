## インストール
Python3のみ動作確認済み、PYPIに登録していますのでpipからインストール出来ます https://pypi.python.org/pypi/japaneselogger
```
pip3 install japaneselogger
```
## 使い方
Errorを含むDebug以上の全てのメッセージは"***.debug.log"ファイルに保存される

Errorだけは"***.error.log"ファイルに保存される

**ソースコードの例**
```python
# -*- coding: utf-8 -*-
from japaneselogger import logger,debug,info,warn,error,exception
if __name__ == '__main__':
    debug("デバッグ")
    error("エラー")
    try:
        num = 1/0
    except:
        exception("ゼロで割ってはいけません")
    pass
```

**出力内容の例**
```
03/23 22:16:44 DEBUG main.py 4 デバッグ
03/23 22:16:44 ERROR main.py 5 エラー
03/23 22:16:44 ERROR main.py 9 ゼロで割ってはいけません
Traceback (most recent call last):
  File "/home/takasi/workspace/logger_py/test/main.py", line 7, in <module>
    num = 1/0
ZeroDivisionError: division by zero
```