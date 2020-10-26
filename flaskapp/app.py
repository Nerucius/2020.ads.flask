import json

from flask import request, url_for, abort, jsonify, redirect, render_template
from bson.objectid import ObjectId

from flaskapp.config import app, mongo
from flaskapp.forms import ProductForm


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products/")
def products_list():
    return "Listing of all products we have."


@app.route("/products/<product_id>/")
def product_detail(product_id):
    """Provide HTML page with a given product."""
    # Query: get Product object by ID.
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    print(product)
    if product is None:
        # Abort with Not Found.
        abort(404)
    return render_template("product/detail.html", product=product)


@app.route("/products/<product_id>/edit/", methods=["GET", "POST"])
def product_edit(product_id):
    return "Form to edit product #.".format(product_id)


@app.route("/products/create/", methods=["GET", "POST"])
def product_create():
    """Provide HTML form to create a new product."""
    form = ProductForm(request.form)
    if request.method == "POST" and form.validate():
        mongo.db.products.insert_one(form.data)
        # Success. Send user back to full product list.
        return redirect(url_for("products_list"))
    # Either first load or validation error at this point.
    return render_template("product/edit.html", form=form)


@app.route("/products/<product_id>/delete/", methods=["DELETE"])
def product_delete(product_id):
    raise NotImplementedError("DELETE")


# ================================
# DEBUG
# ================================


def dump_request_detail(request):
    request_detail = """
## Request INFO ##
request.endpoint: {request.endpoint}
request.method: {request.method}
request.view_args: {request.view_args}
request.args: {request.args}
request.form: {request.form}
request.user_agent: {request.user_agent}
request.files: {request.files}

## request.headers ##
{request.headers}
  """.format(
        request=request
    ).strip()
    return request_detail


@app.before_request
def callme_before_every_request():
    # Demo only: the before_request hook.
    app.logger.debug(dump_request_detail(request))


@app.after_request
def callme_after_every_response(response):
    # Demo only: the after_request hook.
    app.logger.debug("# After Request #\n" + repr(response))
    return response
