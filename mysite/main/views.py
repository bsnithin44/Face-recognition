from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
# from fbprophet import Prophet
import pandas as pd
import json


import pandas as pd
from pandas.io.json import json_normalize
import os,requests,json

subscription_key = '0b138b19f25a45379d64a4739b16aaf7'

face_api_url = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0/detect'

image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg'

headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
    
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}



def Facerecognition():
    response = requests.post(face_api_url,params=params, headers=headers, json={"url": image_url})
    return response.json()


def homepage(request):
    return render(request,'main/home.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created :{username}")
            login(request,user)
            messages.info(request,f"{username} successfully logged in")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request,f"{msg}:{form.error_messages[msg]}")
                
    form = UserCreationForm
    return render(request,
                 "main/register.html",
                 context = {"form":form})


def logout_request(request):
    logout(request)
    messages.info(request,"logged out succesfully")
    return redirect("main:homepage")



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not  None:
                login(request,user)
                messages.info(request,f"You are now logged in as {username} ")
                return redirect("main:homepage")
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
            
    form = AuthenticationForm()
    return render(request,
                "main/login.html",
                {"form":form})
        
def upload(request):
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        type_ = request.POST.get('type')
        if uploaded_file is not None:
            fs = FileSystemStorage()
            fs.save(uploaded_file.name,uploaded_file)
            messages.info(request,"The file is uploaded successfully")
            # with open(f"http://127.0.0.1:8000/media/{uploaded_file.name}",'rb') as f:
            #     image_data = f.read()
            request.session['image_data'] = 0
            return redirect("main:homepage")
        else:
            messages.error(request,'The file could not be uploaded')
    else:
        pass
    return render(request,'main/upload.html')




def fit_data(request):

    image_data = request.session['image_data']

    response = requests.post(face_api_url,params=params, headers=headers, json={"url": image_url})
    data = response.json()
    face_id = data[0]['faceId']

    return render(request,'main/fit.html', 
            {
                'face_id': face_id ,


            } 
                )            
