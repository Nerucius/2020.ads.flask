import json, bson
from bson.objectid import ObjectId

from flask import request, url_for, abort, jsonify, redirect, render_template
from flask_login import current_user
from flask_login import login_user, logout_user, login_required

from flaskapp.config import app, mongo, login_manager
from flaskapp.forms import ProductForm, LoginForm
from flaskapp.models import User


@app.route("/")
def index():
    return redirect(url_for("products_list"))


@app.route("/products/")
def products_list():
    """Provide HTML listing of all Products."""
    # Query: Get all Products objects, sorted by date.
    products = mongo.db.products.find()[:]
    return render_template("product/index.html", products=products)


@app.route("/products/<product_id>/")
def product_detail(product_id):
    """Provide HTML page with a given product."""
    # Query: get Product object by ID.
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if product is None:
        # Abort with Not Found.
        abort(404)
    return render_template("product/detail.html", product=product)


@app.route("/products/<product_id>/edit/", methods=["GET", "POST"])
def product_edit(product_id):
    # Find product or panic
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if product is None:
        abort(404)

    # Form handling
    form = ProductForm(request.form)
    if request.method == "POST" and form.validate():
        mongo.db.products.update_one({"_id": ObjectId(product_id)}, {"$set": form.data})
        return redirect(url_for("products_list"))

    return render_template(
        "product/edit.html", title="Edit a Product", form=form, product=product
    )


@app.route("/products/create/", methods=["GET", "POST"])
def product_create():
    """Provide HTML form to create a new product."""
    form = ProductForm(request.form)
    if request.method == "POST" and form.validate():
        mongo.db.products.insert_one(form.data)
        # Success. Send user back to full product list.
        return redirect(url_for("products_list"))
    # Either first load or validation error at this point.
    return render_template(
        "product/edit.html", title="Create a new Product", form=form, product=dict()
    )


@app.route("/products/<product_id>/delete/", methods=["DELETE"])
def product_delete(product_id):
    """Delete record using HTTP DELETE, respond with JSON."""
    result = mongo.db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        # Abort with Not Found, but with simple JSON response.
        response = jsonify({"status": "Not Found"})
        response.status = 404
        return response
    return jsonify({"status": "OK"})


@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("products_list"))
    form = LoginForm(request.form)
    error = None
    if request.method == "POST" and form.validate():
        username = form.username.data.lower().strip()
        password = form.password.data.lower().strip()
        user = mongo.db.users.find_one({"username": username})
        if user and User.validate_login(user["password"], password):
            user_obj = User(user["username"])
            login_user(user_obj)
            return redirect(url_for("products_list"))
        else:
            error = "Incorrect username or password."
    return render_template("user/login.html", form=form, error=error)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("products_list"))


# ================================
# Error Handlers
# ================================


@app.errorhandler(404)
def error_not_found(error):
    return render_template("error/not_found.html"), 404


@app.errorhandler(bson.errors.InvalidId)
def error_invalid_id(error):
    return render_template("error/not_found.html"), 404


# ================================
# LOGIN
# ================================


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login hook to load a User instance from ID."""
    u = mongo.db.users.find_one({"username": user_id})
    if not u:
        return None
    return User(u["username"])


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
    # app.logger.debug(dump_request_detail(request))
    pass


@app.after_request
def callme_after_every_response(response):
    # Demo only: the after_request hook.
    # app.logger.debug("# After Request #\n" + repr(response))
    return response
