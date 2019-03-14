# coding=utf-8
from werkzeug.utils import secure_filename
from flask import *
import algorithm2 as ag
import name as nm
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '加密Session所需的密钥'


@app.route('/')
def index():
    return render_template('index.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.route('/redirect_to_index')
def redirect_to_index():
    return redirect(url_for('index'))

@app.route('/error')
def show_error():
    return render_template('404.html')

@app.route('/show', methods=['post', 'get'])
def show():
    name = request.values.get('my_query')
    #print(name)
    result = ag.getRetrievalResults(name.strip())
    #print('*'*20)
    #print(result)
    #print('*' * 20)
    #length = 10
    #if len(result) < 10:
    length = len(result)
    #print(length)
    if length == 0:
        template = redirect(url_for('show_error'))
        resp = make_response(template)
        return resp
    template = render_template('show.html', result = json.dumps(result), length = length, init = 0)
    resp = make_response(template)
    return resp

@app.route('/getResult', methods=['post', 'get'])
def getResult():
    name = request.values.get('key')
    print(name)
    # resp = make_response(json.dumps({'a': 1, 'b':1}))
    result = ag.getRetrievalResults(name.strip())
    length = len(result)
    if length == 0:
        resp = make_response(json.dumps({'error': '未找打查询结果'},ensure_ascii=False))
        return resp
    return make_response(json.dumps(result,ensure_ascii=False))

@app.route('/extract', methods=['post'])
def extract():
    my_url = request.values.get('url')
    extract_result = nm.getName(my_url)
    #print(extract_result)
    return extract_result

if __name__ == '__main__':
    #app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1')
