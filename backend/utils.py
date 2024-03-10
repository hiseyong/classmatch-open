from random import randint
import requests
import reqConfig as info
from bs4 import BeautifulSoup

def login(login_id, login_pw):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    headers = {'User-Agent': user_agent,
               'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}

    session = requests.Session()
    session.headers.update(headers)

    url_login_page = 'https://hi.hana.hs.kr/member/login.asp'
    session.get(url_login_page)

    url_login_proc = 'https://hi.hana.hs.kr/proc/login_proc.asp'
    login_data = {'login_id': login_id, 'login_pw': login_pw, 'x': str(randint(10, 99)), 'y': str(randint(10, 99))}
    res = session.post(url_login_proc, headers={'Referer': url_login_page}, data=login_data)
    if '로그인 정보가 잘못되었습니다.' in res.text:
        return False
    return session

def mobile_login(login_id, login_pw):
    session = requests.Session()

    login_data = {
        "mUsr_ID": login_id,
        "mUsr_PW": login_pw,
        "loginArr": "test1,test2,test6,teste,teste10,teste11,teste12,teste13,teste2,teste3,teste4,teste5,teste7,teste8,testest,testI,testm,testo,testp,tests,tests1,tests2,tests22,tests3",
        "push_Token": ""
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    while True:
        res = session.post("https://go.hana.hs.kr/json/loginProc.ajax", data=login_data, headers=headers)
        if 'success' in res.content.decode('utf-8'):
            break
    return session

def get_Id_Name(session):
    soup = BeautifulSoup(session.get('https://hi.hana.hs.kr/SYSTEM_Member/Member/MyPage/mypage.asp').text, 'html.parser')
    response = session.get('https://hi.hana.hs.kr/SYSTEM_Member/Member/MyPage/mypage.asp')
    start_index = response.text.find("학번 : ") + len("학번 : ")
    personal_code = response.text[start_index:start_index + 5]
    return personal_code, soup.select('[name="MUsr_Name"]')[0].get('value')

def get_Timetable(session):
    # mcode = 109
    # while True:
    #     res = session.get('https://hi.hana.hs.kr/SYSTEM_Sugang/Sugang_info/Subject_timeTale/sugang_timetable.asp?Mcode='+str(mcode))
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     timetable = soup.find_all('tr')
    #     timetable_edit=[]
    #     cls={}
    #     for i in timetable:
    #         for j in i.find_all('td'):
    #             if '교시' not in j.text:
    #                 timetable_edit.append(j.text.lstrip().split())
    #     for i in timetable_edit:
    #         if len(i) != 0:
    #             del i[-2]
    #             tot=''
    #             trashNum = 0
    #             for j in range(len(i[:-1])):
    #                 if '/' not in i[:-1][j]:
    #                     tot+=str(i[:-1][j])
    #                 else:
    #                     trashNum += 1
    #                     print(trashNum)
    #                 if j+1+trashNum < len(i[:-1]):
    #                     tot+=' '
    #             if tot[-1] == ' ':
    #                 tot = tot[:-1]
    #             cls[tot] = i[-1].split('/')[0].split(':')[1]
    #     if len(cls) != 0 or mcode == 111:
    #         break
    #     else:
    #         mcode += 1
    #
    # return cls
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    mcode = 109
    cls = {}
    while True:
        if mcode == 112:
            break
        response = session.get('https://go.hana.hs.kr/json/userTimeTable.ajax?mcode=' + str(mcode), headers=headers)
        classes = eval(response.content.decode('utf-8'))['resultList']
        if len(classes) == 0:
            mcode+=1
            continue
        for i in classes:
            cls[i['scodeName']] = i['divCode']
        break
    return cls



def get_personal_code(session):
    url_mypage = 'https://hi.hana.hs.kr/SYSTEM_Member/Member/MyPage/mypage.asp'
    response = session.get(url_mypage, headers={'Referer': 'https://hi.hana.hs.kr/'})

    start_index = response.text.find("조회용 개인번호 : ") + len("조회용 개인번호 : ")
    userid = response.text[start_index:start_index + 6]
    return userid