# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
import subprocess
import json

def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


def get_salt():
    """
    获取安全随机数
    """
    cmd = ['openssl', 'rand', '-base64', '125']

    p=subprocess.Popen(cmd,
                       stderr=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       shell=False)
    salt,err = p.communicate()
    print(salt.decode())
    print('err:%s'%err.decode())


def exec_cmd(*args):
    """
    执行shell命令
    """
    for index,cmd in enumerate(args):
        if index == 0:
            p=subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,
                               shell=False)
        else:
            p=subprocess.Popen(cmd,stdin=p.stdout,stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE,shell=False)
    ret, err = p.communicate()
    return ret, err

if __name__ == "__main__":
    get_salt()