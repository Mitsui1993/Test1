from django.shortcuts import render,redirect,HttpResponse
import pymysql
from sqlser import sqlhelper
import json

def classes(request):

    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='wbn123',db='my',charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('select cid,cname from class')
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()

    return render(request,'classes.html',{'class_list':class_list})

def add_class(request):
    # print(request.method)
    if request.method == "GET":
        return render(request,'add_class.html')

    else:
        v = request.POST.get('title')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wbn123', db='my', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('insert into class(cname) VALUES (%s)',[v,])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/classes/')

def del_class(request):
    nid = request.GET.get('nid')

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wbn123', db='my', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('delete from class WHERE cid=%s', [nid, ])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/classes/')

def edit_class(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wbn123', db='my', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('select cid,cname from class WHERE cid=%s', [nid, ])
        res = cursor.fetchone()
        cursor.close()
        conn.close()

        return render(request,'edit_class.html',{'res':res})

    else:
        nid = request.GET.get('nid')
        v = request.POST.get('title')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wbn123', db='my', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('update class set cname=%s WHERE cid=%s', [v,nid, ])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/classes/')

def student(request):

    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='wbn123',db='my',charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select student.sid,student.sname,student.class_id,class.cname from student LEFT JOIN class ON student.class_id=class.cid')
    student_list = cursor.fetchall()
    cursor.close()
    conn.close()
    res = sqlhelper.get_all('select class.cid,class.cname from class',[])

    # print(student_list)
    return render(request,'student.html',{'student_list':student_list,'res':res})


def add_student(request):
    if request.method == 'GET':
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wbn123', db='my', charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('select cid,cname from class ')
        class_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(request,'add_student.html',{'class_list':class_list})

    else:
        name = request.POST.get('name')
        cid = request.POST.get('class_id')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wbn123', db='my', charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('insert into student(sname,class_id) VALUES (%s,%s)',[name,cid,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/student/')

def edit_student(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        class_list = sqlhelper.get_all('select cid,cname from class',[])
        res = sqlhelper.get_one('select sid,sname,class_id from student WHERE class_id=%s',[nid,])

        return render(request,'edit_student.html',{'class_list':class_list,'res':res})


##################对话框####################

def modal_add_class(request):
    title = request.POST.get('title').strip()
    if len(title) > 0 and len(title) <= 20:
        sqlhelper.modify('insert into class(cname) VALUES (%s)',[title,])
        return HttpResponse('ok')
    elif len(title) > 20:
        return HttpResponse('字符超过限制！')
    else:
        return HttpResponse('输入不能为空！')

def modal_edit_class(request):
    cid = int(request.POST.get('cid').strip())
    cname = request.POST.get('cname').strip()
    print(cname,cid)
    if len(cname) > 0 and len(cname) <= 20:
        sqlhelper.modify('update class set cname=%s where cid=%s', [cname,cid, ])
        return HttpResponse('ok')
    elif len(cname) > 20:
        return HttpResponse('字符超过限制！')
    else:
        return HttpResponse('输入不能为空！')

def modal_del_class(request):
    cid = int(request.POST.get('cid').strip())
    sqlhelper.modify('delete from class WHERE cid=%s', [cid,])
    return HttpResponse('ok')

    # ret = {'status': True, 'message': None}
    # try:

#-------------------学生对话框--------------#
def modal_add_student(request):
    class_id = request.POST.get('class_id')
    cname = request.POST.get('cname')

    sqlhelper.modify('insert into student(sname,class_id) VALUES (%s,%s)',[cname,class_id,])
    return HttpResponse('ok')

def modal_edit_student(request):
    ret = {'status':True, 'message': None}
    try:
        class_id = request.POST.get('class_id')
        sname = request.POST.get('sname')
        sid = request.POST.get('sid')
        sqlhelper.modify('update student set sname=%s,class_id=%s WHERE sid=%s',[sname,class_id,sid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def modal_del_student(request):
    ret = {'status': True, 'message': None}
    try:
        sid = request.POST.get('sid')
        sqlhelper.modify('delete from student WHERE sid=%s', [sid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))



# -------老师对话框-------
def teacher(request):
    teacher_list = sqlhelper.get_all('''select teacher.tid,teacher.tname,class.cname from teacher LEFT JOIN guanxi ON
        teacher.tid=guanxi.teacher_id LEFT JOIN class
        on class.cid=guanxi.class_id''',[])
    res = {}
    for row in teacher_list:
        tid = row['tid']
        if tid in res:
            res[tid]['cnames'].append(row['cname'])
        else:
            res[tid] = {'tid':row['tid'],'tname':row['tname'],'cnames':[row['cname'],]}
    obj = sqlhelper.SqlHelper()
    class_list = obj.get_list('select cid,cname from class',[])
    obj.close()

    return render(request,'teacher.html',{'teacher_list':res.values(),'res':class_list})

def add_teacher(request):
    if request.method == 'GET':
        class_list = sqlhelper.get_all('select cid,cname from class',[])
        return render(request,'add_teacher.html',{'class_list':class_list})

    else:
        tname = request.POST.get('name')
        clist = request.POST.getlist('class_id')
        sqlhelper.modify('insert into teacher(tname) VALUES (%s)',[tname,])
        news = sqlhelper.get_one('select max(tid) from teacher',[])
        new_id = int(news['max(tid)'])
        cls_list = []
        for row in clist:
            # sqlhelper.modify('insert into guanxi(class_id,teacher_id) VALUES (%s,%s)',[int(row),new_id])
            temp = (int(row),new_id,)
            cls_list.append(temp)
        obj=sqlhelper.SqlHelper()
        obj.multiple_modify('insert into guanxi(class_id,teacher_id) VALUES (%s,%s)',cls_list)
        obj.close()
        return redirect('/teacher/')

def edit_teacher(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        obj = sqlhelper.SqlHelper()
        teacher_info = obj.get_one('select tid,tname from teacher WHERE tid=%s',[nid,])
        cls_id = obj.get_list('select class_id from guanxi WHERE teacher_id=%s',[nid,])
        class_list = obj.get_list('select cid,cname from class',[])
        obj.close()
        cid = []
        for item in cls_id:
            cid.append(item['class_id'])
        return render(request,'edit_teacher.html',{'teacher_info':teacher_info,'cls_id':cid,'class_list':class_list})

    else:
        nid = request.GET.get('nid')
        tname = request.POST.get('name')
        cid = request.POST.getlist('class_id')
        obj = sqlhelper.SqlHelper()
        obj.modify('update teacher set tname=%s WHERE tid=%s',[tname,nid,])
        obj.modify('delete from guanxi WHERE teacher_id=%s',[nid,])
        cls_id = []
        for item in cid:
            temp = (item,nid)
            cls_id.append(temp)
        obj.multiple_modify('insert into guanxi(class_id,teacher_id) VALUES (%s,%s)',cls_id)

        return redirect('/teacher/')

#-----------对话框老师---------------
def modal_add_teacher(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        cid = request.POST.getlist('cid')
        obj = sqlhelper.SqlHelper()
        tid = obj.create('insert into teacher(tname) VALUES (%s)',[name,])
        cls_list = []
        for i in cid:
            item = (int(i),tid)
            cls_list.append(item)
        obj.multiple_modify('insert into guanxi(class_id,teacher_id) VALUES (%s,%s)',cls_list)
        obj.close()
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def get_all_list(request):
    obj = sqlhelper.SqlHelper()
    class_list = obj.get_list('select cid,cname from class',[])
    obj.close()
    return HttpResponse(json.dumps(class_list))

def get_cid_list(request):
    tid = request.POST.get('tid')
    obj = sqlhelper.SqlHelper()
    class_list = obj.get_list('select cid,cname from class',[])
    cls_id = obj.get_list('select class_id from guanxi WHERE teacher_id=%s',[tid,])
    c_list=[class_list,cls_id]
    return HttpResponse(json.dumps(c_list))

def modal_edit_teacher(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        cid = request.POST.getlist('cid')
        tid = request.POST.get('tid')
        obj = sqlhelper.SqlHelper()
        obj.modify('update teacher set tname=%s WHERE tid=%s',[name,tid,])
        cls_list = []
        for i in cid:
            item = (int(i), tid)
            cls_list.append(item)
        obj.modify('delete from guanxi WHERE teacher_id=%s', [tid, ])
        obj.multiple_modify('insert into guanxi(class_id,teacher_id) VALUES (%s,%s)', cls_list)
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def layout(request):
    tk = request.COOKIES.get('ticket')
    if not tk:
        return redirect('/login/')
    return render(request,'layout.html')

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')

    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        if user == 'alex@qq.com' and pwd == '123':
            obj = render(request,'layout.html')
            obj.set_cookie('ticket','sdfsdfs')
            return obj

        else:
            return render(request,'login.html')

