# -*- coding: utf-8 -*-
'''
Created on 2017/03/17

@author: tzatter

loggingについてのチュートリアル
https://docs.python.jp/3/howto/logging.html

必要パッケージ
・メール通知機能、インストールはubuntuの場合「sudo apt-get install postfix」
・デスクトップ通知機能、notify-sendコマンドが端末で使える事
'''
import logging
import os
import smtplib
import subprocess
import sys
from logging import Handler
from logging.handlers import RotatingFileHandler, SMTPHandler
from os.path import basename, splitext


DIRNAME = "log"
MAX_LOG_BYTES = 10 ** 6
BACKUP_COUNT = 5
DATE_FORMAT = "%m/%d %H:%M:%S"


def _resolve_logname():
    try:
        return basename(splitext(sys.modules["__main__"].__file__)[0])
    except AttributeError:
        return "japaneselogger"


def _ensure_log_directory():
    if not os.path.exists(DIRNAME):
        os.makedirs(DIRNAME)


def _create_formatter():
    return logging.Formatter(
        "[%(asctime)s %(levelname)s %(filename)s %(lineno)s] %(message)s",
        datefmt=DATE_FORMAT,
    )


def _add_stream_handler(target_logger, formatter):
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    target_logger.addHandler(handler)


def _add_rotating_handler(target_logger, formatter, level, suffix):
    handler = RotatingFileHandler(
        "{}.{}.log".format(os.path.join(DIRNAME, LOGNAME), suffix),
        maxBytes=MAX_LOG_BYTES,
        backupCount=BACKUP_COUNT,
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    target_logger.addHandler(handler)


def _setup_logger():
    logger_instance = logging.getLogger(LOGNAME)
    logger_instance.setLevel(logging.DEBUG)

    if logger_instance.handlers:
        return logger_instance

    _add_stream_handler(logger_instance, FORMATTER)
    _add_rotating_handler(logger_instance, FORMATTER, logging.DEBUG, "debug")
    _add_rotating_handler(logger_instance, FORMATTER, logging.ERROR, "error")
    return logger_instance


LOGNAME = _resolve_logname()
FORMATTER = _create_formatter()
_ensure_log_directory()
logger = _setup_logger()

#関数を上書き
debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error
exception = logger.exception

#メール通知機能
def enableEMailNotification(
    #メール設定
    EMAIL_TO_ADDRESS = 'example@example.com',
    SMTP_HOST = 'localhost',
    SMTP_PORT = 25,
                            ):
    try:
        #SMTPサーバーが利用可能かの確認
        server = smtplib.SMTP()
        server.connect(SMTP_HOST, SMTP_PORT)
        server.close()
        
        sh = SMTPHandler(mailhost=(SMTP_HOST, SMTP_PORT),
                         fromaddr=LOGNAME,
                         toaddrs=EMAIL_TO_ADDRESS,
                         subject=LOGNAME)
        sh.setLevel(logging.ERROR)
        sh.setFormatter(FORMATTER)
        logger.addHandler(sh)
        logger.info("メール通知機能を使います、エラー以上は通知されます")
    except ConnectionRefusedError:
        logger.warning("SMTPサーバーが応答していないためメール通知機能が使えません")

#デスクトップ通知機能
def enableDesktopNotification(commandType="notifiy-send"):
    try:
        if(commandType=="notifiy-send"):
            _ = subprocess.check_output(["notify-send","--version"])
            logger.info("デスクトップ通知機能のnotify-sendを使います、エラー以上は通知されます")
        elif(commandType=="zenity"):
            _ = subprocess.check_output(["zenity","--help"])
            logger.info("デスクトップ通知機能のzenityを使います、エラー以上は通知されます")
        else:
            return
        class NotifyHandler(Handler):
            def emit(self,logRecord):
                if(commandType=="notifiy-send"):
                    command = ["notify-send", LOGNAME, logRecord.getMessage()]
                    subprocess.call(command)
                elif(commandType=="zenity"):
                    command = ["zenity", "--error", "--text={} : {}".format(LOGNAME,logRecord.getMessage())]
                    subprocess.call(command)
        nh = NotifyHandler()
        nh.setLevel(logging.ERROR)
        nh.setFormatter(FORMATTER)
        logger.addHandler(nh)
    except FileNotFoundError:
        logger.warning("デスクトップ通知機能が使えません")
