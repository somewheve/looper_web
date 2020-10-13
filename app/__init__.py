import os
import re
from flask import Flask, render_template, send_file, request, jsonify
from ctpbee import get_ctpbee_path

app = Flask(__name__, static_folder="./static", template_folder="./templates")
import jinja2


def get_info(looper_path):
    data = {}
    for x in os.listdir(looper_path):
        if "trade" in x:
            continue
        else:
            r = x.replace(".html", "")
            result = re.match("(.*)(\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2}_\d{0,6})", r)
            # file.append([result.group(1), result.group(2).replace("_", ":"), os.path.join(looper_path, x), x])
            info = result.group(1).split("_")
            if len(info) == 4:
                data.setdefault(info[0], {}).setdefault(info[1], {}).setdefault(info[2], []).append(result.group(
                    2).replace("_", ":"))
    return data


@app.route("/routes")
def get_file_path():
    return render_template("looper.html")


@app.route("/list_strategy")
def list_strategy():
    looper_path = os.path.join(get_ctpbee_path(), "looper")
    info = get_info(looper_path)
    return jsonify({"data": list(info.keys())})


@app.route("/strategy/", methods=["POST"])
def get_period():
    strs = request.values.get("strs")
    looper_path = os.path.join(get_ctpbee_path(), "looper")
    info = get_info(looper_path)
    return jsonify({"data": list(info.get(strs).keys())})


@app.route("/strategy/get_code", methods=['POST'])
def get_code():
    strs = request.values.get("strs")
    periods = request.values.get("periods")
    looper_path = os.path.join(get_ctpbee_path(), "looper")
    info = get_info(looper_path)
    return jsonify({"data": list(info.get(strs).get(periods).keys())})


@app.route("/strategy/get_time", methods=["POST"])
def get_time():
    strs = request.values.get("strs")
    periods = request.values.get("periods")
    code = request.values.get("codes")
    looper_path = os.path.join(get_ctpbee_path(), "looper")
    info = get_info(looper_path)
    data = info.get(strs).get(periods).get(code)
    return jsonify({"data": data})


@app.route("/get_detail", methods=["POST"])
def get_file_detail():
    p = os.path.join(os.path.join(get_ctpbee_path(), "looper"), request.values.get("path"))
    return send_file(p)


@app.route("/delete")
def delete():
    p = request.values.get("path")
    looper_path = os.path.join(get_ctpbee_path(), "looper")
    p = os.path.join(looper_path, p)
    result = "删除成功"
    if p is not None and os.path.exists(p):
        os.remove(p)
        trade = p.replace(".html", "") + "-trade.html"
        print(trade)
        if os.path.exists(trade):
            os.remove(trade)
    elif p is None:
        result = "文件不存在"
    elif p is not None and not os.path.exists(p):
        result = "文件资源不存在"
    return jsonify(dict(result=result))


@app.route("/")
def index_me():
    return "  "


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
