# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import json

from app.db import get_db, get_device, add_device, add_message

bp = Blueprint('lora', __name__, url_prefix='/lora')

@bp.route('/ack', methods=['POST'])
def ack():
    db = get_db()
    return ""

@bp.route('/join', methods=['POST'])
def join():
    print request.data
    db = get_db()
    return ""

@bp.route('/uplink', methods=['POST'])
def uplink():
    body = request.data
    msg = json.loads(body)
    deveui = msg['devEUI']

    try:
        devid = get_device(deveui)
    except ValueError:
        devid = add_device(deveui)

    add_message(devid, 'uplink', body)

    return ""

@bp.route('/error', methods=['POST'])
def error():
    db = get_db()
    return ""
