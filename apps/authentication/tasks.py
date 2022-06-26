# -*- coding: utf-8 -*-
#
#

# from celery import shared_task
from config.celery_app import app
from src.utils import write_login_log

@app.task
def write_login_log_async(*args, **kwargs):
    write_login_log(*args, **kwargs)
    # pass

