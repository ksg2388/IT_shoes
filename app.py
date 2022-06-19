#i/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import subprocess
import sys
import requests
import json
from flask import Flask, render_template, request, redirect, flash
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.secret_key = "My_Key"
es_host = "http://localhost:9200"

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/SingUp', methods=['GET', 'POST'])
def register():
    es = Elasticsearch(es_host)

    if request.method == 'GET':
        return render_template("SingUp.html")
    else:
        id = request.form.get('id')
        name = request.form.get('name')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')
        print(name)
        print(password)
        
        if (id and name and password):
            doc = {
                    'id' : id,
                    'name' : name,
                    'password' : password
            }
            res = es.index(index='user', id = id, document=doc)
            print(doc)
            print(res)

            return "회원가입 성공"
        
        else:
            if id == "":
                flash("id를 입력해주세요.")
            elif name == "":
                flash("닉네임을 입력해주세요.")
            elif password == "":
                flash("password를 입력해주세요.")
            elif password != passwordConfirm:
                flash("password를 확인해주세요.")
            return render_template("SingUp.html")

        return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    es = Elasticsearch(es_host)

    if request.method == 'GET':
        return render_template("Login.html")
    else:
        id = request.form.get('id')
        password = request.form.get('password')
        print(id)
        print(password)
        return redirect('/')


if __name__ == '__main__':

    app.run(host="127.0.0.1", port=5000, debug=True)
