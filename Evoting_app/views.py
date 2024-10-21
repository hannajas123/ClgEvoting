import datetime
import json

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect





# Create your views here.
#Login
from Evoting_app.models import *











def Login(request):
    return render(request,'Login.html')
def Login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    if login_tab.objects.filter(username=username,password=password).exists():

         res=login_tab.objects.get(username=username,password=password)
         request.session['lid']=res.id
         if res.type=='Admin':
            return redirect('/Evoting/AdminHome/')
         elif res.type=='Subadmin':
            return redirect('/Evoting/Subadmin_home/')
         elif res.type=='Electioncoordinator':
            return redirect('/Evoting/electn_home/')

         else:
           return HttpResponse('''<script>alert('invalid password or username');window.location='/Evoting/Login/'</script>''')
    else:
       return HttpResponse('''<script>alert('invalid password or username');window.location='/Evoting/Login/'</script>''')


def logout(request):
    request.session['lid'] = ''
    return redirect('/Evoting/Login/')
def forget_password(request):
    return render(request,'forgetpassword.html')

def forget_password_post(request):
    em = request.POST['em_add']
    import random
    password = random.randint(00000000, 99999999)
    log = login_tab.objects.filter(username=em)
    if log.exists():
        logg = login_tab.objects.get(username=em)
        message = 'temporary password is ' + str(password)
        send_mail(
            'temp password',
            message,
            settings.EMAIL_HOST_USER,
            [em, ],
            fail_silently=False
        )
        logg.password = password
        logg.save()
        return HttpResponse('<script>alert("success");window.location="/Evoting/Login/"</script>')
    else:
        return HttpResponse('<script>alert("invalid email");window.location="/Evoting/Login/"</script>')

#Admin
def AdminHome(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')

    return render(request,'AdminHome2.html')

def changepassword(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    res=login_tab.objects.get(id=request.session['lid'])
    return render(request,'Admin/Change_pasword.html',{'data':res})
def Change_pwd_post(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    pass1=request.POST["frstpwd"]
    pass2=request.POST["currentpswd"]
    obj=login_tab.objects.get(id=request.session['lid'])
    print(pass1)
    print(obj.password)
    if obj.password==pass2:
     obj.password=pass1
     obj.save()
     return HttpResponse("<script>alert('You changed password');window.location='/Evoting/Login/'</script>")
    else:
        return HttpResponse("<script>alert('You cannot change password');window.location='/Evoting/changepassword/'</script>")


def Add_department(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    return render(request,'Admin/Add_Department.html')
def AddDep_post(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    dname=request.POST["depname"]
    ob=department_tab()
    ob.departmentname=dname
    ob.save()
    return HttpResponse("<script>alert('You Added New department');window.location='/Evoting/Add_Department/'</script>")

def View_department(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    res = department_tab.objects.all()
    return render(request,'Admin/View_dep_nd_mange.html',{'data':res})
def depSearch(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    search=request.POST["s1"]
    res = department_tab.objects.filter(departmentname__icontains=search)
    return render(request,'Admin/View_dep_nd_mange.html',{'data':res})
def delete_Dep(request,pk):
    obj=department_tab.objects.get(id=pk).delete()
    return redirect('/Evoting/View_Department/')
def edit_Dep(request,pk):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    ob=department_tab.objects.get(id=pk)
    return render(request,'Admin/Edit_Department.html',{'data':ob})
def Edit_dep_post(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    dep=request.POST["depname"]
    did=request.POST["id1"]
    ob=department_tab.objects.get(id=did)
    ob.departmentname=dep
    ob.save()
    return HttpResponse("<script>alert('You updated Department');window.location='/Evoting/View_Department/'</script>")

def Add_course(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    res=department_tab.objects.all()
    return render(request,'Admin/Add_Course.html',{'data':res})
def Add_course_post(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    coname=request.POST["cname"]
    dep=request.POST["department"]
    sem=request.POST["sem"]
    ob=course_tab()
    ob.coursename=coname
    ob.Department=department_tab.objects.get(id=dep)
    ob.totalsem=sem
    ob.save()
    return HttpResponse("<script>alert('You Added New Course');window.location='/Evoting/Add_course/'</script>")

def View_course(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    res=course_tab.objects.all()
    return render(request,'Admin/View_Course.html',{'data':res})
def coSearch(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    search=request.POST["s1"]
    res = course_tab.objects.filter(coursename__icontains=search)
    return render(request,'Admin/View_Course.html',{'data':res})
def delete_course(request,pk):
    obj=course_tab.objects.get(id=pk).delete()
    return redirect('/Evoting/View_course/')
def edit_course(request,pk):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    res=department_tab.objects.all()
    ob=course_tab.objects.get(id=pk)
    return render(request,'Admin/Edit_Course.html',{'x':ob,'data':res})
def Edit_course_post(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    coname=request.POST["cname"]
    dep=request.POST["department"]
    sem=request.POST["sem"]
    did=request.POST["id1"]
    ob=course_tab.objects.get(id=did)
    ob.coursename=coname
    ob.Department=department_tab.objects.get(id=dep)
    ob.totalsem=sem
    ob.save()
    return HttpResponse("<script>alert('You updated Course');window.location='/Evoting/View_course/'</script>")
def Add_subAdmin(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    return render(request,'Admin/Add_Subadmin.html')
def Add_Subadmin_post(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    subAdmn=request.POST["subadminname"]
    mail=request.POST["email"]
    phone=request.POST["phoneno"]
    img=request.FILES["img"]
    fs = FileSystemStorage()
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
    fn = fs.save(date, img)
    oo=login_tab()
    oo.username=mail
    oo.password=phone
    oo.type='Subadmin'
    oo.save()
    ob=subadmin_tab()
    ob.subadminname=subAdmn
    ob.email=mail
    ob.phoneno=phone
    ob.LOGIN_id=oo.id
    ob.photo=fs.url(date)
    ob.save()
    return HttpResponse("<script>alert('You Added New Subadmin');window.location='/Evoting/Add_subAdmin/'</script>")

def View_Subadmin(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    res=subadmin_tab.objects.all()
    return render(request,'Admin/View_subadmin.html',{'data':res})
def searchsub(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    search=request.POST["s1"]
    res = subadmin_tab.objects.filter(subadminname__icontains=search)
    return render(request,'Admin/View_subadmin.html',{'data':res})
def delete_subadmin(request,pk):
    obj = subadmin_tab.objects.get(id=pk).delete()
    return redirect('/Evoting/View_subadmin/')
def edit_subAdmin(request,pk):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    ob=subadmin_tab.objects.get(id=pk)
    return render(request,'Admin/Edit_subAdmin.html',{'data':ob})
def update_Subadmin(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    subAdmn = request.POST["subadminname"]
    mail = request.POST["email"]
    phone = request.POST["phoneno"]
    img = request.FILES["img"]
    did = request.POST["id1"]
    fs = FileSystemStorage()
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
    fn = fs.save(date, img)
    ob = subadmin_tab.objects.get(id=did)
    ob.subadminname=subAdmn
    ob.email=mail
    ob.phoneno=phone
    ob.photo=fs.url(date)
    ob.save()
    return HttpResponse("<script>alert('You Added Updated Subadmin');window.location='/Evoting/View_subadmin/'</script>")
def Add_election(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    return render(request,'Admin/Add_Election.html')
def Add_election_post(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    elename = request.POST["electionname"]
    elededate = request.POST["electiondeclareddate"]
    eledate = request.POST["electiondate"]
    # status=request.POST["status"]
    ob = election_tab()
    ob.electionname = elename
    ob.electiondeclareddate =elededate
    ob.electiondate = eledate
    ob.status='pending'
    ob.save()
    return HttpResponse("<script>alert('You Added New Election');window.location='/Evoting/Add_Election/'</script>")
def View_Election(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    res=election_tab.objects.all()
    return render(request,'Admin/View_Election.html',{'data':res})
def searchelec(request):
    if request.session['lid'] == '':
        return redirect('/Evoting/Login/')
    search=request.POST["s1"]
    res = election_tab.objects.filter(electionname__icontains=search)
    return render(request,'Admin/View_Election.html',{'data':res})
def delete_election(request,pk):
    obj = election_tab.objects.get(id=pk).delete()
    return redirect('/Evoting/View_Election/')
def edit_election(request,pk):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    ob=election_tab.objects.get(id=pk)
    return render(request,'Admin/Edit_Election.html',{'data':ob})
def update_election(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    elename = request.POST["electionname"]
    elededate = request.POST["electiondeclareddate"]
    eledate = request.POST["electiondate"]
    did = request.POST["id1"]
    ob=election_tab.objects.get(id=did)
    ob.electionname = elename
    ob.electiondeclareddate = elededate
    ob.electiondate = eledate
    ob.status = 'pending'
    ob.save()
    return HttpResponse("<script>alert('You updated election');window.location='/Evoting/View_Election/'</script>")
def AssignCood(request,pk):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=election_tab.objects.get(id=pk)
    oo=staff_tab.objects.all()
    return render(request,'Admin/Assign_election_coordinator.html',{'i':res,'data':oo})
def AssignCoord_post_(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    staff=request.POST["staff"]
    elename=request.POST["elename"]
    print(staff)

    lobj=login_tab.objects.filter(id=staff).update(type='Electioncoordinator')
    sobj=staff_tab.objects.get(LOGIN_id=staff)
    ob=electioncoordinator_tab()
    ob.STAFF=staff_tab.objects.get(id=sobj.id)
    ob.STAFF=sobj
    ob.ELECTION=election_tab.objects.get(id=elename)
    ob.save()
    return HttpResponse("<script>alert('You Assigned a Electioncoordinator');window.location='/Evoting/View_Election/'</script>")
def View_Staff(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res = staff_tab.objects.all()
    return render(request, 'Admin/View_Staff.html',{'data': res})
def searchstaff(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = staff_tab.objects.filter(staffname__icontains=search)
    return render(request,'Admin/View_Staff.html',{'data':res})
def View_result(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res = election_tab.objects.all()
    return render(request, 'Admin/View_result.html', {'data': res})
def View_voting_result(request,did):

    res=nominees_tab.objects.filter(ELECTION_id=did,status='Verified')
    from web3 import Web3, HTTPProvider
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'D:\\project\\build\\contracts\\Evoting.json'
    deployed_contract_address = web3.eth.accounts[5]


    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    lq=[]
    for i in range(blocknumber,4, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])

            print("ku")
            print(decoded_input[1])
            lq.append(str(decoded_input[1]['candida']))
        except Exception as a:
            pass
    print(lq,"======")

    finalresult=[]

    for i in res:
        cnt=0
        for j in lq:

            if str(i.id)==  j:
                cnt=cnt+1

        finalresult.append({'name': i.STUDENT.name, 'vote': cnt})



    print(finalresult)
    return render(request,'Admin/View_voting_result.html',{ 'data': finalresult})



def checkalreadyvoted(electionid,lid):

    from web3 import Web3, HTTPProvider
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'D:\\project\\build\\contracts\\Evoting.json'
    deployed_contract_address = web3.eth.accounts[5]


    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    voteelectionid=[]

    cnt=0


    for i in range(blocknumber,4, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        decoded_input = contract.decode_function_input(a['input'])

        print("ku")
        print(decoded_input[1])

        cid=str(decoded_input[1]['candida'])
        ulida=str(decoded_input[1]['ulida'])

        if lid== ulida:
            voteelectionid.append(str(nominees_tab.objects.get(id= cid).ELECTION_id))



    if electionid in voteelectionid:
        return "ok"

    else:
        return "no"






def searchresult(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = election_tab.objects.filter(electionname__icontains=search)
    return render(request,'Admin/View_result.html',{'data':res})
def View_Complaint(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res = complaint_tab.objects.all()
    return render(request, 'Admin/View_Complaintand_send rply.html', {'data': res})
def searchcomp(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    fromi=request.POST["s1"]
    to=request.POST["s2"]
    res = complaint_tab.objects.filter(date__gte=fromi,date__lte=to)
    return render(request,'Admin/View_Complaintand_send rply.html',{'data':res})
def Reply(request,did):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=complaint_tab.objects.get(id=did)
    return render(request,'Admin/Rply_complaint.html',{'data':res})
def Reply_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    reply=request.POST["reply"]
    did=request.POST["id1"]
    obj=complaint_tab.objects.get(id=did)
    obj.reply=reply
    obj.status='Replyed'
    obj.save()
    return HttpResponse("<script>alert('You Replyed succesfully');window.location='/Evoting/Add_course/'</script>")
def View_student(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=student_tab.objects.all()
    return render(request,'Admin/View_Student.html',{'data':res})
def searchstudent(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = student_tab.objects.filter(name__icontains=search)
    return render(request,'Admin/View_Student.html',{'data':res})

#Subadmin
def SubAdm_Home(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    return render(request,'SubadminHome2.html')
def changepasswordsubadmn(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=login_tab.objects.get(id=request.session['lid'])
    return render(request,'Subadmin/Change_pasword.html',{'data':res})
def Change_pwd_postsubadmn(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    pass1=request.POST["frstpwd"]
    pass2=request.POST["currentpswd"]
    obj=login_tab.objects.get(id=request.session['lid'])
    print(pass1)
    print(obj.password)
    if obj.password==pass2:
     obj.password=pass1
     obj.save()
     return HttpResponse("<script>alert('You changed password');window.location='/Evoting/Subadmin_home/'</script>")
    else:
        return HttpResponse("<script>alert('You cannot change password');window.location='/Evoting/Subadmin_home/'</script>")

def View_profile(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=subadmin_tab.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Subadmin/View_profile.html',{'data':res})
def Add_student(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=course_tab.objects.all()
    return render(request,'Subadmin/Add_student.html',{'data':res})
def Add_student_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    stuname = request.POST["sname"]
    gender = request.POST["gender"]
    dob = request.POST["dob"]
    img = request.FILES["photo"]
    hname = request.POST["hname"]
    place = request.POST["place"]
    city = request.POST["city"]
    state = request.POST["state"]
    mail = request.POST["email"]
    phn = request.POST["phone"]
    course = request.POST["course"]
    fs = FileSystemStorage()
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
    fn = fs.save(date, img)
    oo = login_tab()
    oo.username = mail
    oo.password = phn
    oo.type ='Student'
    oo.save()
    ob = student_tab()
    ob.name = stuname
    ob.gender = gender
    ob.dob = dob
    ob.photo = fs.url(date)
    ob.housename = hname
    ob.place = place
    ob.city = city
    ob.state = state
    ob.email = mail
    ob.phone = phn
    ob.COURSE = course_tab.objects.get(id=course)
    ob.semster=course_tab.objects.get(id=course)
    ob.LOGIN_id=oo.id
    ob.save()
    return HttpResponse("<script>alert('You Added New Student');window.location='/Evoting/Add_Student/'</script>")
def View_student_s(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=student_tab.objects.all()
    return render(request,'Subadmin/View_student.html',{'data':res})
def searchstudent_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = student_tab.objects.filter(name=search)
    return render(request,'Subadmin/View_Student.html',{'data':res})
def Edit_student(request,pk):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    ob=student_tab.objects.get(id=pk)
    res=course_tab.objects.all()
    return render(request,'Subadmin/Edit_student.html',{'data':ob,'data1':res})
def Update_student(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    stuname = request.POST["sname"]
    gender = request.POST["gender"]
    dob = request.POST["date"]
    hname = request.POST["hname"]
    place = request.POST["place"]
    city = request.POST["city"]
    state = request.POST["state"]
    mail = request.POST["email"]
    phn = request.POST["phone"]
    course = request.POST["course"]
    did=request.POST["id1"]
    if 'photo' in request.FILES:
        img = request.FILES['photo']

        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
        fs = FileSystemStorage()
        path = fs.url(date)
        fn = fs.save(date, img)
        ob = student_tab.objects.get(id=did)
        ob.name = stuname
        ob.gender = gender
        ob.dob = dob
        ob.photo =path
        ob.housename = hname
        ob.place = place
        ob.city = city
        ob.state = state
        ob.email = mail
        ob.phone = phn
        ob.COURSE_id = course
        ob.save()
        return HttpResponse("<script>alert('You updated student');window.location='/Evoting/View_students/'</script>")
    else:
        ob = student_tab.objects.get(id=did)
        ob.name = stuname
        ob.gender = gender
        ob.dob = dob
        ob.housename = hname
        ob.place = place
        ob.city = city
        ob.state = state
        ob.email = mail
        ob.phone = phn
        ob.COURSE_id =course
        ob.save()
        return HttpResponse("<script>alert('You updated student');window.location='/Evoting/View_students/'</script>")

def delete_Students(request,pk):
    obj = student_tab.objects.get(id=pk).delete()
    return redirect('/Evoting/View_students/')
def Add_staff(request):
     if request.session['lid'] == '':
         return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
     res=department_tab.objects.all()
     return render(request, 'Subadmin/Add_staff.html',{'data':res})
def Addstaff_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    sname=request.POST["staffname"]
    gender=request.POST["gender"]
    dob=request.POST["dob"]
    img=request.FILES["photo"]
    hname=request.POST["hname"]
    place=request.POST["place"]
    city=request.POST["city"]
    state=request.POST["state"]
    mail=request.POST["email"]
    phn=request.POST["phone"]
    dep=request.POST["department"]
    fs = FileSystemStorage()
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
    fn = fs.save(date, img)
    oo = login_tab()
    oo.username = mail
    oo.password = phn
    oo.type = 'Staff'
    oo.save()
    ob=staff_tab()
    ob.staffname=sname
    ob.gender=gender
    ob.dob=dob
    ob.photo=fs.url(date)
    ob.housename=hname
    ob.place=place
    ob.city=city
    ob.state=state
    ob.email=mail
    ob.phone=phn
    ob.LOGIN_id=oo.id
    ob.DEPARTMENT=department_tab.objects.get(id=dep)
    ob.save()
    return HttpResponse("<script>alert('You Added New Staff');window.location='/Evoting/Add_Staff/'</script>")
def View_Staffs(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res = staff_tab.objects.all()
    return render(request, 'Subadmin/View_staff.html',{'data': res})
def searchstaff_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = staff_tab.objects.filter(staffname__icontains=search)
    return render(request,'Subadmin/View_Staff.html',{'data':res})
def delete_staff(request,pk):
    obj = staff_tab.objects.get(id=pk).delete()
    return redirect('/Evoting/View_staffs/')
def edit_staff(request,pk):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    oo=department_tab.objects.all()
    res=staff_tab.objects.get(id=pk)
    return render(request,'Subadmin/Edit_staff.html',{'data':res,'data1':oo})
def update_staff_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    sname=request.POST["staffname"]
    gender=request.POST["gender"]
    dob=request.POST["dob"]
    hname=request.POST["hname"]
    place=request.POST["place"]
    city=request.POST["city"]
    state=request.POST["state"]
    mail=request.POST["email"]
    phn=request.POST["phone"]
    dep=request.POST["department"]
    did=request.POST["id1"]
    img=request.FILES["photo"]
    if 'photo' in request.FILES:
     date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
     fs = FileSystemStorage()
     path= fs.url(date)
     fn = fs.save(date, img)
     ob = staff_tab.objects.get(id=did)
     ob.photo=path
     ob.name = sname
     ob.gender = gender
     ob.dob = dob
     ob.housename = hname
     ob.place = place
     ob.city = city
     ob.state = state
     ob.email = mail
     ob.phone = phn
     ob.Department = dep
     ob.save()
     return HttpResponse("<script>alert('You updated  Staff');window.location='/Evoting/View_staffs/'</script>")
    else:
        ob = staff_tab.objects.get(id=did)
        ob.name = sname
        ob.gender = gender
        ob.dob = dob
        ob.housename = hname
        ob.place = place
        ob.city = city
        ob.state = state
        ob.email = mail
        ob.phone = phn
        ob.Department = dep
        ob.save()
    return HttpResponse("<script>alert('You updated  Staff');window.location='/Evoting/View_staffs/'</script>")
def view_eletions(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=election_tab.objects.all()
    return render(request,'Subadmin/View_eletion.html',{'data':res})
def searchelec_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = election_tab.objects.filter(electionname__icontains=search)
    return render(request,'Subadmin/View_eletion.html',{'data':res})
def View_resultsele(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res = election_tab.objects.all()
    return render(request, 'Subadmin/View_result.html', {'data': res})
def View_voting_result_Subadmin(request,did):

    res=nominees_tab.objects.filter(ELECTION_id=did,status='Verified')
    from web3 import Web3, HTTPProvider
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'D:\\project\\build\\contracts\\Evoting.json'
    deployed_contract_address = web3.eth.accounts[5]


    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    lq=[]
    for i in range(blocknumber,4, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])

            print("ku")
            print(decoded_input[1])
            lq.append(str(decoded_input[1]['candida']))
        except Exception as a:
            pass
    print(lq,"======")

    finalresult=[]

    for i in res:
        cnt=0
        for j in lq:

            if str(i.id)==  j:
                cnt=cnt+1

        finalresult.append({'name': i.STUDENT.name, 'vote': cnt})



    print(finalresult)
    return render(request,'Subadmin/View_voting_result_Subadmin.html',{ 'data': finalresult})
def searchresult_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = election_tab.objects.filter(electionname__icontains=search)
    return render(request,'Subadmin/View_result.html',{'data':res})
def View_electioncoordinator(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=electioncoordinator_tab.objects.all()
    return render(request,'Subadmin/View_election_coordinator.html',{'data':res})
def searchelecoode_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = electioncoordinator_tab.objects.filter(ELECTION__electionname__icontains=search)
    return render(request,'Subadmin/View_election_coordinator.html',{'data':res})
def View_nominees(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=nominees_tab.objects.filter(status='Verified')
    return render(request,'Subadmin/View_Nominees.html',{'data':res})
def searchnominee_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = nominees_tab.objects.filter(STUDENT__name__icontains=search)
    return render(request,'Subadmin/View_Nominees.html',{'data':res})




#Election coordinator

def EleCoordHome(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    return render(request,'Electioncoodinator_Home2.html')
def changepasswordelecoord(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=login_tab.objects.get(id=request.session['lid'])
    return render(request,'Electioncoordinator/Change_pasword.html',{'data':res})
def Change_pwd_postelecoord(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    pass1=request.POST["frstpwd"]
    pass2=request.POST["currentpswd"]
    obj=login_tab.objects.get(id=request.session['lid'])
    print(pass1)
    print(obj.password)
    if obj.password==pass2:
     obj.password=pass1
     obj.save()
     return HttpResponse("<script>alert('You changed password');window.location='/Evoting/electn_home/'</script>")
    else:
        return HttpResponse("<script>alert('You cannot change password');window.location='/Evoting/changepassword/'</script>")

def searchnominee_verify(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = nominees_tab.objects.filter(STUDENT__name__icontains=search)
    return render(request,'Electioncoordinator/View_nominees_nd_verify.html',{'data':res})

def View_nomine_verify(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=nominees_tab.objects.all()
    return render(request,'Electioncoordinator/View_nominees_nd_verify.html',{'data':res})
def verifynominee(request,pk):
    res=nominees_tab.objects.filter(id=pk).update(status="Verified")
    return HttpResponse("<script>alert('You verified the nominee');window.location='/Evoting/View_nominees_nd_verify/'</script>")

def searchresult_voting(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = nominees_tab.objects.filter(ELECTION__electionname__icontains=search)
    return render(request,'Electioncoordinator/View_voting_result.html',{'data':res})

def view_voting_result(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=nominees_tab.objects.all()
    return render(request,'Electioncoordinator/View_voting_result.html',{'data':res})
def View_voting_result_Elecoord(request,did):

    res=nominees_tab.objects.filter(ELECTION_id=did,status='Verified')
    from web3 import Web3, HTTPProvider
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'D:\\project\\build\\contracts\\Evoting.json'
    deployed_contract_address = web3.eth.accounts[5]


    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    lq=[]
    for i in range(blocknumber,4, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])

            print("ku")
            print(decoded_input[1])
            lq.append(str(decoded_input[1]['candida']))
        except Exception as a:
            pass
    print(lq,"======")

    finalresult=[]

    for i in res:
        cnt=0
        for j in lq:

            if str(i.id)==  j:
                cnt=cnt+1

        finalresult.append({'name': i.STUDENT.name, 'vote': cnt})



    print(finalresult)
    return render(request,'Electioncoordinator/View_voting_result_Elecoord.html',{ 'data': finalresult})
def view_eletions_nd_status(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=election_tab.objects.all()
    return render(request,'Electioncoordinator/View_nd_Update_election_status.html',{'data':res})
def searcheleNdsta(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    search=request.POST["s1"]
    res = election_tab.objects.filter(electionname__icontains=search)
    return render(request,'Electioncoordinator/View_nd_Update_election_status.html',{'data':res})
def update_status(request,pk):
    res=election_tab.objects.filter(id=pk).update(status="Election completed")
    return HttpResponse("<script>alert('You updated status');window.location='/Evoting/View_election_nd_status/'</script>")
def View_profile_elecoord(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>window.location='/Evoting/Login/'</script>''')
    res=electioncoordinator_tab.objects.get(STAFF__LOGIN_id=request.session['lid'])
    return render(request,'Electioncoordinator/View_profile.html',{'data':res})



#student......Flutter.......................................................
def userlogin_post(request):
    username = request.POST['username']
    password = request.POST['password']
    lobj = login_tab.objects.filter(username=username, password=password)
    if lobj.exists():
        lobjj = login_tab.objects.get(username=username, password=password)
        if lobjj.type == 'Student':
            lid = lobjj.id

            return JsonResponse({'status':'ok', 'lid': str(lid)})
        else:
         return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status': 'no'})


def user_Changepassword(request):
    lid=request.POST["lid"]
    cpassword=request.POST["currentpassword"]
    npassword=request.POST["newpassword"]
    if login_tab.objects.filter(id=lid,password=cpassword).exists():

     obj=login_tab.objects.get(id=lid)
     obj.password=npassword
     obj.save()
     return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'no'})

def Send_nominations(request):
    lid=request.POST["lid"]
    from datetime import datetime
    date=datetime.now().date().today()
    eid=request.POST["electionname"]
    status="pending"

    s=nominees_tab.objects.filter(ELECTION_id=eid,STUDENT=student_tab.objects.get(LOGIN_id=lid))
    if  s.exists():
        return JsonResponse({'status': 'exists'})

    else:

        oo=nominees_tab()
        oo.STUDENT=student_tab.objects.get(LOGIN_id=lid)
        oo.submiteddate=date
        oo.ELECTION_id=eid
        oo.status=status
        oo.save()
        return JsonResponse({'status': 'ok'})

def user_complaint_post(request):
    lid = request.POST["lid"]
    from datetime import datetime
    date = datetime.now().date().today()
    complaint = request.POST["complaint"]
    status = "pending"
    reply = 'pending'

    cobj = complaint_tab()
    cobj.date = date
    cobj.complaint = complaint
    cobj.status = status
    cobj.reply = reply
    cobj.USER =student_tab.objects.get(LOGIN_id=lid)
    cobj.save()
    return JsonResponse({'status': 'ok'})


def view_nominees_post(request):
    lid = request.POST['lid']
    sf = nominees_tab.objects.filter(STUDENT__LOGIN_id=lid,status='Verified')
    l = []
    for i in sf:
        l.append({'id': i.id, 'date': i.submiteddate, 'status': i.status, 'electioname': i.ELECTION.electionname, 'electiondeclareddate': i.ELECTION.electiondeclareddate,'electiondate':i.ELECTION.electiondate,'electionstatus':i.ELECTION.status,'nominee':i.STUDENT.name})
    return JsonResponse({'status': 'ok', 'data': l})

def view_result_post(request):
    res = election_tab.objects.all()
    l = []
    for i in res:
        l.append({'id': i.id, 'electionname': i.electionname,'electiondeclareddate':i.electiondeclareddate,'electiondate':i.electiondate,'status':i.status})
    return JsonResponse({'status': 'ok', 'data': l})
def view_election(request):
    res = election_tab.objects.all()
    l = []
    for i in res:
        l.append({'id': i.id, 'electionname': i.electionname,'electiondeclareddate':i.electiondeclareddate,'electiondate':i.electiondate,'status':i.status})
    return  JsonResponse({'status':'ok', 'data':l})
def view_reply(request):
    lid = request.POST['lid']
    sf = complaint_tab.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in sf:
         l.append({'id':i.id,'date': i.date, 'complaint':i.complaint,'status': i.status, 'reply': i.reply})
    return JsonResponse({'status': 'ok', 'data': l})
def view_profile(request):
    lid=request.POST['lid']
    cd=student_tab.objects.get(LOGIN_id=lid)
    return  JsonResponse({'status': 'ok', 'name':cd.name,'gender':cd.gender,'email':cd.email,'phone':cd.phone,'housename':cd.housename,'place':cd.place,'city':cd.city,'state':cd.state,'dob':cd.dob,'photo':cd.photo,'semester':cd.semster,'course':cd.COURSE.coursename})
def View_election_for_nomination(request):
    sf=election_tab.objects.all()
    l=[]
    for i in sf:
        l.append({'id': i.id, 'election_name': i.electionname})

    # print(l)
    return JsonResponse({'status':'ok','data':l})

def electiontoday(request):
    from datetime import datetime
    date = datetime.now().date().today()

    res = election_tab.objects.filter(electiondate=date)
    l = []
    for i in res:
        l.append({'id': i.id, 'electionname': i.electionname,'electiondeclareddate':i.electiondeclareddate,'electiondate':i.electiondate,'status':i.status})
    return  JsonResponse({'status':'ok', 'data':l})
def View_and_vote_for_nominees(request):
    eid=request.POST["eid"]
    res=nominees_tab.objects.filter(ELECTION_id=eid,status='Verified')
    l=[]
    for i in res:
        l.append({'id':i.id,'nominee':i.STUDENT.name,'photo':i.STUDENT.photo})
    return JsonResponse({'status':'ok','data':l})



#############################block chain#########################################
def Add_vote(request):

    import json
    from web3 import Web3, HTTPProvider
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]

    compiled_contract_path = 'D:\\project\\build\\contracts\\Evoting.json'
    deployed_contract_address = web3.eth.accounts[5]

    cand_id=request.POST['candid']
    uid=request.POST['lid']

    s=checkalreadyvoted(electionid=str(nominees_tab.objects.get(id=cand_id).ELECTION_id),lid=uid)

    if s== "ok":

        return JsonResponse({'status': 'exists'})
    else:

        print(cand_id,uid,"=========================================")


        from datetime import datetime
        date=datetime.now().strftime('%Y-%m-%d')
        time=datetime.now().strftime('%H:%M:%S')
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        blocknumber = web3.eth.get_block_number()
        vote=contract.functions.addvote(int(cand_id),int(uid),str(date),str(time)).transact()
        return JsonResponse({'status':'ok'})


def View_votes_Nominees(request):
    did = request.POST["eid"]
    res = nominees_tab.objects.filter(ELECTION_id=did, status='Verified')
    from web3 import Web3, HTTPProvider
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'D:\\project\\build\\contracts\\Evoting.json'
    deployed_contract_address = web3.eth.accounts[5]

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    lq = []
    for i in range(blocknumber, 4, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])

            print("ku")
            print(decoded_input[1])
            lq.append(str(decoded_input[1]['candida']))
        except Exception as a:
            pass
    print(lq, "======")

    finalresult = []

    for i in res:
        cnt = 0
        for j in lq:

            if str(i.id) == j:
                cnt = cnt + 1

        finalresult.append({'name': i.STUDENT.name, 'vote': cnt})

    print(finalresult)
    return JsonResponse({'status':'ok','data': finalresult})
