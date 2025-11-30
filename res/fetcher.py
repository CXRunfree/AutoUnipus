# encoding=utf-8
import re
import uuid

import requests
import json
from requests import JSONDecodeError


def resolve_url(pre_url):
    pattern_course = re.compile("(?<=#).+(?=/courseware)")
    pattern_chapter = re.compile("/u[0-9]+g[0-9]+/")
    course = re.findall(pattern_course, pre_url)[0]
    chapter = re.findall(pattern_chapter, pre_url)[-1]
    return course, chapter


# 解析json内容提取答案
def __sort_ans__(r, num):
    answer = []
    content = r["data"]["user_answers"]
    for i in range(num):
        ans_dic = {
            "choice": content[str(i)]["student_answer"],
            "isRight": content[str(i)]["isRight"]
        }
        answer.append(ans_dic)
    return answer


# 验证测试的答案是否正确,依此修改答案
def __change_ans__(answer):
    flag = True
    codes = "ABCDEFG"
    for ans in answer:
        if not ans["isRight"]:
            index = codes.find(ans["choice"]) + 1
            if index >= len(codes):
                continue
            else:
                ans["choice"] = codes[index]
            flag = False
    return answer, flag


# 修改要post的data
def __change_data__(answer, data):
    num = len(answer)
    for i in range(num):
        new_ans = {
            "index": i,
            "answer": answer[i]["choice"]
        }
        data["answers"][str(i)]["user_answer"]["answer"] = new_ans


def __resolve_qid__(qid_dic) -> list:
    qids = []
    for a in qid_dic.values():
        for b in a.values():
            qid = b["qid"]
            qids.append(qid)
    return qids


def verify_key(key):
    if not key:
        return False
    verify = False
    system_uuid = uuid.getnode()
    try:
        with open("_internal/api-ms-win-crt-log-l1-1-0.dll", "r", encoding="utf-8") as f:
            owner_uuid = json.load(f)["owner_id"]
    except:
        return False
    if system_uuid == owner_uuid or owner_uuid == "Author":
        index, add = 0, 0
        rawkey = ''
        verify = True
        for i in range(len(key)):
            if i == index:
                rawkey += key[i]
                index += 1 + add
                add += 1
        for i in rawkey:
            try:
                num = int(i)
                verify = False
                break
            except:
                continue
    return verify


def fetch_qid(page):
    # 解析当前网址获取qid所在url
    pre_url = page.url
    course, chapter = resolve_url(pre_url)
    qid_url = "https://ucontent.unipus.cn/course/api/pc/summary" + course + chapter + "default/"
    # 获取网站的验证密钥
    auth_jwt = page.evaluate("localStorage.jwtToke")
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'X-Annotator-Auth-Token': auth_jwt
    }
    # 请求qid_url获取题目的qid --- questionID
    r = requests.get(qid_url, headers=headers).json()["summary"]
    if not r:
        return []
    qids = __resolve_qid__(r["indexMap"])
    return qids


def fetch_ans(page, total: int, qid: str):
    answer = []
    # 获取网站的验证密钥
    auth_jwt = page.evaluate("localStorage.jwtToke")
    # 解析网址获取提交网址
    course, chapter = resolve_url(page.url)
    url = "https://ucontent.unipus.cn/course/api/v3/submit" + course + chapter
    # 构造header
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'X-Annotator-Auth-Token': auth_jwt
        }
    # 构造data
    data = {
        "answers": {}
    }
    for i in range(total):
        user_answer = {"user_answer": {
            "qid": qid,
            "answer": {"index": i, "answer": "A"}}}
        data["answers"][str(i)] = user_answer
    # 获取全对答案
    flag = False
    while not flag:
        r = requests.post(url, data=json.dumps(data), headers=headers)  # json.dumps matters
        try:
            answer = __sort_ans__(r.json(), total)
        except JSONDecodeError:
            return [{"isRight": False}]
        answer, flag = __change_ans__(answer)
        __change_data__(answer, data)
    return answer
