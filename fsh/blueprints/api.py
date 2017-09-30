import uuid
import os
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, send_from_directory
from flask import current_app as app

import fsh.models.models as models

bp = Blueprint('api', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@bp.route("/")
def index():
    return render_template('landing.html')


@bp.route("/add", methods=["GET"])
def add():
    products = models.Product.query.all()
    return render_template('add.html', products=products)


@bp.route("/add", methods=["POST"])
def add_post():
    name = request.form['product']
    weight = request.form['weight']
    if weight.endswith("g"):
        weight = weight[:-1]
    weight = int(weight)
    description = request.form['description']
    entry = models.Product(name=name, weight=weight, description=description)

    if 'image' in request.files:
        file = request.files['image']
        if file.filename != "" and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + "." + file.filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            entry.image = filename

    models.db.session.add(entry)
    models.db.session.commit()
    return redirect(url_for('api.index'))
    # e = models.ProductEntry()


@bp.route("/take", methods=["GET"])
def take():
    entries = models.Product.query.filter_by(taken=False)
    return render_template('take.html', entries=entries)


@bp.route("/take/<id>", methods=["POST"])
def take_post(id):
    entry = models.Product.query.get(id)

    if request.form['weight'] == '':
        weight_taken = None
    else:
        weight_taken = int(request.form['weight'])

    old_weight = entry.weight
    if weight_taken is None or weight_taken >= old_weight - 10:
        entry.taken = True
    else:
        entry.weight = old_weight - weight_taken

    models.db.session.add(entry)
    models.db.session.commit()
    return redirect(url_for('api.take'))


@bp.route("/image/<path:filename>")
def image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
