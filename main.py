from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox, Chrome, PhantomJS
from selenium import webdriver
from argparse import ArgumentParser
from urllib.parse import quote
import time
import copy
import sys
import os

TIMEOUT = 20
TIMESLP = 3


def login(driver, username, password, failed=0):
    if failed == 3:
        raise Exception('门户登录失败')

    iaaaUrl = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp'
    appName = quote('北京大学校内信息门户新版')
    redirectUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'
    driver.get('https://portal.pku.edu.cn/portal2017/')
    driver.get(
        f'{iaaaUrl}?appID=portal2017&appName={appName}&redirectUrl={redirectUrl}'
    )

    print('门户登陆中...')
    driver.find_element_by_id('user_name').send_keys(username)
    time.sleep(TIMESLP)
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(TIMESLP)
    driver.find_element_by_id('logon_button').click()

    try:
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.LINK_TEXT, '我知道了')))
    except:
        pass
    else:
        driver.find_element_by_link_text('我知道了').click()

    try:
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, 'all')))
    except:
        login(driver, username, password, failed + 1)
    else:
        print('门户登录成功！')


def go_to_application(driver):
    driver.find_element_by_id('all').click()
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'tag_s_epidemic')))
    driver.find_element_by_id('tag_s_epidemic').click()
    time.sleep(TIMESLP)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-input__inner')))
    print('已进入燕园云战疫！')


def click_no(driver):
    print("选择是否存在以下症状：否")
    temp = driver.find_element_by_xpath('//*[@id="pane-daily_info_tab"]/form/div[13]/div/label[2]').click()
    print("Done")
    time.sleep(TIMESLP)

def select_healthy(driver):
    print("选择疫情诊断：健康")
    driver.find_element_by_xpath('//*[@id="pane-daily_info_tab"]/form/div[14]/div/div').click()
    time.sleep(TIMESLP)
    driver.find_element_by_xpath(f'//li/span[text()="健康"]').click()
    print("Done")
    time.sleep(TIMESLP)

def submit(driver):
    print("保存信息")
    driver.find_element_by_xpath('//*[@id="pane-daily_info_tab"]/form/div[17]/div/button').click()
    print("Done")
    time.sleep(2*TIMESLP)


def fill(driver):
    click_no(driver)
    select_healthy(driver)
    submit(driver)
    print('填报完毕！')


def run(driver, username, password):
    login(driver, username, password)
    print('=================================')
    go_to_application(driver)
    fill(driver)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--username', '-u', type=str, help='用户名')
    parser.add_argument('--password', '-p', type=str, help='密码')
    args = parser.parse_args()
    args_public = copy.deepcopy(args)
    args_public.password = 'xxxxxxxx'
    print('Arguments: {}'.format(args_public))
    print('Driver Launching...')

    # driver = Firefox()
    # driver = Chrome()

    if sys.platform == 'darwin':  # macOS
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-darwin')
    elif sys.platform == 'linux':  # linux
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-linux-x86_64')
    else:  # windows
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-windows.exe')

    driver = PhantomJS(executable_path=phantomjs_path)

    run(driver, args.username, args.password)

    driver.close()
