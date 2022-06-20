#i/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import subprocess
import sys
import requests
import json
from flask import Flask, render_template, request, redirect, flash
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "My_Key"
es_host = "http://localhost:9200"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}

@app.route('/')


def home():
#나이키 신발 정보 크롤링
    url="https://www.nike.com/kr/launch/?type=upcoming"
    res = requests.get(url,headers=headers)
    res.raise_for_status() #사이트에 접근 에러 발생 시 처리

    soup = BeautifulSoup(res.text, "lxml") #lxml 객체로 만듦
    shoes=soup.find_all("a",attrs={"class":"card-link d-sm-b comingsoon"}) #발매 예정인 상품만 찾음

    url_list=[] #발매 예정 상품의 url 리스트 
    for index, shoe in enumerate(shoes):  
        result = divmod(index,2)
        if result[1] == 0:
            url_list.append("https://www.nike.com"+shoe["href"]) #정보가 2개씩 나와서 1개만 나오도록 함
    
    nikeUrl_list=url_list
    
    shoes_info=[]
    for nike_url in nikeUrl_list:  #url 중 하나
        respond = requests.get(nike_url,headers=headers)
        respond.raise_for_status()

        nike_soup = BeautifulSoup(respond.text,"lxml")
        nike_shoes=nike_soup.find_all("div",attrs={"class":"product-info ncss-col-sm-12 full"})  #신발 정보 모음
        
        for nike_shoe in nike_shoes:
            shoe_info=[]
            shoe_info.append(nike_shoe.h1.get_text()) # 상품명
            shoe_info.append(nike_shoe.h5.get_text()) #색상
            shoe_info.append(nike_shoe.div.get_text()) #가격
            date = nike_shoe.find(attrs={"class":"test-available-date"}) #발매날짜
            shoe_info.append(date.get_text())
            image = nike_soup.find("img",attrs={"class":"image-component"}) #상품이미지
            shoe_info.append(image["src"])

            shoes_info.append(shoe_info)
    print(shoes_info)
#    print(nike_shoes(nikeUrl_list))

# 뉴발란스 신발 정보 크롤링
    url="https://www.nbkorea.com/launchingCalendar/list.action?listStatus=C"
    res = requests.get(url)
    res.raise_for_status() #사이트에 접근 에러 발생 시

    soup = BeautifulSoup(res.text, "lxml") #lxml 객체로 만듦

    shoes=soup.find_all("div",attrs={"class":"launching"})

    coming_list=[]
    for shoe in shoes:
        coming_list.append("https://www.nbkorea.com/"+shoe.a["href"]) 

    #[ [상품명,(색상),가격,발매날짜,상품이미지],[],..[]]
    shoes_info2=[]
    
    for nb_url in coming_list:
        respond = requests.get(nb_url)
        respond.raise_for_status()

        nb_soup = BeautifulSoup(respond.text,"lxml")
        nb_shoes = nb_soup.find_all("div",attrs={"class":"launchingDetail_prd"} )

        for nb_shoe in nb_shoes:
            shoe_info2=[]
            product = nb_shoe.find("p", attrs={"class":"launchingDetail_proName"})
            shoe_info2.append(product.get_text())  #상품명
            price = nb_shoe.find("p", attrs={"class":"launchingDetail_price"})
            shoe_info2.append(price.get_text())  #가격
            date = nb_soup.select_one('body > div > div.container.npb > div.launching.launchingDetail > div.launchingDetail_info > p:nth-child(1) > b > span') #날짜
            hour = nb_soup.select_one('body > div > div.container.npb > div.launching.launchingDetail > div.launchingDetail_info > p:nth-child(2) > b > span') #시간
            shoe_info2.append(date.get_text()+"  "+hour.get_text()+" 출시 예정") #발매날짜 정보

            #이미지를 NB런칭 캘린더에서 가져옴
            img_url="https://www.nbkorea.com/launchingCalendar/list.action?listStatus=C"
            img_res = requests.get(img_url)
            img_res.raise_for_status() #사이트에 접근 에러 발생 시

            img_soup = BeautifulSoup(img_res.text, "lxml") #lxml 객체로 만듦

            img_shoes=img_soup.find("div",attrs={"class":"launching_img"})
            shoe_info2.append(img_shoes.img["src"]) 

            shoes_info2.append(shoe_info2)

    #print(nb_shoes(nbUrl_list))
    return render_template("home.html", shoes_info=shoes_info, shoes_info2=shoes_info2)


@app.route('/SingUp', methods=['GET', 'POST'])
def SingUp():
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
            flash("회원가입이 완료되었습니다.")

            return "회원가입 성공"
        
        else:
            if id == "":
                id_error = "id를 입력해주세요."
            else:
                id_error = ""
            if name == "":
                name_error = "닉네임을 입력해주세요."
            else:
                name_error = ""
            if password == "":
                password_error = "password를 입력해주세요."
            else:
                password_error = ""
            if password != passwordConfirm:
                passwordConfirm_error = "password를 한번 더 입력해주세요."
            else:
                passwordConfirm_error = ""
            return render_template("SingUp.html", id_error = id_error, name_error = name_error, password_error = password_error, passwordConfirm_error = passwordConfirm_error)

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
    return redirect('/')

if __name__ == '__main__':

    app.run(host="127.0.0.1", port=5000, debug=True)


