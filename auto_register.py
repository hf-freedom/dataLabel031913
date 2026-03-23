import random
import string
import os
from playwright.sync_api import sync_playwright
from datetime import datetime

SCREENSHOT_DIR = r"C:\Users\12824\Desktop\dataLabel\0319\p13\login_picture"

FIRST_NAMES = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴", "徐", "孙", "马", "朱", "胡", "郭", "何", "高", "林", "罗"]
LAST_NAMES = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞"]

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_email():
    username = generate_random_string(10)
    return f"{username}@163.com"

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
        print(f"创建截图目录: {SCREENSHOT_DIR}")

def auto_register():
    ensure_screenshot_dir()
    
    username = "user_" + generate_random_string(6)
    password = generate_random_password()
    email = generate_random_email()
    name = generate_random_name()
    age = generate_random_age()
    phone = generate_random_phone()
    
    print(f"准备注册信息:")
    print(f"  用户名: {username}")
    print(f"  密码: {password}")
    print(f"  邮箱: {email}")
    print(f"  姓名: {name}")
    print(f"  年龄: {age}")
    print(f"  手机号: {phone}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            print("\n正在打开网站...")
            page.goto("http://39.107.109.8:8082/", timeout=30000)
            page.wait_for_load_state("networkidle")
            
            print("等待页面加载...")
            page.wait_for_timeout(2000)
            
            print("查找注册链接...")
            register_link = page.query_selector('text=注册') or page.query_selector('text=立即注册') or page.query_selector('a:has-text("注册")')
            
            if register_link:
                print("点击注册链接...")
                register_link.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(1000)
            else:
                print("未找到注册链接，尝试直接查找注册表单...")
            
            print("\n查找注册表单字段...")
            
            username_selectors = [
                'input[name="username"]',
                'input[name="user"]',
                'input[name="userName"]',
                'input[placeholder*="用户名"]',
                'input[placeholder*="账号"]',
                '#username',
                '#userName',
                'input[type="text"]:first-of-type'
            ]
            
            password_selectors = [
                'input[name="password"]',
                'input[name="pwd"]',
                'input[name="userPassword"]',
                'input[placeholder*="密码"]',
                '#password',
                '#pwd',
                'input[type="password"]'
            ]
            
            email_selectors = [
                'input[name="email"]',
                'input[name="mail"]',
                'input[placeholder*="邮箱"]',
                'input[placeholder*="Email"]',
                '#email',
                'input[type="email"]'
            ]
            
            name_selectors = [
                'input[name="name"]',
                'input[name="realName"]',
                'input[name="realname"]',
                'input[name="userName"]',
                'input[placeholder*="姓名"]',
                'input[placeholder*="真实姓名"]',
                '#name',
                '#realName',
                '#userName'
            ]
            
            age_selectors = [
                'input[name="age"]',
                'input[placeholder*="年龄"]',
                '#age',
                'input[type="number"]'
            ]
            
            phone_selectors = [
                'input[name="phone"]',
                'input[name="mobile"]',
                'input[name="tel"]',
                'input[name="phoneNumber"]',
                'input[placeholder*="手机"]',
                'input[placeholder*="电话"]',
                'input[placeholder*="手机号"]',
                '#phone',
                '#mobile',
                '#tel'
            ]
            
            def find_input(selectors, field_name):
                for selector in selectors:
                    try:
                        element = page.query_selector(selector)
                        if element:
                            print(f"找到{field_name}输入框: {selector}")
                            return element
                    except:
                        continue
                return None
            
            username_input = find_input(username_selectors, "用户名")
            password_input = find_input(password_selectors, "密码")
            email_input = find_input(email_selectors, "邮箱")
            name_input = find_input(name_selectors, "姓名")
            age_input = find_input(age_selectors, "年龄")
            phone_input = find_input(phone_selectors, "手机号")
            
            print("\n填写注册信息...")
            
            if username_input:
                username_input.fill(username)
                print(f"已填写用户名: {username}")
            else:
                print("警告: 未找到用户名输入框")
            
            if password_input:
                password_input.fill(password)
                print(f"已填写密码: {password}")
            else:
                print("警告: 未找到密码输入框")
            
            if email_input:
                email_input.fill(email)
                print(f"已填写邮箱: {email}")
            else:
                print("警告: 未找到邮箱输入框")
            
            if name_input:
                name_input.fill(name)
                print(f"已填写姓名: {name}")
            else:
                print("警告: 未找到姓名输入框")
            
            if age_input:
                age_input.fill(age)
                print(f"已填写年龄: {age}")
            else:
                print("警告: 未找到年龄输入框")
            
            if phone_input:
                phone_input.fill(phone)
                print(f"已填写手机号: {phone}")
            else:
                print("警告: 未找到手机号输入框")
            
            page.wait_for_timeout(500)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filled_screenshot = os.path.join(SCREENSHOT_DIR, f"register_filled_{timestamp}.png")
            page.screenshot(path=filled_screenshot)
            print(f"\n已保存填写完成截图: {filled_screenshot}")
            
            print("\n查找注册按钮...")
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
            
            submit_btn = None
            for selector in submit_selectors:
                try:
                    submit_btn = page.query_selector(selector)
                    if submit_btn:
                        print(f"找到注册按钮: {selector}")
                        break
                except:
                    continue
            
            if submit_btn:
                print("点击注册按钮...")
                submit_btn.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(3000)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                success_screenshot = os.path.join(SCREENSHOT_DIR, f"register_success_{timestamp}.png")
                page.screenshot(path=success_screenshot)
                print(f"已保存注册结果截图: {success_screenshot}")
                
                print("\n注册流程完成!")
            else:
                print("警告: 未找到注册按钮")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                no_btn_screenshot = os.path.join(SCREENSHOT_DIR, f"register_no_button_{timestamp}.png")
                page.screenshot(path=no_btn_screenshot)
                print(f"已保存当前页面截图: {no_btn_screenshot}")
            
            print("\n按Enter键关闭浏览器...")
            input()
            
        except Exception as e:
            print(f"发生错误: {e}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            error_screenshot = os.path.join(SCREENSHOT_DIR, f"register_error_{timestamp}.png")
            try:
                page.screenshot(path=error_screenshot)
                print(f"已保存错误截图: {error_screenshot}")
            except:
                pass
        finally:
            browser.close()
    
    return {
        "username": username,
        "password": password,
        "email": email,
        "name": name,
        "age": age,
        "phone": phone
    }

if __name__ == "__main__":
    print("=" * 50)
    print("自动注册脚本")
    print("=" * 50)
    
    result = auto_register()
    
    print("\n" + "=" * 50)
    print("注册信息汇总:")
    print(f"  用户名: {result['username']}")
    print(f"  密码: {result['password']}")
    print(f"  邮箱: {result['email']}")
    print(f"  姓名: {result['name']}")
    print(f"  年龄: {result['age']}")
    print(f"  手机号: {result['phone']}")
    print("=" * 50)
