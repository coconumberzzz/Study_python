#
#동적 uri
from flask import Flask, render_template,request,url_for, redirect
import pymysql,json

app=Flask(__name__)
app.debug=True
"""
@app.route ("/tutor_mypage")
def tutee_mypage():
    #return render_template(".html")
"""
#Tutor
@app.route("/tutor_mypage",methods=["POST","GET"])
#_내 강의목록
def tutor_lecture():
    #if request.method =="POST":  
        db = pymysql.connect(host='127.0.0.1',
            port=3306,
            user='admin',
            passwd='0507',
            db='attendance',
            charset='utf8')

        cursor=db.cursor()
        query = "SELECT CLASS_INFO.CLASS_NAME FROM CLASS_INFO WHERE TUTOR_INFO.TUTOR_ID=CLASS_INFO.TUTOR_ID;"
        # class_info 테이블의 tutor_id와 tutor_info의 tutor_id 가 같을 때, 
        # class_info 테이블의 class_name 추출
        cursor.execute(query)
        data=(cursor.fetchall())
        tutorlecture=[]       #튜터마이페이지>강의리스트

        cursor.close()
        db.close()

        for row in data:
            if row :  #튜터 마페, 강의목록
                dic={'CLASS_INFO.CLASS_NAME':row[0:]}
                tutorlecture.append(dic)

        return json.dumps(tutorlecture)

"""
def tutorlist():
  if request.method =="POST":  
    db = pymysql.connect(host='127.0.0.1',
        port=3306,
        user='admin',
        passwd='0507',
        db='attendance',
        charset='utf8')
    cursor=db.cursor()    
    query="SELECT TUTEE_INFO.NAME,ATTENDANCE.PASS_TIME,ATTENDANCE.STATUS FROM TUTEE_INFO,ATTENDANCE WHERE ATTENDANCE.MAPPING_ID = TUTEE_CLASS_MAPPING.MAPPING_ID AND TUTEE_CLASS_MAPPING.TUTEE_ID=TUTEE_INFO.TUTEE_ID AND CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID AND CLASS_INFO.CLASS_NAME='linux'"
        # attendance 테이블과 tutee_class_mapping 테이블의 mapping_id가 같아야함
        # class_info 테이블과 tutee_class_mapping 테이블의 class_id가 같아야함
        # tutee_class_mapping 테이블과 tutee_info테이블의 tutee_id가 같아야함
        # class_info 테이블의 class_name과 "사용자가 요청한 강의이름" 이 같아야함
        # tutee_info 테이블의 name 추출
        # attendance 테이블의 pass_time 과 status 추출
    cursor.execute(query)
    data2=(cursor.fetchall())
    tutorlist=[]          #튜터마이페이지>강의리스트>학생리스트
    cursor.close()
    db.close()
    for row in data2:
        if row : 
            dic={'TUTEE_INFO.NAME':row[0:],'ATTENDANCE.PASS_TIME':row[0:],'ATTENDANCE.STATUS':row[0:]}
            tutorlist.append(dic)

  return json.dumps(tutorlist)


#_수강학생리스트
def list_student():
    #if request.method =="POST":

        
#_선그래프, 학생 실시간 출석도
def lgraph():

    
#_원형그래프, 당일 강의의 학생 전체 출석률
def ograph():
  #Tutee
  @app.route("/tutee_mypage",methods=["POST","GET"])
  
  #_수강과목리스트
  def tutee_list():
      if request.method =="POST":
          db = pymysql.connect(host='127.0.0.1',
              port=3306,
              user='admin',
              passwd='0507',
              db='attendance',
              charset='utf8')
  
          cursor=db.cursor()
          query = "SELECT CLASS_INFO.CLASS_NAME, CLASS_INFO.CLASS_TIME, TUTOR_INFO.NAME 
          FROM CLASS_INFO, TUTOR_INFO
          WHERE TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID
          AND CLASS_INFO.TUTOR_ID=TUTOR_INFO.TUTOR_ID;"
          #튜티클래스맵핑 테이블의 분반고유값과 클래스정보 테이블의 분반고유값이 같으며 / 클래스정보테이블의 교수고유값과 튜터정보테이블의 교수고유값이 같을 때
          # 클래스정보 테이블의 수업이름, 수업시간과
          # 튜터정보테이블에서 교수 이름을 뺴온다.
          cursor.execute(query)
          data=(cursor.fetchall())
  
          tuteelist=[]
          for row in data:
              dic={'CLASS_NAME':row[0],'TUTOR_INFO.NAME':row[1], 'CLASS_TIME':row[2]}
              tuteelist.append(dic)
      
          return json.dumps(tuteelist)
  
  #_각 강의 출석그래프
  def tutee_graph():
    if request.method =="POST":
      db2 = pymysql.connect(host='127.0.0.1',
          port=3306,
          user='admin',
          passwd='0507',
          db2='attendance',
          charset='utf8')
          
          cursor2=db2.cursor()
          query = "SELECT  FROM ;"
      
          cursor2.execute(query)
          data2=(cursor2.fetchall())
"""