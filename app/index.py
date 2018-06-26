# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import json
import base64

from app.db import get_db, get_device

bp = Blueprint('index', __name__)

@bp.route('/<int:devid>')
def device(devid):
    db = get_db()
    entries = db.execute('SELECT id, created, type, body '
        'FROM messages '
        'WHERE device_id=? '
        'ORDER BY created DESC',
        (devid, )).fetchall()
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

    return render_template('device.html', messages=messages)

@bp.route('/')
def index():
    db = get_db()
    devices = db.execute('SELECT id, deveui FROM devices')

    return render_template('index.html', devices=devices)
