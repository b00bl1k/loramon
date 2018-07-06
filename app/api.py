# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import math
import json

from app.db import get_db, get_device, add_device, add_message

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/lora-ack', methods=['POST'])
def ack():
    return ""

@bp.route('/lora-join', methods=['POST'])
def join():
    body = request.data
    msg = json.loads(body)

    if 'devEUI' in msg.keys():
        deveui = msg['devEUI']

        try:
            devid = get_device(deveui)
        except ValueError:
            devid = add_device(deveui)

        add_message(devid, 'join', body)

    return ""

@bp.route('/lora-uplink', methods=['POST'])
def uplink():
    body = request.data
    msg = json.loads(body)

    if 'devEUI' in msg.keys():
        deveui = msg['devEUI']

        try:
            devid = get_device(deveui)
        except ValueError:
            devid = add_device(deveui)

        add_message(devid, 'uplink', body)

    return ""

@bp.route('/lora-error', methods=['POST'])
def error():
    return ""

@bp.route('/devices', methods=['GET'])
def devices():
    db = get_db()
    deveui = request.args.get('deveui')
    page = request.args.get('page')
    try:
        page = int(page) - 1
    except Exception:
        page = 0

    if deveui:
        rows = db.execute('SELECT COUNT(*) FROM devices WHERE deveui LIKE (?)',
           ("%{}%".format(deveui), )).fetchone()
    else:
        rows = db.execute('SELECT COUNT(*) FROM devices').fetchone()

    count = rows[0]
    pages = int(math.ceil(count / 10.0))

    if page >= pages or page < 0:
        page = 0

    if deveui:
        rows = db.execute('SELECT id, deveui FROM devices WHERE deveui LIKE (?) LIMIT ?, 10',
           ("%{}%".format(deveui), page * 10))
    else:
        rows = db.execute('SELECT id, deveui FROM devices LIMIT ?, 10', (page * 10, ))

    if rows:
        devices = [{'id': dev['id'],
            'deveui': dev['deveui']} for dev in rows]
    else:
        devices = []

    return json.dumps({
        'page': page + 1,
        'pages': pages,
        'devices': devices})
