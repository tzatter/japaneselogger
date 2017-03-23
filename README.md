# インストール
Python3のみ動作確認済み、PYPIに登録していますのでpipからインストール出来ます https://pypi.python.org/pypi/japaneselogger
```
pip3 install japaneselogger
```
# 使い方
Debug, Info, Warning, Error, Criticalの全てのメッセージは"***.debug.log"ファイルに保存される

Error, Criticalは"***.error.log"ファイルに保存される

**ソースコードの例**
```python
# -*- coding: utf-8 -*-
from japaneselogger import logger

logger.debug("デバッグ")
logger.error("エラー")
try:
    num = 1/0
except:
    logger.exception("ゼロで割ってはいけません")
pass
```

**出力内容の例**
```
03/22 00:42:07 DEBUG main.py 4 デバッグ
03/22 00:42:07 ERROR main.py 5 エラー
03/22 00:42:07 ERROR main.py 9 ゼロで割ってはいけません
Traceback (most recent call last):
  File "/path/to/the/***.py", line 7, in <module>
    num = 1/0
ZeroDivisionError: division by zero
```