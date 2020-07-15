import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException

print("AutoSurvey will be initiated at %sh %sm %ss" % (sys.argv[4], sys.argv[5], sys.argv[6]))
print("Survey Number: %s, Private Key: %s" % (sys.argv[1], sys.argv[2]))

# Firefox 실행 / 진진리서치 열기.
browser = webdriver.Firefox()
browser.get("http://u.jjrss.com/?m=%s&u=%s" % (sys.argv[1], sys.argv[2]))  # 첫번째 매개변수: 방번호, 두번째 매개변수: 개인 키

# 알림창 처리
time.sleep(1)
browser.switch_to.alert.accept()

localtime = time.localtime()  # 4, 5, 6번째 매개변수로 실행할 시각 가져와서 그때까지 기다림
while not (localtime.tm_hour == int(sys.argv[4]) and localtime.tm_min == int(sys.argv[5])
           and localtime.tm_sec == int(sys.argv[6])):
    time.sleep(0.01)
    localtime = time.localtime()
    print(".")

print("Initiating..")

while True:
    try:
        browser.refresh()  # 시간이 되면 새로고침
        time.sleep(0.25)  # 알림창 뜨는데 시간이 걸리드라,,
        browser.switch_to.alert.accept()  # 혹시 시작되지 않았을 때를 대비하여 알림창 닫기
    except NoAlertPresentException:  # 설문이 시작되어서 알림창이 뜨지 않았기 때문에 에러를 던졌을 때
        print("Survey Start Confirmed. Good to go.")  # 자동 설문 시작
        break
    else:
        print("Survey didn't started. Refreshing..")  # 다시 새로고침

# 창바꿈 처리
frames = browser.find_elements_by_tag_name('frame')
browser.switch_to.frame(frames[0])  # 프레임으로 전환

selections = browser.find_elements_by_xpath("//input[@id='lCode_12001']/..")

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

# # 5초 후 브라우저 꺼짐 (테스트할때만)
# for i in range(0, 5):
#     time.sleep(1)
#     print('.')

browser.quit()
