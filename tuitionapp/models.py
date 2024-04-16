from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.

class CustomUser(AbstractUser):
    user_type=models.CharField(max_length=10,default=1)
    status=models.BooleanField(default=False)

class Course(models.Model):
    coursename=models.CharField(max_length=255)
    duration=models.CharField(max_length=255)
    syllabus=models.FileField(upload_to='syllabus_pdfs/')
    fee=models.IntegerField()
    
class Usermember(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name='teacher_student_assignment')
    age=models.IntegerField()
    contact=models.CharField(max_length=255)
    image=models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    current_teacher=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,related_name='teacher_assignment')
    

class TeacherAttendance(models.Model):
    teacher_name=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    date=models.DateField()
    attendance=models.CharField(max_length=20)

class StudentAttendance(models.Model):
    student_name=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    date=models.DateField()
    attendance=models.CharField(max_length=20)

class Task(models.Model):
    task_name=models.CharField(max_length=255)
    start_date=models.DateField()
    end_date=models.DateField()
    teacher = models.ForeignKey(Usermember, on_delete=models.CASCADE, null=True)

class Tasksubmission(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,null=True)
    task_upload=models.FileField(upload_to='task_pdfs/')
    description=models.CharField(max_length=255,null=True, blank=True)
    student= models.ForeignKey(Usermember, on_delete=models.CASCADE)



