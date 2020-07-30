# coding=UTF-8
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException


def wait(browser, hour, minute, second):
    localtime = time.localtime()  # 4, 5, 6번째 매개변수로 실행할 시각 가져와서 그때까지 기다림
    while not (localtime.tm_hour == hour and localtime.tm_min == minute and localtime.tm_sec == second):
        time.sleep(0.01)
        localtime = time.localtime()

    t = time.time()

    while True:
        browser.refresh()  # 시간이 되면 새로고침
        print("It took %f sec to refresh. This is the most time consuming part of this program." % (time.time() - t))
        time.sleep(0.25)  # 알림창 뜨는데 시간이 걸리드라,,

        try:
            browser.switch_to.alert.accept()  # 혹시 시작되지 않았을 때를 대비하여 알림창 닫기
        except NoAlertPresentException:  # 설문이 시작되어서 알림창이 뜨지 않았기 때문에 에러를 던졌을 때
            print("Survey Start Confirmed. Good to go.")  # 자동 설문 시작
            break
        else:
            print("Survey didn't started. Refreshing..")  # 다시 새로고침

    return t


def init(browser, selection):
    # 창바꿈 처리
    frames = browser.find_elements_by_tag_name('frame')
    browser.switch_to.frame(frames[0])  # 프레임으로 전환

    selections = browser.find_elements_by_xpath("//div[@class='lCodeClass styledRadio']")

    # 설문 항목 선택
    select = selections[selection - 1]  # 세번째 매개변수(선택할 항목의 순번(숫자))로 선택할 항목 가져옴
    browser.execute_script("arguments[0].scrollIntoView();", select)  # 선택할 항목으로 스크롤 (안하면 오류남;;)
    select.click()

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 맨 밑으로 스크롤 (실패시 최대한 빨리 대처하기 위함)

    # 설문 완료 버튼 클릭
    button = browser.find_element_by_id("applyBtn")
    button.click()


# Program starts here
# 매개변수 체크 / 바로 실행 여부 확인
if len(sys.argv) == 4:
    init_immediately = True

    survey_num = sys.argv[1]
    private_key = sys.argv[2]
    selection = int(sys.argv[3])
elif len(sys.argv) == 7:
    init_immediately = False

    survey_num = sys.argv[1]
    private_key = sys.argv[2]
    selection = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    second = int(sys.argv[6])
else:
    exit("Usage: python AutoSurvey.py <Survey Number> <Private Key> <Your Selection(in number)> [Survey time (h m s)]")

# 시작 문구 출력
if not init_immediately:  # 바로 실행 여부에 따라 다르게 출력
    print("AutoSurvey will be initiated at %sh %sm %ss" % (hour, minute, second))
print("Survey Number: %s, Private Key: %s" % (survey_num, private_key))
print("Your Selection is %d" % selection)

# Firefox 실행 / 진진리서치 열기.
browser = webdriver.Firefox()
browser.get("http://u.jjrss.com/?m=%s&u=%s" % (survey_num, private_key))  # 첫번째 매개변수: 방번호, 두번째 매개변수: 개인 키
print("Executed FireFox")

if init_immediately:  # 바로 실행
    print("Initiating immediately..")
    start_time = time.time()
    init(browser, selection)

else:  # 시간이 될 때까지 기다리다 실행
    # 알림창 처리
    time.sleep(0.25)  # 알림창 뜨는거 기다림
    try:
        browser.switch_to.alert.accept()
    except NoAlertPresentException:  # 이미 시작해서 알림창이 안 뜨기 때문에 에러를 던질 때 wait()하지 않고 바로 시작
        print("Already started, Initiating immediately")
        start_time = time.time()
    else:  # 시작 전일 때
        start_time = wait(browser, hour, minute, second)

    print("Initiating..")
    init(browser, selection)

print("Done. (%f sec)" % (time.time() - start_time))
