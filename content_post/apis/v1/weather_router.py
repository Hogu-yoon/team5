import json

from django.http import HttpRequest
from ninja import Router
import requests

# 주석

from content_post.services.get_address_temp_service import DivisionCode, TimeWeather

content = Router(tags=["test"])


# @content.post("", url_name="weather")
# def get_weather(request: HttpRequest) -> json:
#     return{'tmp': 19, 'address': '서울 어딘가'}

@content.get("plz/", url_name="plz")
def get_img(request: HttpRequest,temp: int) -> json:
    # print(temp)
    url = "http://15.164.50.222:8000/img/"
    params = {"temp": temp}
    res = requests.get(url, params)
    return res.json()


# 주석
@content.post("", url_name="weather")
def get_weather(request: HttpRequest) -> json:
    # 37.626656, 127.0222314 지훈님댁
    x = request.POST['x']
    y = request.POST['y']

    division_code = DivisionCode(x, y)
    # 좌표값을 토대로 행정구역표 가져오는 서비스
    response = requests.get(division_code.url, params=division_code.params, headers=division_code.headers)
    # 행정구역표를 가져와서 날씨API에서 필요한 격자 X 격자 Y로 바꿔주는 함수
    division = division_code.division_code(response)
    # print(division)
    # 받아온 x, y좌표를 뿌려준다.
    y, x, add_1, add_2, add_3 = division
    # address = add_1 + add_2 + add_3
    address = add_1 + add_2
    # print(x, y)
    # 좌표를 넣어서 날씨 API에 맞는 형식으로 바꿔주는 클래스
    k_weather = TimeWeather(x, y)
    response = requests.get(k_weather.url, params=k_weather.params)
    database = response.json().get('response').get('body').get('items').get('item')

    pre_tmp = list()
    for db in database:
        if db.get('fcstTime') == k_weather.now and db.get('category') == 'TMP':
            pre_tmp.append(db)
    return {'tmp': pre_tmp, 'address': address}

# 주석해제 날씨
