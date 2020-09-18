import os
import re
from flask import Flask, render_template, send_file, request, jsonify
from ctpbee import get_ctpbee_path

app = Flask(__name__, static_folder="./static", template_folder="./templates")
import jinja2


@app.route("/routes")
def get_file_path():
    looper_path = os.path.join(get_ctpbee_path(), "looper")
    file = []
    for x in os.listdir(looper_path):
        if "trade" in x:
            continue
        else:
            r = x.replace(".html", "")
            result = re.match("(.*)(\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2}_\d{0,6})", r)
            file.append([result.group(1), result.group(2).replace("_", ":"), os.path.join(looper_path, x), x])
    return render_template("looper.html", data=list(reversed(file)))


@app.route("/get_detail", methods=["GET"])
def get_file_detail():
    p = request.values.get("path")
    return send_file(p)


@app.route("/delete")
def delete():
    p = request.values.get("path")
    looper_path = os.path.join(get_ctpbee_path(), "looper")
    p = os.path.join(looper_path, p)
    result = "删除成功"
    if p is not None and os.path.exists(p):
        os.remove(p)
    elif p is None:
        result = "文件不存在"
    elif p is not None and not os.path.exists(p):
        result = "文件资源不存在"
    return jsonify(dict(result=result))


@app.route("/<path>")
def index(path):
    looper_path = os.path.join(get_ctpbee_path(), "looper")
    p = os.path.join(looper_path, path)
    result = "删除成功"
    if p is not None and os.path.exists(p):
        return send_file(p)
    elif p is None:
        return "welcome to cy looper center"
    elif p is not None and not os.path.exists(p):
        return "welcome to cy looper center"
