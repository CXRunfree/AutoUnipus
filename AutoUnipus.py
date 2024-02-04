import json
import re
import time
import traceback
from res import fetcher
from playwright.sync_api import sync_playwright
from playwright._impl._errors import TargetClosedError


def auto_login(page, _user, _pwd):
    print("[Tip]图形验证码需手动输入.")
    login_url = "https://u.unipus.cn/user/student"
    page.goto(login_url)
    page.locator('[name="username"]').fill(_user)
    page.locator('[name="password"]').fill(_pwd)
    page.locator('[type="checkbox"]').all()[1].click()
    submit = page.locator(".btn.btn-login.btn-fill")
    submit.click()
    print("[Tip]出现安全验证不必担心,手动认证就好了.")
    page.wait_for_timeout(1000)
    print("[Tip]目前只支持单选题作答!")
    try:
        page.wait_for_selector('#pw-captchaCode', timeout=800)
        page.eval_on_selector('#pw-captchaCode', 'el => el.placeholder = "PS:请手动输入图形验证码"')
    except:
        return


def get_exercise(page):
    must_exe = []
    page.wait_for_selector(".icon-lianxi.iconfont")
    exercise = page.locator(".icon-lianxi.iconfont").all()
    for each in exercise:
        if each.locator(".iconfont").count():
            must_exe.append(each)
    return must_exe


def auto_answer(page, auto_mode):
    flag = False  # 用于判断是否有特殊题型
    # 获取题目的qid
    qids = fetcher.fetch_qid(page)
    if not qids:
        return not flag
    # qid为题目的标识符,据此进行答案获取
    single_choice = ".questions--questionDefault-2XLzl.undefined"
    for qid in qids:
        page.wait_for_timeout(800)
        total_ques = page.query_selector_all(single_choice)
        answer = fetcher.fetch_ans(page, total=len(total_ques), qid=qid)
        rank = 0
        for ques in total_ques:
            if answer[rank]["isRight"] and ques.is_visible():
                choice = answer[rank]["choice"]
                select = ques.wait_for_selector(f'input[value="{choice}"]')
                page.wait_for_timeout(100)
                select.click()
                rank += 1
            else:
                flag = True
                break
        # 点击下一页(最后一页则为"提交")
        # 如果不是automode,则不进行提交
        if not auto_mode and qids.index(qid) == len(qids) - 1:
            break
        page.locator(".submit-bar-pc--btn-1_Xvo").all()[-1].click()
    # 答题结束
    if flag:  # 判断是否有特殊题型
        if auto_mode:
            page.eval_on_selector('.dialog-header-pc--dialog-header-2qsXD',
                                  'element => element.style.fontSize = "20px"')
            page.eval_on_selector('.dialog-header-pc--dialog-header-2qsXD',
                                  'element => element.innerHTML = "PS:&nbsp;&nbsp;&nbsp;存在不支持题型，本次答题不会提交"')
            page.wait_for_timeout(2000)
        else:
            return flag


def init_page():
    # 启动自带浏览器
    if driver == "Chrome":
        print("[Info]正在启动Chrome浏览器...")
        browser = p.chromium.launch(channel="chrome", headless=False)
    else:
        print("[Info]正在启动Edge浏览器...")
        browser = p.chromium.launch(channel="msedge", headless=False)
    context = browser.new_context()
    context.grant_permissions(['microphone', 'camera'])
    page = context.new_page()
    # 设置程序超时时限
    page.set_default_timeout(6000000)
    # 进行登录
    print("[Info]等待登录完成...")
    auto_login(page, user, pwd)
    page.wait_for_selector(".my_course_box")
    # 绕过环境检测
    page.locator(".layui-layer-btn0").click()
    page.wait_for_event("popup").close()
    # 设置浏览器视口大小
    viewsize = page.evaluate('''() => {
                   return {width: window.screen.availWidth,height: window.screen.availHeight};}''')
    viewsize["height"] -= 50
    page.set_viewport_size(viewsize)
    return page


def auto_func():
    page = init_page()
    # 根据用户数据进行选课
    class_urls = [url for url in account["class_url"] if "unipus" in url]
    for class_url in class_urls:
        page.goto(class_url)
        # 获取"必修"课程练习
        course = page.wait_for_selector(".cc_course_intro_text").text_content().strip()
        print(f"[Info]当前课程:{course.splitlines(keepends=False)[0]}")
        page.wait_for_selector(".icon-bixiu.iconCustumStyle.iconfont")  # truly valid wait
        must_exe = get_exercise(page)
        # 进行必修题目的答题
        for exe in must_exe[-1:]:
            page.reload()
            page.wait_for_selector(".icon-bixiu.iconCustumStyle.iconfont")
            exe.click()
            if must_exe.index(exe) == 0:
                page.wait_for_selector(".iKnow").click()  # 点击"我知道了"
            page.locator(".dialog-header-pc--close-yD7oN").click()  # 关闭提示框
            # 开始自动答题
            auto_answer(page, automode)
            page.goto(class_url)
        print(f"[Info]课程:{course.splitlines(keepends=False)[0]}已完成!")


def assist_func():
    page = init_page()
    title_pattern = re.compile("[0-9]+?\.[0-9]+?.+")
    print("[System]请先进入题目界面.")
    while True:
        input("[System]:按Enter获取答案:")
        page.reload()
        # 关闭提示框
        try:
            page.wait_for_selector(".dialog-header-pc--close-yD7oN", timeout=2500).click()
        except:
            print("[Error]当前为非答题页面!")
            continue
        # 开始获取答案
        print("[Info]正在获取答案,请稍等...")
        flag = auto_answer(page, automode)
        if flag:
            print("[Error]答案获取失败,不支持当前题型!")
            continue
        try:
            head = page.wait_for_selector(".layoutHeaderStyle--menuList-Ef90e", timeout=1000).text_content()
            title = re.findall(title_pattern, head)[0]
            print(f"[Info]获取 <<{title}>> 答案成功!")
        except:
            print("[Info]获取答案成功!")
            continue


if __name__ == '__main__':
    try:
        # 读取用户数据
        with open("account.json", "r", encoding="utf-8") as f:
            account = json.loads(f.read())
            user = account["username"].strip()
            pwd = account["password"].strip()
            driver = account["Driver"].strip()
            automode = account["Automode"]
        print("===== Runtime Log =====")
        with sync_playwright() as p:
            if automode:
                print("[System]Automode 已启动.")
                auto_func()
                print("所有课程已完成!!")
                input("按Enter退出程序...")
            else:
                print("[System]Assistmode 已启动.")
                assist_func()
    except TargetClosedError:
        print("[Error]糟糕,网页关闭了!")
    except TimeoutError:
        print("程序长时间无响应,自动退出...")

    except Exception as e:
        print(f"[Error]{e}")
        if type(e) == KeyError:
            print("[Tip]可能是account文件的配置出错")
        log = traceback.format_exc()
        with open("log.txt", "w", encoding="utf-8") as doc:
            doc.write(log)
        print("[Info]错误日志已保存至:log.txt")
        print("[Tip]系统出错,要不重启一下?")
    finally:
        time.sleep(1.5)
