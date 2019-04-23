from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import cv2,base64,json,time,os,requests
import pandas as pd
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pandas.io.json import json_normalize


subscription_key = '0b138b19f25a45379d64a4739b16aaf7'

face_api_url = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0/detect'


headers = {'Content-Type': 'application/octet-stream', 
           'Ocp-Apim-Subscription-Key': subscription_key}
    
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}


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
        

def capture(request):

    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('media/temp.jpeg', image)
    del(camera)       

    return redirect('main:homepage')



def detect(request):
    with open('media/temp.jpeg','rb') as f:
        image_data  =f.read()
    img = mpimg.imread('media/temp.jpeg')
    print('read')
    i = 0
    while True or i>5:
        response = requests.post(face_api_url,params=params, headers=headers, data = image_data)
        time.sleep(2)
        if response.status_code == 200:
            break
        time.sleep(1)
        i +=1


    ids = []
    emotion_happiness = []
    data = response.json()
    fig,ax = plt.subplots(1)
    for i in range(len(data)):
        ids.append(data[i]['faceId'])
        top = data[i]['faceRectangle']['top']
        left = data[i]['faceRectangle']['left']
        height = data[i]['faceRectangle']['height']
        width = data[i]['faceRectangle']['width']
        emotion_happiness.append(data[i]['faceAttributes']['emotion']['happiness'])
        ax.imshow(img)
        rect = patches.Rectangle((left,top),width,height,linewidth=2,edgecolor='g',facecolor='none')
        ax.add_patch(rect)
    plt.savefig('media/result.jpeg')

    return render(request,'main/detect.html', 
            {
                'emotion_happiness': emotion_happiness ,


            } 
                )            
