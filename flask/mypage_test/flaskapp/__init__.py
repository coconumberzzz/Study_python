from flask import Flask, render_template,request,url_for, redirect
import pymysql,json

app=Flask(__name__)
app.debug=True
@app.route("/tutor_mypage",methods=["POST","GET"])
#_내 강의목록
def tutor_lecture():
    db = pymysql.connect(host='127.0.0.1',
        port=3306,
        user='admin',
        passwd='0507',
        db='attendance',
        charset='utf8')
    cursor=db.cursor()

    query = "SELECT CLASS_INFO.CLASS_NAME FROM CLASS_INFO,TUTOR_INFO WHERE TUTOR_INFO.TUTOR_ID=CLASS_INFO.TUTOR_ID;"

    cursor.execute(query)
    data=(cursor.fetchall())

    query="SELECT TUTEE_INFO.NAME,ATTENDANCE.PASS_TIME,ATTENDANCE.STATUS FROM CLASS_INFO,TUTEE_INFO,ATTENDANCE,TUTEE_CLASS_MAPPING WHERE ATTENDANCE.MAPPING_ID = TUTEE_CLASS_MAPPING.MAPPING_ID AND TUTEE_CLASS_MAPPING.TUTEE_ID=TUTEE_INFO.TUTEE_ID AND CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID AND CLASS_INFO.CLASS_NAME='linux'"

    cursor.execute(query)
    data2=(cursor.fetchall())

    query="SELECT CLASS_INFO.CLASS_NAME,CLASS_INFO.CLASS_TIME,CLASS_ROOM,ATTENDANCE.DATE FROM CLASS_INFO,ATTENDANCE,TUTOR_INFO,TUTEE_CLASS_MAPPING WHERE ATTENDANCE.MAPPING_ID = TUTEE_CLASS_MAPPING.MAPPING_ID AND CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID AND CLASS_INFO.TUTOR_ID=TUTOR_INFO.TUTOR_ID"
    
    cursor.execute(query)
    data3=(cursor.fetchall())

    cursor.close()
    db.close()

    datalist=[]       
    for row in data:
        if row :  #튜터마이페이지 > 강의목록
            dic={'CLASS_INFO.CLASS_NAME':row[0:]}
            datalist.append(dic)

    for row in data2:
        if row :  #튜터마이페이지 > 학생목록
            dic={'TUTEE_INFO.NAME':row[0:],'ATTENDANCE.PASS_TIME':row[0:],'ATTENDANCE.STATUS':row[0:]}
            datalist.append(dic)
    
    for row in data3:
        if row :  #튜터마이페이지 > 캘린더
            dic={'CLASS_INFO.CLASS_NAME':row[0:],'CLASS_INFO.CLASS_TIME':row[0:],'CLASS_INFO.CLASS_ROOM':row[0:],'ATTENDANCE.DATE':row[0:]}
            datalist.append(dic)

    return json.dumps(datalist)
