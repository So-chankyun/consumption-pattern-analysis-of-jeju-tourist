import numpy as np
import pandas as pd
from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json

# naver api
client_id = 'mncjy4lf5z'
client_pw = 's82zIti8a9u7g6CzlEajqgcgHdIhwTfvh8pPXdJN'

api_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='

# 주소 목록 파일
jeju_town_data = pd.read_csv('./input/domestic_consumption_data.csv', encoding='ANSI')['제주 중분류'].unique()

# 네이버 지도 API 이용해서 위경도 찾기
def find_position(addresses):
    geo_coordi = []
    data = addresses.tolist()
    for add in data:
        add_urlenc = parse.quote(add)
        url = api_url + add_urlenc
        request = Request(url)
        request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
        request.add_header('X-NCP-APIGW-API-KEY', client_pw)
        try:
            response = urlopen(request)
        except HTTPError as e:
            print('HTTP Error!')
            latitude = None
            longitude = None
        else:
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read().decode('utf-8')
                response_body = json.loads(response_body)
                if 'addresses' in response_body:
                    latitude = response_body['addresses'][0]['y']
                    longitude = response_body['addresses'][0]['x']
                    print('Success!')
                else:
                    print("'result' not exist!")
                    latitude = None
                    longitude = None
            else:
                print('Response error code %d' % rescode)
                latitude = None
                longitude = None

        geo_coordi.append([latitude, longitude])

    np_geo_coordi = np.array(geo_coordi)
    pd_geo_coordi = pd.DataFrame({"address":data,
                                  "latitude":np_geo_coordi[:,0],
                                  "longitude":np_geo_coordi[:,1]})
    return pd_geo_coordi

find_position(jeju_town_data).to_csv('jeju_town_pos', index = False)