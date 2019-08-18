from flask import Flask, render_template,request,url_for, redirect
import pymysql,json

app=Flask(__name__)
app.debug=True
@app.route("/tutorMypage",methods=["POST","GET"])
#_튜터>강의목록
def tutorLecture():
    db = pymysql.connect(host='127.0.0.1',
        port=3306,
        user='admin',
        passwd='0507',
        db='attendance',
        charset='utf8')
    cursor=db.cursor()

    #튜터>강의목록
    query = "SELECT CLASS_INFO.CLASS_NAME FROM CLASS_INFO,TUTOR_INFO WHERE TUTOR_INFO.TUTOR_ID=CLASS_INFO.TUTOR_ID;"
    cursor.execute(query)
    data=(cursor.fetchall())
    datalist=[]
    for row in data:
        if row :        #튜터마이페이지 > 강의목록
            dic={'CLASS_INFO.CLASS_NAME':row[0:]}
            datalist.append(dic)
    i = json.dumps(dic)
    loaded_i = json.loads(i)
    cursor.close()
    db.close()
    return loaded_i

@app.route("/tutorStudent",methods=["POST","GET"])
#_튜터>학생목록
def tutorStudent():
    db = pymysql.connect(host='127.0.0.1',
        port=3306,
        user='admin',
        passwd='0507',
        db='attendance',
        charset='utf8')
    cursor=db.cursor()

    #튜터>학생목록
    query="SELECT TUTEE_INFO.NAME,ATTENDANCE.ENGAGEMENT,ATTENDANCE.STATUS FROM CLASS_INFO,TUTEE_INFO,ATTENDANCE,TUTEE_CLASS_MAPPING WHERE ATTENDANCE.MAPPING_ID = TUTEE_CLASS_MAPPING.MAPPING_ID AND TUTEE_CLASS_MAPPING.TUTEE_ID=TUTEE_INFO.TUTEE_ID AND CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID AND CLASS_INFO.CLASS_NAME='linux'"
    cursor.execute(query)
    data2=(cursor.fetchall())
    datalist=[]
    for row in data2:
        if row :        #튜터마이페이지 > 학생목록
            dic={'TUTEE_INFO.NAME':row[0:],'ATTENDANCE.PASS_TIME':row[0:],'ATTENDANCE.STATUS':row[0:]}
            datalist.append(dic)
    i = json.dumps(dic)
    loaded_i = json.loads(i)
    cursor.close()
    db.close()
    return loaded_i

@app.route("/tutorCalendar",methods=["POST","GET"])
#_튜터>달력
def tutorCalendar():
    db = pymysql.connect(host='127.0.0.1',
        port=3306,
        user='admin',
        passwd='0507',
        db='attendance',
        charset='utf8')
    cursor=db.cursor()

    #튜터>달력
    query="SELECT CLASS_INFO.CLASS_NAME,CLASS_INFO.CLASS_TIME,CLASS_INFO.CLASS_ROOM,ATTENDANCE.DATE FROM CLASS_INFO,ATTENDANCE,TUTOR_INFO,TUTEE_CLASS_MAPPING WHERE ATTENDANCE.MAPPING_ID = TUTEE_CLASS_MAPPING.MAPPING_ID AND CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID AND CLASS_INFO.TUTOR_ID=TUTOR_INFO.TUTOR_ID"
    cursor.execute(query)
    data3=(cursor.fetchall())
    datalist=[]
    for row in data3:
        if row :        #튜터마이페이지 > 캘린더
            dic={'CLASS_INFO.CLASS_NAME':row[0:],'CLASS_INFO.CLASS_TIME':row[0:],'CLASS_INFO.CLASS_ROOM':row[0:],'ATTENDANCE.DATE':row[0:]}
            datalist.append(dic)
    i = json.dumps(dic)
    loaded_i = json.loads(i)
    cursor.close()
    db.close()
    return loaded_i

@app.route("/tutorOgraph",methods=["POST","GET"])
#_튜터>출결현황그래프(각 인원수)
def tutorOgraph():
    db = pymysql.connect(host='127.0.0.1',
        port=3306,
        user='admin',
        passwd='0507',
        db='attendance',
        charset='utf8')
    cursor=db.cursor()
    
    #튜터>출결현황그래프(각 인원수)
    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'pass~~' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID; "
    cursor.execute(query)
    data4=(cursor.fetchall())
    datalist=[]
    for row in data4:   
        if row :        #튜터마이페이지 > 출결현황(출석)
            dic={'COUNT(STATUS)':row[0]}
            datalist.append(dic)
    for row in data4:
      data4=row[0]

    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'LATE' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID;"
    cursor.execute(query)
    data5=(cursor.fetchall())
    for row in data5:  
        if row :        #튜터마이페이지 > 출결현황(지각)
            dic={'COUNT(STATUS)':row[0]}
            datalist.append(dic)
    for row in data5:
      data5=row[0]

    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'FAIL' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID;"
    cursor.execute(query)
    data6=(cursor.fetchall())
    for row in data6:  
        if row :        #튜터마이페이지 > 출결현황(결석)
            dic={'COUNT(STATUS)':row[0]}
            datalist.append(dic)
    for row in data6:
      data6=row[0]

    #튜터>출결현황그래프>총인원
    query = "SELECT COUNT(CLASS_ID) FROM TUTEE_CLASS_MAPPING WHERE TUTEE_CLASS_MAPPING.CLASS_ID='1';"
    cursor.execute(query)
    data7=(cursor.fetchall())
    for row in data7:  
        if row :        #튜터마이페이지 > 출결현황(총인원)
            dic={'COUNT(STATUS)':row[0]}
            datalist.append(dic)
    for row in data7:
      data7=row[0]
    
    #튜터>출결현황그래프>날짜(최신,달력)
    query = "SELECT max(DATE) FROM ATTENDANCE WHERE DATE IN (SELECT max(DATE) FROM ATTENDANCE)"
    cursor.execute(query)
    data8=(cursor.fetchall())

    #출석, 지각, 결석 퍼센트 쿼리문
    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING WHERE TUTEE_CLASS_MAPPING.CLASS_ID='1' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND ATTENDANCE.DATE=%s AND ATTENDANCE.STATUS='pass~~';"
    value=(data8)
    cursor.execute(query,value)
    data9=(cursor.fetchall())
    percent=(cursor.fetchall())
    for row in percent:   #출석 퍼센트
      percent=row[0]
    percent=(int)((data4/data7)*100)
    for row in data9:  
        if row :        #튜터마이페이지 > 출결현황(출석퍼센트)
            dic={'pass%':'%s'%percent}
            datalist.append(dic)

    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING WHERE TUTEE_CLASS_MAPPING.CLASS_ID='1' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND ATTENDANCE.DATE=%s AND ATTENDANCE.STATUS='LATE';"
    value=(data8)
    cursor.execute(query,value)
    data10=(cursor.fetchall())
    percent2=(cursor.fetchall())
    for row in percent2:  #지각 퍼센트
      percent2=row[0]
    percent2=(int)((data5/data7)*100)
    for row in data10:  
        if row :        #튜터마이페이지 > 출결현황(지각퍼센트)
            dic={'late%':'%s'%percent2}
            datalist.append(dic)

    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING WHERE TUTEE_CLASS_MAPPING.CLASS_ID='1' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND ATTENDANCE.DATE=%s AND ATTENDANCE.STATUS='FAIL';"
    value=(data8)
    cursor.execute(query,value)
    data11=(cursor.fetchall())
    percent3=(cursor.fetchall())
    for row in percent3:  #결석 퍼센트
      percent3=row[0]
    percent3=(int)((data6/data7)*100)
    for row in data11:  
        if row :        #튜터마이페이지 > 출결현황(결석퍼센트)
            dic={'fail%':'%s'%percent3}
            datalist.append(dic)

    i = json.dumps(dic)
    loaded_i = json.loads(i)
    cursor.close()
    db.close()
    return loaded_i

@app.route("/tutorLgraph",methods=["POST","GET"])
#_튜터>출결현황그래프(각 인원수)
def tutorLgraph():
    db = pymysql.connect(host='127.0.0.1',
        port=3306,
        user='admin',
        passwd='0507',
        db='attendance',
        charset='utf8')
    cursor=db.cursor()

    #튜터>출결현황그래프>날짜(최신,달력)
    query = "SELECT max(DATE) FROM ATTENDANCE WHERE DATE IN (SELECT max(DATE) FROM ATTENDANCE)"
    cursor.execute(query)
    data8=(cursor.fetchall())

    #튜터>평균그래프
    query = "SELECT CLASS_INFO.CLASS_TIME,ATTENDANCE.PASS_TIME FROM ATTENDANCE,CLASS_INFO,TUTEE_CLASS_MAPPING WHERE CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID AND ATTENDANCE.MAPPING_ID=TUTEE_CLASS_MAPPING.MAPPING_ID AND ATTENDANCE.DATE=%s AND TUTEE_CLASS_MAPPING.TUTEE_ID='1'"
    value=(data8)
    cursor.execute(query,value)
    data12=(cursor.fetchall())
    datalist=[]
    for row in data12:
        if row :
            dic ={'CLASS_INFO.CLASS_TIME':row[0:],'ATTENDANCE.PASS_TIME':row[0:]}
            datalist.append(dic)
    
    i = json.dumps(data8)
    loaded_i=json.loads(i)
    cursor.close()
    db.close()
    return loaded_i

@app.route("/tuteeMypage",methods=["POST","GET"])
def tutee_lecture():
    db = pymysql.connect(host='127.0.0.1',
        port=3306,
        user='admin',
        passwd='0507',
        db='attendance',
        charset='utf8')
    cursor=db.cursor()
    #튜티>강의목록
    query = "SELECT CLASS_INFO.CLASS_NAME FROM CLASS_INFO,TUTEE_INFO,TUTEE_CLASS_MAPPING WHERE TUTEE_INFO.TUTEE_ID=TUTEE_CLASS_MAPPING.TUTEE_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID;"
    cursor.execute(query)
    data=(cursor.fetchall())

    datalist=[]       
    for row in data:
        if row :  #튜티마이페이지 > 강의목록
            dic={'CLASS_INFO.CLASS_NAME':row[0:]}
            datalist.append(dic)

    cursor.close()
    db.close()
    return json.dumps(datalist)
