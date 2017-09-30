from flask import Blueprint, jsonify, request, render_template

import fsh.models.models

bp = Blueprint('api', __name__)


@bp.route("/")
def index():
    return render_template('landing.html')


@bp.route("/add", methods=["GET"])
def add():
    return render_template('add.html')


@bp.route("/take", methods=["GET"])
def take():
    return render_template('take.html')
