# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import json
import base64

from app.db import get_db, get_device

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    return render_template('index.html')
