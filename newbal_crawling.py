import requests
from bs4 import BeautifulSoup 

def nb_url():
  url="https://www.nbkorea.com/launchingCalendar/list.action?listStatus=C"
  res = requests.get(url)
  res.raise_for_status() #사이트에 접근 에러 발생 시

  soup = BeautifulSoup(res.text, "lxml") #lxml 객체로 만듦

  shoes=soup.find_all("div",attrs={"class":"launching"})

  coming_list=[]
  for shoe in shoes:
    coming_list.append("https://www.nbkorea.com/"+shoe.a["href"]) 
  
  return coming_list

#[ [상품명,(색상),가격,발매날짜,상품이미지],[],..[]]
def nb_shoes(nb_urls):
  shoes_info=[]
  
  for nb_url in nb_urls:
    respond = requests.get(nb_url)
    respond.raise_for_status()

    nb_soup = BeautifulSoup(respond.text,"lxml")
    nb_shoes = nb_soup.find_all("div",attrs={"class":"launchingDetail_prd"} )

    for nb_shoe in nb_shoes:
      shoe_info=[]
      product = nb_shoe.find("p", attrs={"class":"launchingDetail_proName"})
      shoe_info.append(product.get_text())  #상품명
      price = nb_shoe.find("p", attrs={"class":"launchingDetail_price"})
      shoe_info.append(price.get_text())  #가격
      date = nb_soup.select_one('body > div > div.container.npb > div.launching.launchingDetail > div.launchingDetail_info > p:nth-child(1) > b > span') #날짜
      hour = nb_soup.select_one('body > div > div.container.npb > div.launching.launchingDetail > div.launchingDetail_info > p:nth-child(2) > b > span') #시간
      shoe_info.append(date.get_text()+"  "+hour.get_text()+" 출시 예정") #발매날짜 정보

      #이미지를 NB런칭 캘린더에서 가져옴
      img_url="https://www.nbkorea.com/launchingCalendar/list.action?listStatus=C"
      img_res = requests.get(img_url)
      img_res.raise_for_status() #사이트에 접근 에러 발생 시

      img_soup = BeautifulSoup(img_res.text, "lxml") #lxml 객체로 만듦

      img_shoes=img_soup.find("div",attrs={"class":"launching_img"})
      shoe_info.append(img_shoes.img["src"]) 

      shoes_info.append(shoe_info)

  return shoes_info


nbUrl_list=nb_url()
nb_shoes(nbUrl_list)
#print(nb_shoes(nbUrl_list))
