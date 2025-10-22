# crawling_KBS.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def get_logged_in_contents(user_id, user_pw):
    """네이버에 로그인한 후 보이는 콘텐츠를 수집한다."""
    contents = []

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 브라우저 창 없이 실행 (테스트용)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://www.naver.com')
        time.sleep(2)

        login_button = driver.find_element(By.CLASS_NAME, 'MyView-module__link_login___HpHMW')
        login_button.click()
        time.sleep(2)

        id_input = driver.find_element(By.ID, 'id')
        pw_input = driver.find_element(By.ID, 'pw')

        id_input.send_keys(user_id)
        pw_input.send_keys(user_pw)
        pw_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # 로그인 후 보이는 콘텐츠 예시: 사용자 이름 표시
        driver.get('https://www.naver.com')
        time.sleep(2)

        try:
            username = driver.find_element(By.CLASS_NAME, 'MyView-module__my_name___2mpii').text
            contents.append(f'로그인한 사용자 이름: {username}')
        except Exception:
            contents.append('사용자 이름을 찾을 수 없음')

        # 보너스: 네이버 메일 제목 추출
        driver.get('https://mail.naver.com')
        time.sleep(5)

        mail_titles = driver.find_elements(By.CLASS_NAME, 'mail_title')

        for mail in mail_titles:
            contents.append('메일 제목: ' + mail.text)

    finally:
        driver.quit()

    return contents


def main():
    """메인 함수"""
    # 사용자 입력 필요
    user_id = input('네이버 아이디를 입력하세요: ')
    user_pw = input('네이버 비밀번호를 입력하세요: ')

    result = get_logged_in_contents(user_id, user_pw)

    for item in result:
        print(item)


if __name__ == '__main__':
    main()
