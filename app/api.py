# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import math
import json
import base64

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

@bp.route('/device/<int:dev_id>', methods=['GET'])
def device(dev_id):
    db = get_db()
    page = request.args.get('page')
    try:
        page = int(page) - 1
    except Exception:
        page = 0

    rows = db.execute('SELECT COUNT(*) FROM messages WHERE device_id=?', (dev_id, )).fetchone()
    count = rows[0]
    pages = int(math.ceil(count / 10.0))

    if page >= pages or page < 0:
        page = 0

    entries = db.execute('SELECT id, datetime(created, \'localtime\') as created, type, body ' +
        'FROM messages WHERE device_id=? ' +
        'ORDER BY created DESC LIMIT ?, 10', (dev_id, page * 10)).fetchall()
    messages = []

    for entry in entries:
        data = None
        obj = json.loads(entry['body'])

        if 'data' in obj.keys():
            data = " ".join([x.encode('hex')
                for x in base64.b64decode(obj['data'])])

        messages.append({'id': entry['id'],
            'created': entry['created'],
            'type': entry['type'],
            'data': data})

    return json.dumps({
        'page': page + 1,
        'pages': pages,
        'messages': messages})