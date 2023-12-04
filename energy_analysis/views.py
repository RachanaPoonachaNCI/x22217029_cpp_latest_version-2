import psycopg2
from django.conf import settings
import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication import models as authModels
from .models import airConditionerUnits, electricityUnits, gas as GasUnits, dailyHistory
import math
import boto3
from energy_management.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

@login_required(login_url="/auth/login/")
def dashboard(request):
    if request.method == "GET":
        try:
            allData = list(
                map(
                    lambda x: {
                        "date": x.date,
                        "energy": x.totalElectricity,
                        "gas": x.totalGas,
                        "ac": x.totalAc,
                    },
                    dailyHistory.objects.filter(user__id=request.user),
                )
            )

            matrix = {
                "dailyAvgEnergy": sum(list(map(lambda x: x["energy"], allData)))
                / len(list(map(lambda x: x["energy"], allData))),
                "dailyAvgAc": sum(list(map(lambda x: x["ac"], allData)))
                / len(list(map(lambda x: x["ac"], allData))),
                "dailyAvgGas": sum(list(map(lambda x: x["gas"], allData)))
                / len(list(map(lambda x: x["gas"], allData))),
                "weeklyAvgEnergy": sum(
                    list(
                        map(
                            lambda x: x["energy"],
                            list(
                                filter(
                                    lambda x: x["date"]
                                    > datetime.datetime.now().date()
                                    - datetime.timedelta(days=7),
                                    allData,
                                )
                            ),
                        )
                    )
                )
                / len(
                    list(
                        map(
                            lambda x: x["energy"],
                            list(
                                filter(
                                    lambda x: x["date"]
                                    > datetime.datetime.now().date()
                                    - datetime.timedelta(days=7),
                                    allData,
                                )
                            ),
                        )
                    )
                ),
                "weeklyAvgAc": sum(
                    list(
                        map(
                            lambda x: x["ac"],
                            list(
                                filter(
                                    lambda x: x["date"]
                                    > datetime.datetime.now().date()
                                    - datetime.timedelta(days=7),
                                    allData,
                                )
                            ),
                        )
                    )
                )
                / len(
                    list(
                        map(
                            lambda x: x["ac"],
                            list(
                                filter(
                                    lambda x: x["date"]
                                    > datetime.datetime.now().date()
                                    - datetime.timedelta(days=7),
                                    allData,
                                )
                            ),
                        )
                    )
                ),
                "weeklyAvgGas": sum(
                    list(
                        map(
                            lambda x: x["gas"],
                            list(
                                filter(
                                    lambda x: x["date"]
                                    > datetime.datetime.now().date()
                                    - datetime.timedelta(days=7),
                                    allData,
                                )
                            ),
                        )
                    )
                )
                / len(
                    list(
                        map(
                            lambda x: x["gas"],
                            list(
                                filter(
                                    lambda x: x["date"]
                                    > datetime.datetime.now().date()
                                    - datetime.timedelta(days=7),
                                    allData,
                                )
                            ),
                        )
                    )
                ),
                "monthlyTotalEnergy": sum(
                    list(
                        map(
                            lambda x: x["energy"],
                            filter(
                                lambda x: x["date"].month
                                == datetime.datetime.now().date().month
                                and x["date"].year
                                == datetime.datetime.now().date().year,
                                allData,
                            ),
                        )
                    )
                ),
                "monthlyTotalAc": sum(
                    list(
                        map(
                            lambda x: x["ac"],
                            filter(
                                lambda x: x["date"].month
                                == datetime.datetime.now().date().month
                                and x["date"].year
                                == datetime.datetime.now().date().year,
                                allData,
                            ),
                        )
                    )
                ),
                "monthlyTotalGas": sum(
                    list(
                        map(
                            lambda x: x["gas"],
                            filter(
                                lambda x: x["date"].month
                                == datetime.datetime.now().date().month
                                and x["date"].year
                                == datetime.datetime.now().date().year,
                                allData,
                            ),
                        )
                    )
                ),
            }
        except:
            matrix = []
        return render(
            request,
            "dashboard.html",
            context={"message": "Success", "matrix": matrix},
            status=201,
        )


@login_required(login_url="/auth/login/")
def profile(request):
    if request.method == "GET":
        user_id = request.user.id
        user = authModels.consumer.objects.get(id=request.user)
        db_parameters = settings.DATABASES['default']
        connection = psycopg2.connect(database=db_parameters["NAME"], user=db_parameters["USER"], password=db_parameters["PASSWORD"], 
            host=db_parameters["HOST"], port=db_parameters["PORT"])
        cursor = connection.cursor()
        
        query = f"""
                    SELECT * FROM energy_analysis_dailyhistory WHERE user_id = '{user.id}' ORDER BY date;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        print(result)
        history = list(
            map(
                lambda x: {
                    "date": x.date.strftime("%Y-%m-%d"),
                    "energy": x.totalElectricity,
                    "gas": x.totalGas,
                    "ac": x.totalAc,
                },
                dailyHistory.objects.filter(user__id=request.user).order_by("date")
            )
        )
        user = authModels.consumer.objects.get(id=request.user)
        filename = user.pp  # Changing this to the desired file name
        bucket_name = AWS_STORAGE_BUCKET_NAME
        print(bucket_name)
        url = ""
        try:
            s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': filename},
                ExpiresIn=3600  # Setting the expiration time for the URL in seconds (e.g., 1 hour)
                )
        except Exception as e:
                print(f"Error uploading file to S3: {e}")        
       # except:
        #  print("Credentials not available")
        username = user.name if user.name != None else "change username"
        return render(
            request,
            "profile_page.html",
            context={
                "message": "Success",
                "history": history,
                "username": username,
                "email": request.user,
                "profile_pic": url
            },
            status=201,
        )
    elif request.method == "POST":
        reqType = request.POST.get("type")
        print(reqType, request.POST)
        if reqType == "user_name":
            username = request.POST["user_name"]
            user = authModels.consumer.objects.get(id=request.user)
            user.name = username
            user.save()
        elif reqType == "profile_pic":
            #uploading profile pictires to S3
            file = request.FILES.get("profile_pic")
            filename = "any_file.extension"  # Change this to the desired file name
            bucket_name = AWS_STORAGE_BUCKET_NAME
            s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            try:
            # Upload the file to the specified bucket
                s3.upload_fileobj(file, bucket_name, filename)
            #except Exception as e:
            #    print(e)
            except Exception as e:
                print(f"Error uploading file to S3: {e}")
            user = authModels.consumer.objects.get(id=request.user)
            user.pp = filename
            user.save()
        return HttpResponse("Success")


@login_required(login_url="/auth/login/")
def form_submit(request):
    if request.method == "GET":
        ac_obj = authModels.airConditioner.objects.filter(user__id=request.user)
        ac = list()
        count = 0
        for obj in ac_obj:
            count += 1
            ac.append(f"AC-{count} used [{obj.watts} W]")
        return render(
            request,
            "user_input.html",
            context={"message": "Success", "ac_list": ac},
            status=201,
        )
    elif request.method == "POST":
        date = request.POST["date"]
        energy = float(request.POST["energy"])
        gas = float(request.POST["gas"])

        ac_data = list()
        totalAcWatt = 0

        count = 0
        ac_obj = authModels.airConditioner.objects.filter(user__id=request.user)
        ac = list()
        count = 0
        for obj in ac_obj:
            count += 1
            ac.append((obj, f"AC-{count} used [{obj.watts} W]"))
        for i in ac:
            hrs = float(request.POST[i[1]])
            ac_data.append((hrs, i[0]))
            totalAcWatt += hrs * i[0].watts

        consumerObj = authModels.consumer.objects.get(id=request.user)
        for i in ac_data:
            newAc = airConditionerUnits(date=date, time=i[0], ac=i[1])
            newAc.save()

        newGas = GasUnits(date=date, weight=gas, user=consumerObj)
        newGas.save()

        newEnergy = electricityUnits(date=date, units=energy, user=consumerObj)
        newEnergy.save()
#lamdba
        newHistory = dailyHistory(
            date=date,
            user=consumerObj,
            totalAc=totalAcWatt,
            totalElectricity=energy,
            totalGas=gas,
        )
        newHistory.save()

        return redirect("/")
