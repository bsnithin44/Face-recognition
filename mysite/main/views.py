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
import cognitive_face as cf

cf.util.requests.ConnectTimeout = 1
subscription_key = '0b138b19f25a45379d64a4739b16aaf7'
base_url = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
cf.Key.set(subscription_key)
cf.BaseUrl.set(base_url)

def homepage(request):
    return render(request,'main/home2.html')

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
        

def process(request):
    try:
        face_detect = cf.face.detect('media/image from button.jpeg') 
        response = cf.face.identify([face_detect[0]['faceId']],person_group_id='group_1')
        print('response recieved')
        r2 = response[0]['candidates']
        print(1)
        if len(r2)>0:
            df_r = json_normalize(r2)
            print(2)
            df_r.sort_values('confidence',ascending=False,inplace=True)
            if df_r['confidence'][0]>0.70:
                print(3)
                # Matched with good accuracy so head to results page and show an image or name of the person
                data_persons = cf.person.lists('group_1')
                df_persons = json_normalize(data_persons)
                detected_personId = df_r['personId'][0]
                detected_confidence = df_r['confidence'][0] 
                name_of_detected_person = df_persons[df_persons['personId']==detected_personId]['name'].values[0]
                messages.success(request,"Detected!")
                return render(request,'main/results.html',
                {
                    'detected_faceId': detected_personId ,
                    'confidence': detected_confidence  ,
                    'name':name_of_detected_person 
                }            
                )
            elif df_r['confidence'][0]>.50 and df_r['confidence'][0]<0.70:
                messages.info(request,"Please try again")
                return render(request,'main/home2.html')
            else:
                # Achived very less accuracy So ask the try again else ask to register
                # Go to Details page
                messages.info(request,'Please register again')
                return render(request,"main/details.html")
        else:
            print('1b')
            return render(request,"main/details.html")
    except Exception as e:
        messages.error(request,e)
        # return render(request,'main/home2.html')
        return redirect('main:homepage')
        #  take details and train
            

#################################################################
#            Code Under Test



def details(request):
    if request.method == "POST":
        name_of_person = request.POST.get('name')
        if len(cf.person_group.lists()) == 0:
            cf.person_group.create('group_1','all')
            new_person = cf.person.create('group_1',name_of_person)
            cf.person.add_face('media/image from button.jpeg','group_1',new_person['personId'])   
        else:
            data_persons = cf.person.lists('group_1')  
            df_persons = json_normalize(data_persons)
            if name_of_person in df_persons['name'].values:
                id_of_person = df_persons[df_persons['name']==name_of_person]['personId'].values[0]
                cf.person.add_face('media/image from button.jpeg','group_1',id_of_person)
            else:
                new_person = cf.person.create('group_1',name_of_person)
                cf.person.add_face('media/image from button.jpeg','group_1',new_person['personId'])
        cf.person_group.train('group_1')

        return redirect("main:homepage")
    else:
        pass
    return render(request,"main/details.html")





def process_old(request):
    if len(cf.person_group.lists()) == 0:
        cf.person_group.create(person_group_id='group_1',name='all')
    else:
        face_detect = cf.face.detect('media/image from button.jpeg')
        try:
            response = cf.face.identify([face_detect[0]['faceId']],person_group_id='group_1')
            print('responasdasdasdasdnasna-------------------------------')
            if len(response) >0:
                r2 = response[0]['candidates']
                df_r = json_normalize(r2)
                df_r.sort_values('confidence',ascending=False,inplace=True)
                print('got a response')
                return render(request,'main/results.html', 
                        {
                            'detected_faceId': df_r['personId'][0] ,
                            'confidence': df_r['confidence'][0]

                        } 
                            )    
        except Exception as e:
            cf_id = cf.person.create('group_1','nithin')            
            cf.person.add_face('media/image from button.jpeg','group_1',cf_id['personId'])
            cf.person_group.train('group_1')
            print('training done')
            messages.info(request,'New person detected and trained')
            return render(request,'main/home2.html')

def results(request):
    render(request,"main/results.html")

def image(request):
    print('here')
    camera = cv2.VideoCapture(0)
    return_value,image = camera.read()
    cv2.imwrite('media/image from button.jpeg', image)
    del camera

    return render(request,'main/image.html')
#################################################################
#  Old Code TBD

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
        response = requests.post(face_api_url,params=params, headers=headers, data = image_data,timeout=2)
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

