import string
import time

import pymysql
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # use headless browser login

time_start = time.clock()

username = "username"  # 在此填入你的用户名
password = "password"  # 在此填入你的密码
# driver = webdriver.Firefox()

# 使用Firefox自带的无头浏览器登录
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(firefox_options=options)  # use headless firefox to login
conn = pymysql.connect(user='root', password='123456', host='127.0.0.1', port=3306, database='renrendai',
                       use_unicode=True, charset="utf8")
# driver.set_page_load_timeout(10000);
cursor = conn.cursor()

first = 1


def LoginRRD(username, password):
    try:
        print(u'准备登录网站...')
        # driver.get("https://www.we.com/pc/passport/index/login")
        driver.get("https://www.renrendai.com/login");
        global first
        if first == 1:
            first = 0
            driver.find_element_by_class_name("tab-password").click()
        # elem_user = driver.find_element_by_name("j_username")
        # elem_user = driver.find_element_by_name("username")
        elem_user = driver.find_element_by_id("login_username")

        elem_user.send_keys(username)
        time.sleep(2)  # 设置等待时间，不用修改
        elem_pwd = driver.find_element_by_name("j_password")
        elem_pwd.send_keys(password)
        time.sleep(5)  # 设置等待时间，以防止用户名下拉菜单挡住登录按钮
        driver.find_element_by_class_name("is-allow").click()
        # driver.find_element_by_xpath(r"""//*[@id="form-login"]/div/div[2]""").click()  # 点击登录
        # driver.find_element_by_xpath(r"""//*[@id="form-reg"]/div/div[0]""").click()  # 点击登录

        time.sleep(10)  # 设置等待几秒，以进入用户主界面，如不等待而直接进入爬虫会提示未登录
        print(u'登录成功！')
    except Exception as e:
        print("Error:", e)
        driver.save_screenshot('screen.png')
    finally:
        print(u'End Login!\n')


def parse_userinfo(loanid):
    # """用于提取借款人各项信息数据"""
    print(loanid)
    urll = "https://www.renrendai.com/loan-%s.html" % loanid
    try:
        driver.get(urll)
    except selenium.common.exceptions.TimeoutException as e:
        print(loanid, "连接超时")
        return 0
    html = BeautifulSoup(driver.page_source, 'html.parser')

    info = html.find_all('div', class_="loan-user-info")  # 这个地方的命名经常修改
    info2 = html.find_all('div', class_="loan-con-l loan-alone-style")
    info_state = html.find_all('div', class_="check-status")
    try:
        li = info2[0].findAll('li')
    except IndexError as e:
        print(loanid, "不存在")
        return 0
    userinfo = {}
    try:
        items = info[0].findAll('span', {"class": "pr20"})
    except IndexError as e:
        print("errir", e);
        LoginRRD(username, password)
        return 0;
    else:
        for item in items:
            var = item.get_text()
            # print(var)
            # print(item.parent.text)
            value = item.parent.text.replace(var, "")
            # print(value)
            userinfo[var] = value
        for l in li:
            var = l.findAll('i')[0].get_text()
            value = l.findAll('span')[0].get_text()
            userinfo[var] = value
        try:
            cursor.execute(
                "INSERT INTO tbl_bmessage(loan_id, nick_name, credit_rating, name, identify, age, degree, marriage, loan, loc, overdue, success, total, overdue_amount, pay_num, non_pay, serious_overdue, income, estate, hose_loan, car, car_loan, other, industy, scale, career, city, work_time, value_date, err, risk_level, repayment_mode, repayment_source, frd, sex)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (loanid, userinfo.get('信用评级', 'null'), userinfo.get('年龄', 'null'), userinfo.get('学历', 'null'),
                 userinfo.get('婚姻', 'null'), userinfo.get('申请借款', 'null'), userinfo.get('信用额度', 'null'),
                 userinfo.get('逾期金额', 'null'), userinfo.get('成功借款', 'null'), userinfo.get('借款总额', 'null'),
                 userinfo.get('逾期次数', 'null'), userinfo.get('还清笔数', 'null'), userinfo.get('代还本息', 'null'),
                 userinfo.get('严重逾期', 'null'), userinfo.get('收入', 'null'), userinfo.get('房产', 'null'),
                 userinfo.get('房贷', 'null'), userinfo.get('车产', 'null'), userinfo.get('车贷', 'null'),
                 userinfo.get('其他', 'null'), userinfo.get('公司行业', 'null'), userinfo.get('公司规模', 'null'),
                 userinfo.get('岗位职业', 'null'), userinfo.get('工作城市', 'null'), userinfo.get('工作时间', 'null'),
                 userinfo.get('起息日', 'null'), userinfo.get('提前还款率', 'null'), userinfo.get('风险等级', 'null'),
                 userinfo.get('还款方式', 'null'), userinfo.get('还款来源', 'null'), userinfo.get('首还款日期', 'null'),
                 userinfo.get('性别', 'null')))
            conn.commit()
        except pymysql.err.IntegrityError as e:
            print(loanid, "已存在")
            return 300;
        try:
            tbody = info_state[0].findAll('tbody')
            trs = tbody[0].findAll('tr')
        except IndexError as e:
            print(loanid, '没有审核状态')
        else:
            for tr in trs:
                check_titles = ['审核项目', '状态', '通过日期']
                tds = tr.findAll('td')
                j = 0
                for td in tds:
                    userinfo[check_titles[j % 3]] = td.get_text()
                    j = j + 1
                cursor.execute("INSERT INTO tbl_check_state(loan_id, project, state, pass_date) VALUES (%s,%s,%s,%s)", (
                    loanid, userinfo.get('审核项目', 'null'), userinfo.get('状态', 'null'), userinfo.get('通过日期', 'null')))
                conn.commit()
        try:
            driver.find_element_by_xpath(r"""//*[@class="lend-bottom"]/ul/li[3]""").click()  # 转到还款表现
        except Exception as e:
            driver.save_screenshot('locate_error.png')
        # driver.save_screenshot('transfer_success.png')
        time.sleep(1)
        payhtml = BeautifulSoup(driver.page_source, 'html.parser')
        paydiv = payhtml.find_all('div', class_='loan-list-table')
        try:
            pay_tbody = paydiv[1].findAll('tbody')
            pay_trs = pay_tbody[0].findAll('tr')
        except IndexError as e:
            print(loanid, '还款表现有问题')
            print(e)
            return 0
        else:
            titles = ['合约还款日期', '状态', '应还本息', '应付罚息', '实际还款日期']
            k = 0
            for tr in pay_trs:
                td = tr.findAll('td')
                for t in td:
                    span = t.findAll('span')
                    if len(span) == 0:
                        userinfo[titles[k % 5]] = t.get_text()
                    else:
                        str = ''
                        for s in span:
                            str = str + s.get_text()
                        userinfo[titles[k % 5]] = str
                    k = k + 1
                cursor.execute(
                    "INSERT INTO tbl_repayment(loan_id, repayTime, repayType, unRepaidAmount, repaidFee, actualRepayTime) VALUES (%s,%s,%s,%s,%s,%s)",
                    (loanid, userinfo.get('合约还款日期', 'null'), userinfo.get('状态', 'null'), userinfo.get('应还本息', 'null'),
                     userinfo.get('应付罚息', 'null'), userinfo.get('实际还款日期', 'null')))
                conn.commit()
                return 0
        # return data


if __name__ == '__main__':

    LoginRRD(username, password)  # login renrendai website
    i = 1
    base = 2526299
    for loanid in range(100000):
        base = base + parse_userinfo(loanid + base)
        print(i)
        i += 1  # check how many times of this program loop

    time_end = time.clock()
    print("\nElapsed time: %s seconds" % (str(time_end - time_start)))
