# -*- coding: utf-8 -*-

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def get_device(deveui):
    db = get_db()
    dev = db.execute('SELECT id FROM devices WHERE deveui=?', (deveui, )).fetchone()
    if dev is not None:
        return dev['id']
    raise ValueError("Device not found")

def add_device(deveui):
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO devices (deveui) VALUES (?)', (deveui, ))
    lastid = cur.lastrowid
    cur.close()
    db.commit()
    return lastid

def add_message(devid, devtype, message):
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO messages (device_id, type, body) VALUES (?, ?, ?)',
        (devid, devtype, message))
    lastid = cur.lastrowid
    cur.close()
    db.commit()
    return lastid

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')
