from sys import path
from django.shortcuts import render
from pathlib import Path
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.contrib.auth import authenticate,login,logout
import os


cred=credentials.Certificate(str(Path(__file__).resolve().parent.parent)+'\\fullsite\\'+"ass-jdmr-ischool-firebase-adminsdk-ydg88-16a442ac76.json")
firebase_admin.initialize_app(cred)
db=firestore.client()



def login(request):
    if request.method == 'POST':
        uname=request.POST.get('loginname')
        upass=request.POST.get('loginpass')
        user=authenticate(username=uname,password=upass)
        if user is not None:
            login(user)
            collection = db.collection('chatRoom')
            collection.document(uname).set({"name":uname})
    
            users_ref=collection.document(uname).collection('messages')
            docs = users_ref.stream()

            all_user_docs = db.collection(u'chatRoom').stream()
            temp_list=[]
            for doc in all_user_docs:
                temp_list.append(doc.id)
        
            list_detail=[]
            for doc in docs:
                msg_detail=doc.to_dict()
                list_detail.append({"msg":msg_detail.get('msg'),"username":msg_detail.get('username')})

            return render(request,'fullsite/home.html',{'username':uname,'msg_detail':list_detail,"all_user_docs":temp_list})

        return render(request,'fullsite/login.html')
    
    return render(request,'fullsite/login.html')

# Create your views here.
def home(request):
    return render(request,'fullsite/home.html')

def sendMessage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        msg=request.POST.get('message')
        collection = db.collection('chatRoom')
        try:
            collection.document(uname).collection('messages').document().set({'msg':msg,'username':uname})
        except Exception:
            pass
        users_ref=collection.document(uname).collection('messages')
        docs = users_ref.stream()
        list_detail=[]

        all_user_docs = db.collection(u'chatRoom').stream()
        temp_list=[]
        for doc in all_user_docs:
            temp_list.append(doc.id)
            

        for doc in docs:
            msg_detail=doc.to_dict()
            list_detail.append({"msg":msg_detail.get('msg'),"username":msg_detail.get('username')})
        return render(request,'fullsite/home.html',{'username':uname,'msg_detail':list_detail,"all_user_docs":temp_list})
    
    uname=request.GET.get('personSend')
    collection = db.collection('chatRoom')
    users_ref=collection.document(uname).collection('messages')
    docs = users_ref.stream()
    list_detail=[]

    all_user_docs = db.collection(u'chatRoom').stream()
    temp_list=[]
    for doc in all_user_docs:
        temp_list.append(doc.id)

    for doc in docs:
        msg_detail=doc.to_dict()
        list_detail.append({"msg":msg_detail.get('msg'),"username":msg_detail.get('username')})
    return render(request,'fullsite/home.html',{'username':uname,'msg_detail':list_detail,"all_user_docs":temp_list})


def admin_chat(request):
    if request.method =='POST':
        print("step0")
        personReceive=request.POST.get('personReceive')
        personSend=request.POST.get('personSend')
        msg=request.POST.get('message')
        print("step1",personSend,personReceive,msg)
        collection = db.collection('chatRoom')
        try:
            collection.document(personReceive).collection('messages').document().set({'msg':msg,'username':personSend})
        except Exception:
            pass
        print("step2")
        all_user_docs = db.collection(u'chatRoom').stream()
        temp_list=[]
        for doc in all_user_docs:
            temp_list.append(doc.id)
        print("step3")
        users_ref=collection.document(personReceive).collection('messages')
        docs = users_ref.stream()
        list_detail=[]
        print("step4")
        for doc in docs:
            msg_detail=doc.to_dict()
            list_detail.append({"msg":msg_detail.get('msg'),"username":msg_detail.get('username')})

        print("step5")
        print(list_detail,temp_list)
        return render(request,'fullsite/admin_chat.html',{'username':personSend,'msg_detail':list_detail,"all_user_docs":temp_list})

    personReceive=request.GET.get('personReceive')
    personSend=request.GET.get('personSend')
    print(personReceive,personSend)
    

    all_user_docs = db.collection(u'chatRoom').stream()
    temp_list=[]
    for doc in all_user_docs:
        temp_list.append(doc.id)
    
    collection = db.collection(u'chatRoom')
    users_ref=collection.document(personReceive).collection('messages')
    docs = users_ref.stream()
    list_detail=[]
    for doc in docs:
        msg_detail=doc.to_dict()
        list_detail.append({"msg":msg_detail.get('msg'),"username":msg_detail.get('username')})
    print(list_detail,temp_list)
    return render(request,'fullsite/admin_chat.html',{'username':personSend,"personReceive":personReceive,'msg_detail':list_detail,"all_user_docs":temp_list})