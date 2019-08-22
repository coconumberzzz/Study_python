from flask import Flask, render_template,request,url_for, redirect,session,escape
from datetime import timedelta
import pymysql,json, hashlib,math

app=Flask(__name__)
app.debug=True
app.secret_key="temporary string"

@app.before_request
def befor_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=30)

@app.route("/")

@app.route("/<error>")
def index(error=None):
  return'%s' %error

@app.route("/tutorMypage")
def tutorMypage():
    if 'username' in session:
        result = '%s'%escape (session['username'])
        return render_template('tutor_mypage.html')
    else :
        return render_template('index.html')

@app.route("/tutorStudent")
def tutorStudent():
    if 'username' in session:
        result = '%s'%escape (session['username'])
        return render_template('tutor_mypage.html')
    else :
        return render_template('index.html')


@app.route("/tutorMypageProcess",methods=["POST","GET"])
#_튜터>강의목록
def tutorMypageProcess():
    if 'username' in session:
        result = '%s'%escape (session['username'])
        db = pymysql.connect(host='127.0.0.1',
          port=3306,
          user='admin',
          passwd='0507',
          db='attendance',
          charset='utf8')
        cursor=db.cursor()
        query = "SELECT TUTOR_ID FROM TUTOR_INFO WHERE EMAIL = %s" 
        value = (result)
        cursor.execute(query,value)
        key = (cursor.fetchall()) #tutor_id
        
        for row in key :
            key = row[0]

        if key:
            #튜터>강의목록
            query = "SELECT CLASS_NAME,CLASS_ID FROM CLASS_INFO WHERE TUTOR_ID=%s;"
            value=(key)
            cursor.execute(query,value)
            data=(cursor.fetchall())

            datalist=[]
            for row in data:
                if row :        #튜터마이페이지 > 강의목록
                    dic={'NAME':row[0],'ID':row[1]}
                    datalist.append(dic)

            DATA={'class_info':datalist}
            i = json.dumps(DATA)
            loaded_i = json.loads(i)
            cursor.close()
            db.close()
            return loaded_i
        else : 
            error = {'error':'error!error!error!'}
            r = json.dumps(error)
            loaded_r = json.loads(r)
            cursor.close()
            db.close()
            return redirect(url_for("index",error=loaded_r))

    else: #로그인 안됐을때 접근제한 처리
        error = {'error':'error!error!error!'}
        r = json.dumps(error)
        loaded_r = json.loads(r)
        return redirect(url_for("login",error=loaded_r))

@app.route("/tutorStudentProcess",methods=["POST","GET"])
#_튜터>학생목록
def tutorStudentProcess():
    if request.method == "GET":
        class_id=request.args.get("class_id")
        if 'username' in session:
            result = '%s'%escape (session['username'])
            db = pymysql.connect(host='127.0.0.1',
            port=3306,
            user='admin',
            passwd='0507',
            db='attendance',
            charset='utf8')
            cursor=db.cursor()
            query = "SELECT TUTOR_ID FROM TUTOR_INFO WHERE EMAIL = %s" 
            value = (result)
            cursor.execute(query,value)
            key = (cursor.fetchall())   #tutor_id
        
            for row in key :
                if row :
                    key = row[0]

            if key:
              #튜터>학생목록
                query="SELECT TUTEE_INFO.NAME,ENGAGEMENT,STATUS,TUTEE_INFO.TUTEE_ID FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO,TUTEE_INFO WHERE CLASS_INFO.CLASS_ID=%s AND CLASS_INFO.TUTOR_ID=%s AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.TUTEE_ID=TUTEE_INFO.TUTEE_ID AND CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID;"
                value=(class_id,key)
                cursor.execute(query,value)
                data2=(cursor.fetchall())
                
                datalist=[]

                for row in data2:
                    if row :        #튜터마이페이지 > 학생목록
                        dic={'tutee_name':row[0],'engagement':row[1],'status':row[2],'tutee_id':row[3]}
                        datalist.append(dic)
                DATA={'studentList':datalist}
                i = json.dumps(DATA)
                loaded_i = json.loads(i)
                cursor.close()
                db.close()
                return loaded_i
            else : 
                error = {'error':'error!error!error!'}
                r = json.dumps(error)
                loaded_r = json.loads(r)
                cursor.close()
                db.close()
                return redirect(url_for("index",error=loaded_r))

        else: #로그인 안됐을때 접근제한 처리
            error = {'error':'error!error!error!'}
            r = json.dumps(error)
            loaded_r = json.loads(r)
            return redirect(url_for("login",error=loaded_r))

@app.route("/tutorInfoProcess",methods=["POST","GET"])
#_튜터>강의
def tutorInfoProcess():
    class_id=request.args.get("class_id")
    db = pymysql.connect(host='127.0.0.1',
            port=3306,
            user='admin',
            passwd='0507',
            db='attendance',
            charset='utf8')
    cursor=db.cursor()


    query="SELECT CLASS_NAME FROM CLASS_INFO WHERE CLASS_ID =%s"
    value=(class_id)
    cursor.execute(query,value)
    data14=(cursor.fetchall())

    datalist=[]
    for row in data14:
        if row :        #튜터마이페이지 > 강의목록
            dic={'class_name':row[0]}
            datalist.append(dic)

            DATA={'class_info':datalist}
            i = json.dumps(DATA)
            loaded_i = json.loads(i)
            cursor.close()
            db.close()
            return loaded_i
        else :
            error = {'error':'error!error!error!'}
            r = json.dumps(error)
            loaded_r = json.loads(r)
            cursor.close()
            db.close()
            return redirect(url_for("index",error=loaded_r))


@app.route("/tutorCalendarProcess",methods=["POST","GET"])
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
        class_id=1

        query="SELECT COUNT(STATUS),DATE FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'pass' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=%s AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID GROUP BY DATE;"
        value=(class_id)
        cursor.execute(query,value)
        data=(cursor.fetchall())   #출석인원
        datalist=[]

        for row in data:
            if row :        #캘린더
                dic={'pass':row[0],'date':row[1]}
                datalist.append(dic)


        query="SELECT COUNT(STATUS),DATE FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'late' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=%s AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID GROUP BY DATE;"

        value=(class_id)
        cursor.execute(query,value)
        data2=(cursor.fetchall())   #지각인원
        
        for row in data2:
            if row :        #캘린더
                dic={'late':row[0],'date':row[1]}
                datalist.append(dic)

        query="SELECT COUNT(STATUS),DATE FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'fail' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=%s AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID GROUP BY DATE;"

        value=(class_id)
        cursor.execute(query,value)
        data3=(cursor.fetchall())   #결석인원

        for row in data3:
            if row :        #캘린더
                dic={'fail':row[0],'date':row[1]}
                datalist.append(dic)
        DATA = {'calendar':datalist}
        i = json.dumps(DATA)
        loaded_i = json.loads(i)
        cursor.close()
        db.close()
        return loaded_i


@app.route("/tutorOgraphProcess",methods=["POST","GET"])
#_튜터>출결현황그래프(각 인원수)
def tutorOgraphProcess():
        db = pymysql.connect(host='127.0.0.1',
          port=3306,
          user='admin',
          passwd='0507',
          db='attendance',
          charset='utf8')
        cursor=db.cursor()
        
        class_id=request.args.get("class_id")
        
        #튜터>출결현황그래프>날짜(최신,달력)
        query = "SELECT max(DATE) FROM ATTENDANCE WHERE DATE IN (SELECT max(DATE) FROM ATTENDANCE)"
        cursor.execute(query)
        data8=(cursor.fetchall())

        #튜터>출결현황그래프(각 인원수)
        query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'pass' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=%s AND ATTENDANCE.DATE=%s AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID;"
        value=(class_id,data8)
        cursor.execute(query,value)
        data4=(cursor.fetchall())   #출석인원
        datalist=[]
        for row in data4:   
            if row :        #튜터마이페이지 > 출결현황(출석)
                dic={'pass':row[0]}
                datalist.append(dic)
        for row in data4:
            data4=row[0]

        DATA={'attendance':datalist}
        i=json.dumps(DATA)
        loaded_i=json.loads(i)


        query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'late' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=%s AND ATTENDANCE.DATE=%s AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID;"
        value=(class_id,data8)
        cursor.execute(query,value)
        data5=(cursor.fetchall())
        for row in data5:  
            if row :        #튜터마이페이지 > 출결현황(지각)
                dic={'late':row[0]}
                datalist.append(dic)
        for row in data5:
            data5=row[0]

        DATA={'attendance':datalist}
        i=json.dumps(DATA)
        loaded_i=json.loads(i)


        query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING,CLASS_INFO WHERE STATUS = 'fail' AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=CLASS_INFO.CLASS_ID AND TUTEE_CLASS_MAPPING.CLASS_ID=%s AND ATTENDANCE.DATE=%s;"
        value=(class_id,data8)
        cursor.execute(query,value)
        data6=(cursor.fetchall())
        for row in data6:  
            if row :        #튜터마이페이지 > 출결현황(결석)
                dic={'fail':row[0]}
                datalist.append(dic)
        for row in data6:
            data6=row[0]
        DATA={'attendance':datalist}
        i=json.dumps(DATA)
        loaded_i=json.loads(i)
        

        #튜터>출결현황그래프>총인원
        query = "SELECT COUNT(CLASS_ID) FROM TUTEE_CLASS_MAPPING,ATTENDANCE WHERE TUTEE_CLASS_MAPPING.CLASS_ID=%s AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND ATTENDANCE.DATE=%s;"
        value=(class_id,data8)
        cursor.execute(query,value)
        data7=(cursor.fetchall())
        for row in data7:  
            if row :        #튜터마이페이지 > 출결현황(총인원)
                dic={'all':row[0]}
                datalist.append(dic)
        for row in data7:
            data7=row[0]
        DATA={'attendance':datalist}
        i=json.dumps(DATA)
        loaded_i=json.loads(i)
            

        #출석, 지각, 결석 퍼센트 쿼리문
        query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING WHERE TUTEE_CLASS_MAPPING.CLASS_ID=%s AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND ATTENDANCE.DATE=%s AND ATTENDANCE.STATUS='pass';"
        value=(class_id,data8)
        cursor.execute(query,value)
        data9=(cursor.fetchall())
        percent=(cursor.fetchall())
        for row in percent:   #출석 퍼센트
            percent=row[0]
        percent=round((float)((data4/data7)*100),2)
        for row in data9:  
            if row :        #튜터마이페이지 > 출결현황(출석퍼센트)
                dic={'pass%':percent}
                datalist.append(dic)
        DATA={'my_graph':datalist}
        i=json.dumps(DATA)
        loaded_i=json.loads(i)


        query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING WHERE TUTEE_CLASS_MAPPING.CLASS_ID=%s AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND ATTENDANCE.DATE=%s AND ATTENDANCE.STATUS='late';"
        value=(class_id,data8)
        cursor.execute(query,value)
        data10=(cursor.fetchall())
        percent2=(cursor.fetchall())
        for row in percent2:  #지각 퍼센트
          percent2=row[0]
        percent2=round((float)((data5/data7)*100),2)
        for row in data10:  
            if row :        #튜터마이페이지 > 출결현황(지각퍼센트)
                dic={'late%':percent2}
                datalist.append(dic)
        DATA={'my_graph':datalist}
        i=json.dumps(DATA)
        loaded_i=json.loads(i)

        query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING WHERE TUTEE_CLASS_MAPPING.CLASS_ID=%s AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND ATTENDANCE.DATE=%s AND ATTENDANCE.STATUS='fail';"
        value=(class_id,data8)
        cursor.execute(query,value)
        data11=(cursor.fetchall())
        percent3=(cursor.fetchall())
        for row in percent3:  #결석 퍼센트
            percent3=row[0]
        percent3=round((float)((data6/data7)*100),2)
        for row in data11:
            if row :        #튜터마이페이지 > 출결현황(결석퍼센트)
                dic={'fail%':percent3}
                datalist.append(dic)
        DATA={'my_graph':datalist}
        i = json.dumps(DATA)
        loaded_i = json.loads(i)
        

        query = "SELECT COUNT(STATUS) FROM ATTENDANCE,TUTEE_CLASS_MAPPING WHERE TUTEE_CLASS_MAPPING.CLASS_ID=%s AND TUTEE_CLASS_MAPPING.MAPPING_ID=ATTENDANCE.MAPPING_ID AND ATTENDANCE.DATE=%s;"
        value=(class_id,data8)
        cursor.execute(query,value)
        data13=(cursor.fetchall())
        percent4=(cursor.fetchall())
        for row in percent4:
            percent4=row[0]
        percent4=round((float)((data4+data5+data6)/data7)*100,2)
        for row in data13:
            if row :        #튜터마이페이지 > 출결현황(총인원퍼센트)
                dic={'all%':percent4}
                datalist.append(dic)
        DATA={'my_graph':datalist}
        i = json.dumps(DATA)
        loaded_i = json.loads(i)
        cursor.close()
        db.close()
        return loaded_i


@app.route("/tutorLgraphProcess",methods=["POST","GET"])
#_튜터>평균그래프(각 인원수)
def tutorLgraphProcess():
    db = pymysql.connect(host='127.0.0.1',
        port=3306,
        user='admin',
        passwd='0507',
        db='attendance',
        charset='utf8')
    cursor=db.cursor()

    class_id=request.args.get("class_id")
    tutee_id=request.args.get("tutee_id")


    #튜터>출결현황그래프>날짜(최신,달력)
    query = "SELECT max(DATE) FROM ATTENDANCE WHERE DATE IN (SELECT max(DATE) FROM ATTENDANCE)"
    cursor.execute(query)
    data8=(cursor.fetchall())

    #튜터>평균그래프
    query = "SELECT CLASS_INFO.CLASS_TIME,ATTENDANCE.PASS_TIME FROM ATTENDANCE,CLASS_INFO,TUTEE_CLASS_MAPPING WHERE CLASS_INFO.CLASS_ID=TUTEE_CLASS_MAPPING.CLASS_ID AND ATTENDANCE.MAPPING_ID=TUTEE_CLASS_MAPPING.MAPPING_ID AND ATTENDANCE.DATE=%s AND TUTEE_CLASS_MAPPING.TUTEE_ID=%s AND CLASS_INFO.CLASS_ID=%s"
    value=(data8,tutee_id,class_id)
    cursor.execute(query,value)
    data12=(cursor.fetchall())
    datalist=[]
    class_time_list = []
    pass_time_list = []
    for row in data12:
        if row :
            class_time_list = row[0].split(',')
            pass_time_list = row[1].split(',')
    dic ={'class_time':class_time_list,'pass_time':pass_time_list}
    datalist.append(dic)
    
    DATA={'student_graph':datalist}
    i = json.dumps(DATA)
    loaded_i=json.loads(i)
    cursor.close()
    db.close()
    return loaded_i

@app.route("/login")
@app.route("/login/<error>")
def login(error=None):
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        return render_template("login.html",error=error)

@app.route("/loginProcess", methods=["POST"])
def loginProcess():
    if request.method=="POST":
        if request.form.get('email', None) == None:
            error={"error":"Fill in the blanks"}
            r=json.dumps(error)
            loaded_r=json.loads(r)
            return redirect(url_for('login', error=loaded_r))
        elif request.form.get('password', None) == None:
            error={"error":"Fill in the blanks"}
            r=json.dumps(error)
            loaded_r=json.loads(r)
            return redirect(url_for('login', error=loaded_r))
        elif request.form.get('user', None) == None:
            error={"error":"Fill in the blanks"}
            r=json.dumps(error)
            loaded_r=json.loads(r)
            return redirect(url_for('login', error=loaded_r))
        else:
            email=request.form["email"]
            pw=request.form["password"]
            #pw=pw.encode()
            #hash_pw=hashlib.sha256(pw).hexdigest()
            user=request.form['user']

            if user=='tutee':
                db=pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='0507', db='attendance', charset='utf8')
                cursor=db.cursor()

                query="SELECT NAME FROM TUTEE_INFO WHERE EMAIL=%s AND PASSWORD =%s;"
                value=(email, pw)
            
                cursor.execute(query, value)
                data=(cursor.fetchall())
            
                cursor.close()
                db.close()
                
                for row in data:
                    data=row[0]
                
                if data:
                    session['username']=request.form['email']
                    return redirect(url_for('sessionCheck'))
                else:
                    error={"error":"You have entered a wrong email or password"}
                    r = json.dumps(error)
                    loaded_r = json.loads(r)
                    return redirect(url_for('login',error=loaded_r))

            elif user=='tutor':
                db=pymysql.connect(host='127.0.0.1', port=3306, user='admin', password='0507', db='attendance', charset='utf8')
                cursor=db.cursor()
    
                query="SELECT NAME FROM TUTOR_INFO WHERE EMAIL=%s AND PASSWORD =%s;"
                value=(email, pw)

                cursor.execute(query, value)
                data=(cursor.fetchall())

                cursor.close()
                db.close()

                for row in data:
                    data=row[0]

                if data:
                    session['username']=request.form['email']
                    return redirect(url_for('sessionCheck'))
                else:
                    error={"error":"You have entered a wrong email or password"}
                    r = json.dumps(error)
                    loaded_r = json.loads(r)
                    return redirect(url_for('login',error=loaded_r))

@app.route("/sessionCheck")
def sessionCheck():
    if 'username' in session:
        return redirect(url_for('index'))

    else:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect(url_for('index'))

