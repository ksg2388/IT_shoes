#i/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import subprocess
import sys
import requests
import json
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es_host = "http://localhost:9200"

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/SingUp', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("SingUp.html")
    else:
        id = request.form.get('id')
        name = request.form.get('name')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        if not (id and name and password and passwordConfirm):
            return "입력되지 않은 정보가 있습니다"
        elif password != passwordConfirm:
            return "비밀번호가 일치하지 않습니다"
        else:
            doc = {
                    'id' : id,
                    'name' : name,
                    'password' : password
            }
            res = es.index(index='user', id=i, document=doc)
            print(doc)
            print(res)

            return "회원가입 성공"
        return redirect('/')


if __name__ == '__main__':

    es = Elasticsearch(es_host)

    app.run(host="127.0.0.1", port=5000, debug=True)
