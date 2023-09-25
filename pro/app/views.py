from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from app.models import patient
from datetime import datetime
from django.contrib import messages
import pickle
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from keras.models import load_model
import tensorflow_hub as hub
import numpy as np 
import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from django.shortcuts import render,HttpResponse,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,logout
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login


def signin(request):
    if request.method=='POST':
        username=request.POST['username1']
        password=request.POST['password1']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'contact.html')
        else:
            messages.info(request,'invalid credentials')
            return render(request,'contact.html') 
    else:
        return render(request,'signin.html')
def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        phone=request.POST['phone']
        user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
        if User.objects.filter(username=username).exists():
            messages.info(request,"username taken")
            return render(request,'register.html')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"email taken")
            return render(request,'register.html')
        else:
            user.save()
            print('user created')
            return render(request,'register.html')
    else:
        return render(request,'register.html')

def predict(img,model):
    img1=mpimg.imread(img)
    img1=cv2.resize(img1,(224,224),3)
    img1=np.array(img1)/255.0
    img1[np.newaxis,...].shape
    prediction=model.predict(img1[np.newaxis,...])
    prediction=np.argmax(prediction)
    if (prediction==0):
        res='no dr'
    elif(prediction==1):
        res= 'mild dr'
    elif(prediction==2):
        res= 'moderate dr'
    elif(prediction==3):
        res= 'severe'
    else:
        res= 'proliferate'  
    return res
def contact(request):
    if(request.method=='POST'):
        id= request.POST.get('id')
        name= request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        left=request.FILES.get('left')
        right=request.FILES.get('right')
        model=tf.keras.models.load_model('final.h5', custom_objects={'KerasLayer':hub.KerasLayer})
        res1=predict(left,model)
        res2=predict(right,model)
        fs = FileSystemStorage()
        f1 = fs.save(left.name,left)
        f2 = fs.save(right.name,right)
        f1 = fs.url(left)
        f2 = fs.url(right)
        p=patient(id=id,name=name,email=email,phone=phone,desc=desc,img1=left,img2=right,res1=res1,res2=res2,date=datetime.today())
        p.save()
        print(res1)
        print(res2)
        d={'id':id,'name':name,'email':email,'phone':phone,'desc':desc,'img1':f1,'img2':f2,'res1':res1,'res2':res2,'date':datetime.today(),'ans1':res1,'ans2':res2}
        return render(request,'result.html',d)
    return render(request,'contact.html')

def display(request):
    d=patient.objects.all()
    context={
        "obj":d
    }
    return render(request,"display.html",context)

def delete(request, id):
    p=patient.objects.get(id=id)
    p.delete()
    messages.info(request,"Patient Deleted Successfully!")
    #return render(request, 'ack.html',{'title':'Patient Deleted Successfully!'})
    return redirect("/display")

def search(request):
    if request.method=='POST':
        search=request.POST.get('search_input')
        pat=patient.objects.filter(name=search)
        context = {
            "pat":pat
        }
        return render(request,'search.html',context)

def home(request):
    return render(request,'home.html')

