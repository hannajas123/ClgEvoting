from django.db import models

# Create your models here.
class login_tab(models.Model):
    username=models.CharField(max_length=100,default="")
    password=models.CharField(max_length=30,default="")
    type=models.CharField(max_length=200,default="")


class department_tab(models.Model):
    departmentname=models.CharField(max_length=300,default="")

class course_tab(models.Model):
    Department=models.ForeignKey(department_tab,on_delete=models.CASCADE,default=1)
    coursename=models.CharField(max_length=300,default="")
    totalsem=models.CharField(max_length=10,default="")

class subadmin_tab(models.Model):
    subadminname=models.CharField(max_length=100,default="")
    email=models.CharField(max_length=50,default="")
    phoneno=models.CharField(max_length=10,default="")
    photo=models.FileField(max_length=100,default="")
    LOGIN=models.ForeignKey(login_tab,on_delete=models.CASCADE,default=2)

class staff_tab(models.Model):
    staffname=models.CharField(max_length=100,default="")
    gender=models.CharField(max_length=100,default="")
    dob=models.CharField(max_length=20,default="")
    photo=models.FileField(max_length=100,default="")
    housename=models.CharField(max_length=100,default="")
    place=models.CharField(max_length=100,default="")
    city=models.CharField(max_length=100,default="")
    state=models.CharField(max_length=100,default="")
    email=models.CharField(max_length=100,default="")
    phone=models.CharField(max_length=100,default="")
    DEPARTMENT=models.ForeignKey(department_tab,on_delete=models.CASCADE,default=3)
    LOGIN=models.ForeignKey(login_tab,on_delete=models.CASCADE,default=4)

class election_tab(models.Model):
    electionname=models.CharField(max_length=100,default="")
    electiondeclareddate=models.CharField(max_length=10,default="")
    electiondate=models.CharField(max_length=10,default="")
    status=models.CharField(max_length=100,default="")

class electioncoordinator_tab(models.Model):
    STAFF=models.ForeignKey(staff_tab,on_delete=models.CASCADE,default=5)
    ELECTION=models.ForeignKey(election_tab,on_delete=models.CASCADE,default=6)

class student_tab(models.Model):
    name=models.CharField(max_length=100,default="")
    gender=models.CharField(max_length=100,default="")
    dob=models.CharField(max_length=100,default="")
    photo=models.CharField(max_length=500,default="")
    housename=models.CharField(max_length=100,default="")
    place=models.CharField(max_length=100,default="")
    city=models.CharField(max_length=100,default="")
    state=models.CharField(max_length=100,default="")
    email=models.CharField(max_length=100,default="")
    phone=models.CharField(max_length=100,default="")
    semster=models.CharField(max_length=100,default="")
    COURSE=models.ForeignKey(course_tab,on_delete=models.CASCADE,default=7)
    LOGIN=models.ForeignKey(login_tab,on_delete=models.CASCADE,default=8)


class nominees_tab(models.Model):
    STUDENT=models.ForeignKey(student_tab,on_delete=models.CASCADE,default=9)
    ELECTION=models.ForeignKey(election_tab,on_delete=models.CASCADE,default=10)
    submiteddate=models.CharField(max_length=100,default="")
    status=models.CharField(max_length=100,default="")
class complaint_tab(models.Model):
    USER=models.ForeignKey(student_tab,on_delete=models.CASCADE,default=11)
    complaint=models.CharField(max_length=200,default="")
    date=models.CharField(max_length=10,default="")
    reply=models.CharField(max_length=200,default="")
    status=models.CharField(max_length=50,default="")







