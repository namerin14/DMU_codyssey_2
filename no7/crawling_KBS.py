#!/usr/bin/env python3
# coding: utf-8
"""
KBS 뉴스 + 추가 정보 크롤링 과제
- 수행과제: KBS 뉴스 헤드라인 크롤링
- 보너스과제: 기상청 RSS에서 날씨 정보 추가 수집
"""

import requests
from bs4 import BeautifulSoup


def get_kbs_headlines():
    """KBS 메인 페이지에서 헤드라인 뉴스 목록을 추출한다."""
    url = 'http://news.kbs.co.kr'
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        print('페이지 요청 실패:', response.status_code)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # KBS 뉴스 사이트의 주요 기사 제목 선택자 (사이트 구조에 따라 달라질 수 있음)
    headlines = []
    for tag in soup.select('div.news-tit a'):
        text = tag.get_text(strip=True)
        if text:
            headlines.append(text)

    return headlines


def get_weather():
    """기상청 RSS에서 서울(강남구) 날씨 정보 추출."""
    url = 'http://www.weather.go.kr/w/rss/dfs/hr1-forecast.do?zone=1168064000'
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        print('날씨 정보를 가져올 수 없습니다.')
        return None

    soup = BeautifulSoup(response.text, 'xml')
    category = soup.find('category').get_text()
    weather = soup.find('wfKor').get_text()
    temp = soup.find('temp').get_text()

    return {
        '지역': category,
        '날씨': weather,
        '기온': temp + '℃'
    }


def main():
    # 수행과제: KBS 헤드라인 뉴스 출력
    headlines = get_kbs_headlines()
    if not headlines:
        print('헤드라인 뉴스를 가져올 수 없습니다.')
    else:
        print('KBS 주요 헤드라인 뉴스:')
        for idx, title in enumerate(headlines, start=1):
            print('{}: {}'.format(idx, title))

    print()  # 줄바꿈

    # 보너스과제: 날씨 정보 출력
    weather = get_weather()
    if weather:
        print('현재 날씨 정보:')
        for key, value in weather.items():
            print('{}: {}'.format(key, value))


if __name__ == '__main__':
    main()
