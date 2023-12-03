from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import airConditioner, consumer
import boto3
import json
from datetime import datetime
import logging, traceback
from sqs_library.sqs_package.sqs_function import send_sqs_message

#adding logger to checjk exception
logger = logging.getLogger(__name__)
# Create your views here.
@csrf_exempt
def login_api(request):
    if request.method == "GET":
        return render(
            request, "login_page.html", context={"message": "Success"}, status=201
        )
    elif request.method == "POST":
        try:
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return render(
                    request,
                    "login_page.html",
                    context={"message": "User not availabe"},
                    status=404,
                )
        except Exception as e:
            return render(
                request, "login_page.html", context={"message": "Error"}, status=501
            )


@csrf_exempt
# def signup_api(request):
#     if request.method == "GET":
#         return render(
#             request, "signup_page.html", context={"message": "Success"}, status=201
#         )
#     elif request.method == "POST":
#         email = request.POST["email"]
#         password = request.POST["password"]
#         cpassword = request.POST["cpassword"]
#         if password != cpassword:
#             return render(
#                 request,
#                 "signup_page.html",
#                 context={"message": "Password mismatch"},
#                 status=401,
#             )
#         user = User.objects.filter(username=email).first()
#         if user:
#             return render(
#                 request,
#                 "signup_page.html",
#                 context={"message": "Account Exists"},
#                 status=401,
#             )
#         try:
#             # Create a new user
#             user = User.objects.create_user(username=email, password=password)
#             new = consumer(id=email)
#             new.save()
#             login(request, user)
#             #Sending data to SQS service         
#             session = boto3.session.Session(region_name='eu-north-1')
#             sqs_client = session.client('sqs')
            
#             user_data = {
#                 'username': email,
#                 'timestamp': str(datetime.now())
#             }
#             # # Convert user_data to JSON form
#             print("Going to send to sqs")
#             message_body = json.dumps(user_data)
#             response = sqs_client.get_queue_url(QueueName='x22217029_cpp')
#             queue_url = response['QueueUrl']
#             print('\n==>message to send to the queue {} ...\n'.format("User has been registered successfully"))
#             response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
#             return redirect("/auth/add_ac/")
#         except Exception as e:
#           #  print (e)
#             logger.error(traceback.format_exc())
                    
#             return render(
#                 request, "signup_page.html", context={"message": "Error"}, status=501
#             )
def signup_api(request):
     if request.method == "GET":
         return render(
             request, "signup_page.html", context={"message": "Success"}, status=201
         )
     elif request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            cpassword = request.POST["cpassword"]
    
            if password != cpassword:
                return render(
                    request,
                    "signup_page.html",
                    context={"message": "Password mismatch"},
                    status=401,
                )
    
            user = User.objects.filter(username=email).first()
            if user:
                return render(
                    request,
                    "signup_page.html",
                    context={"message": "Account Exists"},
                    status=401,
                )
    
            try:
                # Creating new user
                user = User.objects.create_user(username=email, password=password)
                new = consumer(id=email)
                new.save()
    
                # importing sqs package
                if send_sqs_message(email):
                    return redirect("/auth/add_ac/")
                else:
                    return render(
                        request, "signup_page.html", context={"message": "Error sending SQS message"}, status=501
                    )
            except Exception as e:
                logger.error(traceback.format_exc())
                return render(
                    request, "signup_page.html", context={"message": "Error"}, status=501
                )
                
                

@login_required(login_url="/auth/login/")
def logout_api(request):
    logout(request)
    return redirect("/auth/login/")


def get_ac(request):
    if request.method == "GET":
        return render(
            request, "get_ac.html", context={"message": "Success"}, status=201
        )
    elif request.method == "POST":
        ac_data = list()
        count = 0
        while True:
            count += 1
            try:
                ac = request.POST[f"acWatts{count}"]
                ac_data.append(ac)
            except:
                break
        ac_data = list(map(int, ac_data))
        for i in ac_data:
            user = consumer.objects.get(id=request.user)
            new = airConditioner(user=user, watts=i)
            new.save()
        return redirect("/")
