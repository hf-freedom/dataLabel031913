# -*- coding: utf-8 -*-
import random
import string
import os
import threading
import time
from playwright.sync_api import sync_playwright
from datetime import datetime
import pandas as pd

SCREENSHOT_DIR = r"C:\Users\12824\Desktop\dataLabel\0319\p13\login_picture"
EXCEL_FILE = "registration_data.xlsx"

FIRST_NAMES = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴", "徐", "孙", "马", "朱", "胡", "郭", "何", "高", "林", "罗"]
LAST_NAMES = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞"]

registration_results = []
results_lock = threading.Lock()

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_email():
    username = generate_random_string(10)
    return "{0}@163.com".format(username)

def generate_random_password():
    return generate_random_string(12) + random.choice(string.ascii_uppercase) + random.choice(string.digits)

def generate_random_name():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return first_name + last_name

def generate_random_age():
    return str(random.randint(18, 60))

def generate_random_phone():
    prefixes = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                "150", "151", "152", "153", "155", "156", "157", "158", "159",
                "170", "176", "177", "178",
                "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"]
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices(string.digits, k=8))
    return prefix + suffix

def ensure_screenshot_dir():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
        print("创建截图目录: {0}".format(SCREENSHOT_DIR))

def find_input(page, selectors, field_name):
    for selector in selectors:
        try:
            element = page.query_selector(selector)
            if element:
                return element
        except:
            continue
    return None

def find_submit_button(page):
    submit_selectors = [
        'button:has-text("注册")',
        'button:has-text("提交")',
        'button:has-text("确定")',
        'input[type="submit"]',
        'input[value="注册"]',
        'input[value="提交"]',
        '.register-btn',
        '#register-btn',
        'button[type="submit"]'
    ]
    
    for selector in submit_selectors:
        try:
            submit_btn = page.query_selector(selector)
            if submit_btn:
                return submit_btn
        except:
            continue
    return None

def find_login_button(page):
    login_selectors = [
        'button:has-text("登录")',
        'button:has-text("登 录")',
        'input[type="submit"]',
        'input[value="登录"]',
        '.login-btn',
        '#login-btn',
        'button[type="submit"]'
    ]
    
    for selector in login_selectors:
        try:
            login_btn = page.query_selector(selector)
            if login_btn:
                return login_btn
        except:
            continue
    return None

def find_login_link(page):
    login_selectors = [
        'text=登录',
        'a:has-text("登录")',
        '[href*="login"]'
    ]
    
    for selector in login_selectors:
        try:
            element = page.query_selector(selector)
            if element:
                return element
        except:
            continue
    return None

def register_single_user(user_id):
    start_time = time.time()
    
    username = "user_" + generate_random_string(6)
    password = generate_random_password()
    email = generate_random_email()
    name = generate_random_name()
    age = generate_random_age()
    phone = generate_random_phone()
    
    registration_success = False
    login_success = False
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            print("[用户{0}] 开始注册流程...".format(user_id))
            
            page.goto("http://39.107.109.8:8082/", timeout=30000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
            
            register_link = page.query_selector('text=注册') or page.query_selector('text=立即注册') or page.query_selector('a:has-text("注册")')
            
            if register_link:
                register_link.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(1000)
            
            username_selectors = [
                'input[name="username"]', 'input[name="user"]', 'input[name="userName"]',
                'input[placeholder*="用户名"]', 'input[placeholder*="账号"]',
                '#username', '#userName', 'input[type="text"]:first-of-type'
            ]
            
            password_selectors = [
                'input[name="password"]', 'input[name="pwd"]', 'input[name="userPassword"]',
                'input[placeholder*="密码"]', '#password', '#pwd', 'input[type="password"]'
            ]
            
            email_selectors = [
                'input[name="email"]', 'input[name="mail"]', 'input[placeholder*="邮箱"]',
                'input[placeholder*="Email"]', '#email', 'input[type="email"]'
            ]
            
            name_selectors = [
                'input[name="name"]', 'input[name="realName"]', 'input[name="realname"]',
                'input[placeholder*="姓名"]', 'input[placeholder*="真实姓名"]',
                '#name', '#realName'
            ]
            
            age_selectors = [
                'input[name="age"]', 'input[placeholder*="年龄"]', '#age', 'input[type="number"]'
            ]
            
            phone_selectors = [
                'input[name="phone"]', 'input[name="mobile"]', 'input[name="tel"]',
                'input[placeholder*="手机"]', 'input[placeholder*="电话"]',
                'input[placeholder*="手机号"]', '#phone', '#mobile'
            ]
            
            username_input = find_input(page, username_selectors, "用户名")
            password_input = find_input(page, password_selectors, "密码")
            email_input = find_input(page, email_selectors, "邮箱")
            name_input = find_input(page, name_selectors, "姓名")
            age_input = find_input(page, age_selectors, "年龄")
            phone_input = find_input(page, phone_selectors, "手机号")
            
            if username_input:
                username_input.fill(username)
            if password_input:
                password_input.fill(password)
            if email_input:
                email_input.fill(email)
            if name_input:
                name_input.fill(name)
            if age_input:
                age_input.fill(age)
            if phone_input:
                phone_input.fill(phone)
            
            page.wait_for_timeout(500)
            
            submit_btn = find_submit_button(page)
            if submit_btn:
                submit_btn.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2000)
                registration_success = True
                print("[用户{0}] 注册成功!".format(user_id))
            else:
                print("[用户{0}] 未找到注册按钮".format(user_id))
            
            if registration_success:
                print("[用户{0}] 开始登录验证...".format(user_id))
                
                login_link = find_login_link(page)
                if login_link:
                    login_link.click()
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(1000)
                
                login_username_input = find_input(page, username_selectors, "登录用户名")
                login_password_input = find_input(page, password_selectors, "登录密码")
                
                if login_username_input:
                    login_username_input.fill(username)
                if login_password_input:
                    login_password_input.fill(password)
                
                page.wait_for_timeout(500)
                
                login_btn = find_login_button(page)
                if login_btn:
                    login_btn.click()
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(3000)
                    
                    if page.query_selector('text=个人中心') or page.query_selector('text=用户信息') or page.query_selector('text=我的') or page.query_selector('text=欢迎') or page.query_selector('text=用户名') or page.query_selector('text=账号') or page.url.find('user') != -1 or page.url.find('profile') != -1 or page.url.find('center') != -1 or page.url.find('home') != -1:
                        login_success = True
                        print("[用户{0}] 登录验证成功 - 用户信息正常!".format(user_id))
                    else:
                        print("[用户{0}] 登录成功但未检测到个人信息页面，手动截图确认".format(user_id))
                else:
                    print("[用户{0}] 未找到登录按钮".format(user_id))
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "user_{0}_{1}.png".format(user_id, timestamp))
            page.screenshot(path=screenshot_path)
            
            browser.close()
        
    except Exception as e:
        print("[用户{0}] 发生错误: {1}".format(user_id, e))
    finally:
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        result = {
            "用户ID": user_id,
            "用户名": username,
            "密码": password,
            "邮箱": email,
            "姓名": name,
            "年龄": age,
            "手机号": phone,
            "注册状态": "成功" if registration_success else "失败",
            "登录验证": "通过" if login_success else "未通过",
            "耗时(秒)": duration,
            "注册时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with results_lock:
            registration_results.append(result)
        
        return result

def save_to_excel(results):
    if not results:
        print("没有数据需要保存到Excel")
        return
        
    df = pd.DataFrame(results)
    
    cols = ["用户ID", "用户名", "密码", "邮箱", "姓名", "年龄", "手机号", "注册状态", "登录验证", "耗时(秒)", "注册时间"]
    df = df[cols]
    
    if os.path.exists(EXCEL_FILE):
        existing_df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")
    print("\n注册数据已保存到: {0}".format(os.path.abspath(EXCEL_FILE)))
    print("本次共记录 {0} 条数据".format(len(results)))

def main():
    ensure_screenshot_dir()
    
    num_users = 5
    print("=" * 60)
    print("批量自动注册脚本 - 并发注册 {0} 个用户".format(num_users))
    print("=" * 60)
    
    overall_start_time = time.time()
    
    threads = []
    for i in range(num_users):
        thread = threading.Thread(target=register_single_user, args=(i + 1,))
        threads.append(thread)
        thread.start()
        time.sleep(1)
    
    for thread in threads:
        thread.join()
    
    overall_end_time = time.time()
    total_duration = round(overall_end_time - overall_start_time, 2)
    
    print("\n" + "=" * 60)
    print("注册结果汇总:")
    print("-" * 60)
    
    for result in registration_results:
        status = "✓" if result["注册状态"] == "成功" else "✗"
        verify = "✓" if result["登录验证"] == "通过" else "✗"
        print("用户{0}: {1} - 注册{2} 验证{3} - 耗时{4}秒".format(
            result["用户ID"], result["用户名"], status, verify, result["耗时(秒)"]))
    
    print("-" * 60)
    print("总耗时: {0} 秒".format(total_duration))
    print("成功注册: {0}/{1}".format(sum(1 for r in registration_results if r["注册状态"] == "成功"), num_users))
    print("验证通过: {0}/{1}".format(sum(1 for r in registration_results if r["登录验证"] == "通过"), num_users))
    print("=" * 60)
    
    save_to_excel(registration_results)

if __name__ == "__main__":
    main()
