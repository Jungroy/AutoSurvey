import sys
import time

from selenium import webdriver
# Firefox 실행 / 진진리서치 열기.
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Firefox()
browser.get("http://u.jjrss.com/?m=%s&u=%s" % (sys.argv[1], sys.argv[2]))  # 첫번째 매개변수: 방번호, 두번째 매개변수: 개인 키

time.sleep(0.25)
browser.switch_to.alert.accept()  # 디버그: 알림창 처리

# 창바꿈 처리
frames = browser.find_elements_by_tag_name('frame')
browser.switch_to.frame(frames[0])  # 프레임으로 전환

selections = browser.find_elements_by_xpath("//input[@id='lCode_12001']/..")

# for select in selections:
#     print(select.get_attribute("valid.lectnm"))

# 설문 항목 선택
select = selections[int(sys.argv[3]) - 1]  # 세번째 매개변수(선택할 항목의 순번(숫자))로 선택할 항목 가져옴
browser.execute_script("arguments[0].scrollIntoView();", select)  # 선택할 항목으로 스크롤 (안하면 오류남;;)
select.click()

browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 맨 밑으로 스크롤 (실패시 최대한 빨리 대처하기 위함)

# 설문 완료 버튼 클릭 (완료 버튼 id가 불분명하기 때문에 (2개임) 여러 id를 검색해보고 존재하는 것을 클릭) (applyBtn, applyBtn_sub)
try:
    button = browser.find_element_by_id("applyBtn_sub")
except NoSuchElementException as e:
    print(str(e))
    print("Continuing...")

try:
    button = browser.find_element_by_id("applyBtn")
except NoSuchElementException as e:
    print(str(e))
    print("Continuing...")

try:
    button.click()
except NameError as e:
    print(str(e))
    print("빨리 직접 눌러어어ㅓ")
    exit()

# 5초 후 브라우저 꺼짐 (테스트 편의상)
for i in range(0, 5):
    time.sleep(1)
    print('.')

browser.quit()
