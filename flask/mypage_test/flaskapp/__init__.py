from flask import Flask, render_template,request,url_for, redirect
import pymysql,json

app=Flask(__name__)
app.debug=True
@app.route("/tutorMypage",methods=["POST","GET"])
#_내 강의목록
def tutor_lecture():
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

    #튜터>학생목록
    query="SELECT TUTEE_INFO.NAME,ATTENDANCE.ENGAGEMENT,ATTENDANCE.STATUS FROM CLASS_INFO,TUTEE_INFO,ATTENDANCE,TUTEE_CLASS_MAPPING WHERE ATTENDANCE.MAPPING_ID = TUTEE_CLASS_MAPPING.MAPPING_ID AND TUTEE_CLASS_MAPPING.TUTEE_ID=TUTEE_INFO.TUTEE_ID AND CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID AND CLASS_INFO.CLASS_NAME='linux'"
    cursor.execute(query)
    data2=(cursor.fetchall())

    #튜터>달력
    query="SELECT CLASS_INFO.CLASS_NAME,CLASS_INFO.CLASS_TIME,CLASS_INFO.CLASS_ROOM,ATTENDANCE.DATE FROM CLASS_INFO,ATTENDANCE,TUTOR_INFO,TUTEE_CLASS_MAPPING WHERE ATTENDANCE.MAPPING_ID = TUTEE_CLASS_MAPPING.MAPPING_ID AND CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID AND CLASS_INFO.TUTOR_ID=TUTOR_INFO.TUTOR_ID"
    cursor.execute(query)
    data3=(cursor.fetchall())

    #튜터>출결현황그래프
    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'pass~~' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID; "
    cursor.execute(query)
    data4=(cursor.fetchall())

    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'LATE' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID;"
    cursor.execute(query)
    data5=(cursor.fetchall())

    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'FAIL' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID;"
    cursor.execute(query)
    data6=(cursor.fetchall())
    #c튜터>출결현황그래프>총인원
    query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID AND STATUS = 'pass~~' OR STATUS='LATE' OR STATUS='FAIL'; "
    cursor.execute(query)
    data7=(cursor.fetchall())

    #튜터>출결현황그래프>pass %
    query = "SELECT COUNT(STATUS)/data7 FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID AND STATUS = 'pass~~'; "
    cursor.execute(query)
    data8=(cursor.fetchall())

    datalist=[]       
    for row in data:
        if row :        #튜터마이페이지 > 강의목록
            dic={'CLASS_INFO.CLASS_NAME':row[0:]}
            datalist.append(dic)

    for row in data2:
        if row :        #튜터마이페이지 > 학생목록
            dic={'TUTEE_INFO.NAME':row[0:],'ATTENDANCE.PASS_TIME':row[0:],'ATTENDANCE.STATUS':row[0:]}
            datalist.append(dic)
    
    for row in data3:
        if row :        #튜터마이페이지 > 캘린더
            dic={'CLASS_INFO.CLASS_NAME':row[0:],'CLASS_INFO.CLASS_TIME':row[0:],'CLASS_INFO.CLASS_ROOM':row[0:],'ATTENDANCE.DATE':row[0:]}
            datalist.append(dic)

    for row in data4:   
        if row :        #튜터마이페이지 > 출결현황(출석)
            dic={'COUNT(STATUS)':row[0]}
            datalist.append(dic)

    for row in data5:  
        if row :        #튜터마이페이지 > 출결현황(지각)
            dic={'COUNT(STATUS)':row[0]}
            datalist.append(dic)

    for row in data6:  
        if row :        #튜터마이페이지 > 출결현황(결석)
            dic={'COUNT(STATUS)':row[0]}
            datalist.append(dic)

    for row in data7:  
        if row :        #튜터마이페이지 > 출결현황(총인원)
            dic={'COUNT(STATUS)':row[0]}
            datalist.append(dic)

    for row in data8:  
        if row :        #튜터마이페이지 > 출결현황(출석퍼센트)
            dic={'COUNT(STATUS)/data7':row[0]}
            datalist.append(dic)

    cursor.close()
    db.close()
    return json.dumps(datalist)

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
