import os
import uuid

from flask import Flask
from flask import request

import crossplane
app = Flask(__name__, static_folder='web_ui', static_url_path='/web_ui')
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json;charset=utf-8'  # 设置JSON响应的MIME类型为UTF-8编码


@app.route('/parse_single_conf', methods=['POST'])
def parse_single_conf():
    body_data = request.data
    body_str = body_data.decode('utf-8')

    nginx_conf_temp_path = write_temp_file(body_str)

    try:
        payload = crossplane.parse(nginx_conf_temp_path, single=True, comments=True)
        result = {'code': 0, 'data': payload, 'msg': '解析成功'}
    except Exception as e:
        result = {'code': -1, 'data': None, 'msg': str(e)}
    finally:
        os.remove(path=nginx_conf_temp_path)

    return result


@app.route('/build_conf', methods=['POST'])
def build_conf():
    body_data = request.json

    try:
        conf = crossplane.build(body_data)
        result = {'code': 0, 'data': conf, 'msg': '构建成功'}
    except Exception as e:
        result = {'code': -1, 'data': None, 'msg': str(e)}

    return result


@app.route('/format_conf', methods=['POST'])
def format_conf():
    body_data = request.data
    body_str = body_data.decode('utf-8')

    nginx_conf_temp_path = write_temp_file(body_str)

    try:
        conf = crossplane.format(nginx_conf_temp_path)
        result = {'code': 0, 'data': conf, 'msg': '格式化成功'}
    except Exception as e:
        result = {'code': -1, 'data': None, 'msg': str(e)}
    finally:
        os.remove(path=nginx_conf_temp_path)
    return result


def write_temp_file(write_str):
    nginx_conf_temp_path = 'nginx_conf_temp_%s.conf' % uuid.uuid4().hex
    temp_file = open(nginx_conf_temp_path, mode='w', encoding='utf-8')
    temp_file.write(write_str)
    temp_file.close()
    return nginx_conf_temp_path


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
