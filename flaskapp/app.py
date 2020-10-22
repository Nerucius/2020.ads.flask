from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/')
def index():
  return 'Index'

@app.route('/products/')
def products_list():
  return 'Listing of all products we have.'

@app.route('/products/<product_id>/')
def product_detail(product_id):
  return 'Detail of product     #{}.'.format(product_id)

@app.route(
  '/products/<product_id>/edit/',
  methods=['GET', 'POST'])
def product_edit(product_id):
  return 'Form to edit product #.'.format(product_id)

@app.route( '/products/create/', methods=['GET', 'POST'])
def product():
  return 'Form to create a new product.'

@app.route('/products/<product_id>/delete/', methods=['DELETE'])
def product_delete(product_id):
    raise NotImplementedError('DELETE')

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
  """.format(request=request).strip()
  return request_detail

@app.before_request
def callme_before_every_request():
  # Demo only: the before_request hook.
  app.logger.debug(dump_request_detail(request))

@app.after_request
def callme_after_every_response(response):
  # Demo only: the after_request hook.
  app.logger.debug('# After Request #\n' + repr(response))
  return response