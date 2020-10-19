from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from . import creator
from django.conf import settings
import os
import re
import pandas as pd
from sqlalchemy import create_engine
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import requests
import pathlib
from . import test_pd
from django.core.cache import cache
# Create your views here.
def index(request):
    df,l = creator.Create_df()
    table_1 = pd.DataFrame(df[["Make", "Model", "Year"]])
    table_1["car"] = table_1["Make"] + [" "] + table_1["Model"] + [" "] + table_1["Year"]
    table_1["Views"] = df[f"Views {l}"]
    table_1 = table_1.drop(['Make', 'Model', 'Year'], axis=1)
    table_1 = table_1.sort_values(by=['Views'], ascending=False)
    table_1 = str(table_1.to_html(justify="center", index=False, header=False))
    infile = open("analytics/templates/table_views_daily.html", 'w')
    infile.write(table_1)
    infile.close()

    df1=creator.Create_df_Days()

    table_2 = pd.DataFrame(df1[["Make","Model","Year"]])
    table_2["car"]=table_2["Make"]+[" "]+table_2["Model"]+[" "]+table_2["Year"]
    table_2=table_2.drop(['Make','Model','Year'],axis=1)
    table_2["Average Days Online"]=df1["Average Days Online"] 
    table_2=table_2.sort_values(by=["Average Days Online"],ascending=True)
    table_2=str(table_2.to_html(justify="center",index=False,header=False))
    infile = open("analytics/templates/table_days_daily.html", 'w')
    infile.write(table_2)
    infile.close()
    path= os.path.join(settings.MEDIA_ROOT,"latest")
    img_list=os.listdir(path+"/")
    Days_image=settings.MEDIA_URL+"latest/"+img_list[0]
    Views_image = settings.MEDIA_URL+"latest/" + img_list[1]
    context={'Days_Image':Days_image,"Views_Image":Views_image}
    return render(request,'daily.html',context)
def weekly(request):
    df_views, l = creator.Create_df()
    table_1 = pd.DataFrame(df_views[["Make", "Model", "Year"]])
    table_1["Make"] = table_1["Make"] + [" "] + table_1["Model"] + [" "] + table_1["Year"]
    df_views = df_views.iloc[:, 4:-2]
    l = l

    starting_point= (l-7)*2

    df_views=df_views.iloc[:,starting_point:]
    table_1 = table_1.drop(['Model', 'Year'], axis=1)
    table_1 = pd.concat([table_1, df_views], axis=1)
    unwanted = table_1.columns[table_1.columns.str.startswith('Views Per Day')]
    table_1=table_1.drop(unwanted,axis=1)
    table_1["Average Views Weekly"]=table_1.iloc[:,1:].sum(axis=1).div(7)
    table_1=table_1[["Make","Average Views Weekly"]]
    table_1 = table_1.sort_values(by=['Average Views Weekly'], ascending=False)
    table_1 = str(table_1.to_html(justify="center", index=False, header=False))
    infile = open("analytics/templates/table_views_weekly.html", 'w')
    infile.write(table_1)
    infile.close()

    df1 = creator.Create_df_Days()

    table_2 = pd.DataFrame(df1[["Make", "Model", "Year"]])
    table_2["Make"] = table_2["Make"] + [" "] + table_2["Model"] + [" "] + table_2["Year"]
    df1 = df1.iloc[:, 4:-1]

    starting_point = (l - 7)
    df_views = df_views.iloc[:, starting_point:]
    table_2 = table_2.drop(['Model', 'Year'], axis=1)
    table_2 = pd.concat([table_2, df1], axis=1)
    table_2["Average Days Online Weekly"] =table_2.iloc[:,1:].sum(axis=1).div(7)
    table_2=table_2[["Make","Average Days Online Weekly"]]
    table_2=table_2[table_2["Average Days Online Weekly"]!=0]
    table_2 = table_2.sort_values(by=["Average Days Online Weekly"], ascending=True)
    table_2 = str(table_2.to_html(justify="center", index=False, header=False))
    infile = open("analytics/templates/table_days_weekly.html", 'w')
    infile.write(table_2)
    infile.close()
    media_path = os.path.join(settings.MEDIA_ROOT,"weekly")
    img_list = os.listdir(media_path + "/")
    Days_image = settings.MEDIA_URL+"weekly/" + img_list[0]
    Views_image = settings.MEDIA_URL+"weekly/" + img_list[1]
    context = {'Days_Image': Days_image, "Views_Image": Views_image}
    return render(request, 'weekly.html', context)
def monthly(request):
    df_views, l = creator.Create_df()
    table_1 = pd.DataFrame(df_views[["Make", "Model", "Year"]])
    table_1["Make"] = table_1["Make"] + [" "] + table_1["Model"] + [" "] + table_1["Year"]
    df_views = df_views.iloc[:, 4:-2]


    starting_point = (l - 30) * 2

    df_views = df_views.iloc[:, starting_point:]
    table_1 = table_1.drop(['Model', 'Year'], axis=1)
    table_1 = pd.concat([table_1, df_views], axis=1)
    unwanted = table_1.columns[table_1.columns.str.startswith('Views Per Day')]
    table_1 = table_1.drop(unwanted, axis=1)
    table_1["Average Views Monthly"] = table_1.iloc[:, 1:].sum(axis=1).div(7)
    table_1 = table_1[["Make", "Average Views Monthly"]]
    table_1 = table_1.sort_values(by=['Average Views Monthly'], ascending=False)
    table_1 = str(table_1.to_html(justify="center", index=False, header=False))
    infile = open("analytics/templates/table_views_monthly.html", 'w')
    infile.write(table_1)
    infile.close()

    df1 = creator.Create_df_Days()

    table_2 = pd.DataFrame(df1[["Make", "Model", "Year"]])
    table_2["Make"] = table_2["Make"] + [" "] + table_2["Model"] + [" "] + table_2["Year"]
    df1 = df1.iloc[:, 4:-1]

    starting_point = (l - 30)
    df_views = df_views.iloc[:, starting_point:]
    table_2 = table_2.drop(['Model', 'Year'], axis=1)
    table_2 = pd.concat([table_2, df1], axis=1)
    table_2["Average Days Online Monthly"] = table_2.iloc[:, 1:].sum(axis=1).div(7)
    table_2 = table_2[["Make", "Average Days Online Monthly"]]
    table_2 = table_2.sort_values(by=["Average Days Online Monthly"], ascending=True)
    table_2 = table_2[table_2["Average Days Online Monthly"] != float(0)]
    table_2 = str(table_2.to_html(justify="center", index=False, header=False))
    infile = open("analytics/templates/table_days_monthly.html", 'w')
    infile.write(table_2)
    infile.close()
    path = os.path.join(settings.MEDIA_ROOT,"monthly")
    img_list = os.listdir(path + "/")
    Days_image = settings.MEDIA_URL+"monthly/" + img_list[0]
    Views_image = settings.MEDIA_URL+"monthly/" + img_list[1]
    context = {'Days_Image': Days_image, "Views_Image": Views_image}
    return render(request, 'weekly.html', context)
def search(request,mode):
    # try:
        # cache.clear()
    constraints=request.POST['Container']
        # print("Here",str(request.POST.get('Container')))
        # print(constraints)
        # print(request.session.keys())

    constraints=constraints.split(" ")
    df_days=creator.Create_df_Days()
    # creator.Plot(df_days,constraints)
    print("Days online created")

    df_views,l=creator.Create_df()
    if mode!="latest":
        df_views,df_days=creator.Pre_Plot(df_views,df_days,l,mode)
    creator.Plot(df_days, constraints, mode)
    creator.Plot_Views(df_views,constraints,mode)

    # if mode=="latest":
    #     mode="index"
    return redirect(f'{mode}')
    # except:
    #     return render(request,'error.html')
@csrf_exempt
def csv(request):
    #file =request.POST['file']
    file=request.POST['link']
    r=requests.get(file)
    url_content=r.content
    csv_file=open('file1.csv','wb')
    csv_file.write(url_content)
    csv_file.close()
    Days_df= test_pd.set_Views()
    test_pd.Set_Days_Online(Days_df)
    return HttpResponse("Uploaded")

def dummy(request):
    return redirect('latest')