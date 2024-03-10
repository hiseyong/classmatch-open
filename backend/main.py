from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import utils
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
import pymysql

db_config = {
    '''
    DB정보이므로 비공개
    '''
}


BASE_DIR = Path(__file__).resolve().parent

#templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
root = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
class resisterData(BaseModel):
    id: str
    pw: str

class matchData(BaseModel):
    year: str
    id1: str
    id2: str

class get_Class_Model(BaseModel):
    id: str

class get_People_Model(BaseModel):
    year: str

class get_onwtwoclass_Model(BaseModel):
    year: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/resister")
def index(userInfo:resisterData):
      connection = pymysql.connect(**db_config)
      cursor = connection.cursor()
      session = utils.login(userInfo.id,userInfo.pw)
      if session == False:
          return '계정이 잘못됐습니다.'
      userid, username = utils.get_Id_Name(session)
      mobile_session = utils.mobile_login(userInfo.id,userInfo.pw)
      cls = utils.get_Timetable(mobile_session)
      query = """DB 정보이므로 비공개"""
      cursor.execute(query)
      if len(cursor.fetchall()) != 0:
        query = """DB 정보이므로 비공개"""
        cursor.execute(query)
        connection.commit()
      else:
        query = """DB 정보이므로 비공개"""
        cursor.execute(query)
        connection.commit()
      connection.close()
      return 'success'


@app.post("/api/match")
def index(userInfo:matchData):
      connection = pymysql.connect(**db_config)
      cursor = connection.cursor()
      query = """DB 정보이므로 비공개"""
      cursor.execute(query)
      cls = cursor.fetchall()
      if len(cls) == 0:
          connection.close()
          return '이름1은 등록되지 않은 이름입니다'

      cls1 = {}
      for i in cls:
          if i[0][:2] == userInfo.year:
            cls1 = i
      if len(cls1) == 0:
          connection.close()
          return '이름1은 등록되지 않은 이름입니다'
      cls1 = eval(cls1[2])


      query = """DB 정보이므로 비공개"""
      cursor.execute(query)
      cls = cursor.fetchall()
      if len(cls) == 0:
        connection.close()
        return '이름2는 등록되지 않은 이름입니다'

      cls2 = {}
      for i in cls:
          if i[0][:2] == userInfo.year:
            cls2 = i
      if len(cls2) == 0:
          connection.close()
          return '이름2는 등록되지 않은 이름입니다'
      cls2 = eval(cls2[2])


      match = []
      for i in cls1.keys():
          try:
              classname = i
              othersex = i
              if '(남)' in i:
                  othersex = othersex.replace('(남)','(여)')
                  classname = classname.replace('(남)','')
              if '(여)' in i:
                  othersex = othersex.replace('(여)','(남)')
                  classname = classname.replace('(여)','')
              if cls1[i] == cls2[i]:
                  match.append(classname + '(' + cls1[i] + '분반)')
          except:
              try:
                  if cls1[i] == cls2[othersex]:
                      match.append(classname + '(' + cls1[i] + '분반)')
              except:
                  continue

      connection.close()
      return match

@app.post('/api/getclass')
def get_class(userInfo:get_Class_Model):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = """DB 정보이므로 비공개"""
    cursor.execute(query)
    userClass = cursor.fetchall()
    if len(userClass) == 0:
        return '등록되지 않은 학생입니다'
    userClass = eval(userClass[0][2])
    query = """DB 정보이므로 비공개"""
    cursor.execute(query)
    allUserClass = cursor.fetchall()
    sortedUserClass = []
    for i in allUserClass:
        if i[0][:2] == userInfo.id[:2]:
            sortedUserClass.append(i)

    matchedClasses = {}
    for i in userClass.keys():
        classname = i
        if '(남)' in i:
            classname = classname.replace('(남)','')
        if '(여)' in i:
            classname = classname.replace('(여)','')
        matchedClasses[classname] = [userClass[i],[]]

    for i in sortedUserClass:
        tempClass = eval(i[2])
        for j in userClass.keys():
            classname = j
            if '(남)' in j:
                classname = classname.replace('(남)', '')
            if '(여)' in j:
                classname = classname.replace('(여)', '')
            try:
                if tempClass[j] == userClass[j]:
                    matchedClasses[classname][1].append(i[0]+i[1])
            except:
                try:
                    if tempClass[classname+'(남)'] == userClass[classname+'(남)']:
                        matchedClasses[classname][1].append(i[0] + i[1])
                except:
                    try:
                        if tempClass[classname + '(남)'] == userClass[classname + '(여)']:
                            matchedClasses[classname][1].append(i[0] + i[1])
                    except:
                        try:
                            if tempClass[classname + '(여)'] == userClass[classname + '(남)']:
                                matchedClasses[classname][1].append(i[0] + i[1])
                        except:
                            try:
                                if tempClass[classname + '(여)'] == userClass[classname + '(여)']:
                                    matchedClasses[classname][1].append(i[0] + i[1])
                            except:
                                continue

    for i in matchedClasses:
        eachClassMembers = matchedClasses[i][1]
        go = True
        while go:
            go = False
            for j in range(len(eachClassMembers)-1):
                if eachClassMembers[j] > eachClassMembers[j+1]:
                    go = True
                    temp = eachClassMembers[j+1]
                    eachClassMembers[j+1] = eachClassMembers[j]
                    eachClassMembers[j] = temp
        matchedClasses[i][1] = eachClassMembers
    for i in matchedClasses:
        for j in range(len(matchedClasses[i][1])):
            matchedClasses[i][1][j] = matchedClasses[i][1][j][0:5]+' '+matchedClasses[i][1][j][5:]

    connection.close()
    return matchedClasses

@app.post('/api/getpeople')
def get_people(userInfo:get_People_Model):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = """DB 정보이므로 비공개"""
    cursor.execute(query)
    allUserClass = cursor.fetchall()
    sortedUserClass = []
    for i in allUserClass:
        if i[0][:2] == userInfo.year:
            sortedUserClass.append(i)

    go = True
    while go:
        go = False
        for i in range(len(sortedUserClass)-1):
            if sortedUserClass[i] > sortedUserClass[i+1]:
                go = True
                temp = sortedUserClass[i+1]
                sortedUserClass[i+1] = sortedUserClass[i]
                sortedUserClass[i] = temp

    connection.close()
    return sortedUserClass

# current_directory = Path(__file__).parent
# static_path = current_directory.parent / "frontend" / "build"
#
# app.mount("/getpeople", StaticFiles(directory=str(static_path), html=True), name="static")
# @app.get("/getpeople")
# def read_root():
#     return FileResponse("../frontend/build/index.html")
#
# app.mount("/getclass", StaticFiles(directory=str(static_path), html=True), name="static")
# @app.get("/getclass")
# def read_root():
#     return FileResponse("../frontend/build/index.html")
#
# app.mount("/browse", StaticFiles(directory=str(static_path), html=True), name="static")
# @app.get("/browse")
# def read_root():
#     return FileResponse("../frontend/build/index.html")
#
# app.mount("/register", StaticFiles(directory=str(static_path), html=True), name="static")
# @app.get("/register")
# def read_root():
#     return FileResponse("../frontend/build/index.html")
#
#
# app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")
# @app.get("/")
# def read_root():
#     return FileResponse("../frontend/build/index.html")