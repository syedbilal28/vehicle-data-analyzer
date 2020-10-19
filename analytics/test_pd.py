import pandas as pd
import re
from sqlalchemy import create_engine
import os
import pathlib
from . import creator
def set_Views():
    # Create Connection with Databse
    engine=create_engine("sqlite:///"+"C:/Users/Bilal/PycharmProjects/car-analysis/car/db.sqlite3")
    #Get Current Working Directory
    cwd=str(os.getcwd())
    #Read the received file
    df=pd.read_csv(cwd+'/file1.csv',error_bad_lines=False)
    df= df[["Make","Model","Year","Views","Days Online"]]
    clean_df=df.dropna()
    clean_df["Year"] = df["Year"].astype(str)
    #Calling the current database
    df= pd.read_sql_query(sql="SELECT * from Cars",con=engine)
    df=df.drop('index',axis=1)
    l=int((len(df.keys())-5)/2)
    #Convert units into days
    for index,row in clean_df.iterrows():
        
        row["Days Online"]=row["Days Online"].strip()
        row["Make"] = row["Make"].strip()
        row["Model"] = row["Model"].strip()
        row["Year"] = row["Year"].strip()
        if row["Days Online"][-4:]=="hour" or row["Days Online"][-5:]=="hours":
            num=eval(re.sub('\D','', row["Days Online"]))/24    
            clean_df.at[index,'Days Online']=num
        elif row["Days Online"][-4:]=="mins" or row["Days Online"][-3:]=="min":
            num=eval(re.sub('\D','', row["Days Online"]))/(60*24)
            clean_df.at[index,'Days Online']=num
        elif row["Days Online"][-3:]=="day" or row["Days Online"][-4:]=="days":
            num=eval(re.sub('\D','', row["Days Online"]))
            clean_df.at[index,'Days Online']=num

        new=row["Views"].replace(r',','')
        clean_df.at[index,'Views']=eval(new)
    clean_df["Views"]=clean_df["Views"].astype(int)
    clean_df["Days Online"]=clean_df["Days Online"].astype(float)
    #Impose Count function
    clean_df.loc[:, "Count"] = 1
    #Grouping the dataframe
    aggregate_functions={"Views":'mean','Days Online':'mean',"Count":"sum"}
    clean_df=clean_df.groupby(["Model","Make","Year"],as_index=False,sort=False).aggregate(aggregate_functions)
    clean_df["Year"]=clean_df["Year"].astype(object)
    to_process=clean_df
    #Calculate Views Per Day
    clean_df['Views Per Day']=clean_df["Views"]/clean_df['Days Online']/clean_df['Count']
    clean_df["Views Per Day"]=clean_df["Views Per Day"].astype(float)
    clean_df=clean_df.sort_values(by=["Views"],ascending=False)
    clean_df=clean_df.rename(columns={'Views Per Day':'Views Per Day {}'.format(l)})
    clean_df = clean_df.rename(columns={'Views': 'Views {}'.format(l)})
    # df= pd.read_sql_query(sql="SELECT * from Car",con=engine)
    # df=df.drop('index',axis=1)
    final_df=pd.merge(df,clean_df,how="outer",on=["Model","Make",'Year'])

    final_df=final_df.fillna(value=0)
    final_df["Days Online"] = (final_df["Days Online_x"] + final_df["Days Online_y"])
    final_df["Count"] = (final_df["Count_x"] + final_df["Count_y"])
    final_df = final_df.drop(['Days Online_x', 'Days Online_y','Count_x', 'Count_y'], axis=1)
    cols= list(final_df.columns)
    aggregate_functions={}
    for i in cols:
        if i[0:5]=="Views":
            aggregate_functions[i]='mean'
        elif i[0:4]=="Days":
            aggregate_functions[i]='mean'
        elif i[0:5]=="Count":
            aggregate_functions[i]='sum'


    final_df=final_df.groupby(["Model","Make","Year"],as_index=False,sort=False).aggregate(aggregate_functions)
    #final_df["Days Online"]=((final_df["Days Online_x"]+final_df["Days Online_y"])*l).div(l+1)

    final_df=final_df.sort_values(by="Views",ascending=False)
    engine.execute("DROP TABLE Cars")

    final_df.to_sql(con=engine,name="Cars")
    engine.dispose()
    return to_process
def Set_Days_Online(clean_df):
    
    engine=create_engine("sqlite:///"+"C:/Users/Bilal/PycharmProjects/car-analysis/car/db.sqlite3")
    df= pd.read_sql_query(sql="SELECT * from Car_Days",con=engine)
    df=df.drop('index',axis=1)
    l=len(df.keys())-4
    clean_df = clean_df[["Model", "Make", "Year", "Days Online"]]
    clean_df = clean_df.rename(columns={'Days Online': 'Days Online {}'.format(l)})
    final_df=pd.merge(df,clean_df, how="outer", on=['Model', 'Make', 'Year'])
    to_cal=get_fill_value(final_df)
    final_df=final_df.fillna(value=to_cal)
    aggregate_functions={}
    cols=final_df.filter(like="Days")
    for i in cols:
        if i [0:4]=="Days":
            aggregate_functions[i]='mean'
    final_df=final_df.groupby(["Model","Make","Year"],as_index=False,sort=False).aggregate(aggregate_functions)
    
    final_df['Average Days Online']=0
    final_df["Average Days Online"] = final_df.iloc[:, 3:].sum(axis=1).div(l + 1)
    final_df=final_df.sort_values(by="Average Days Online")
    engine.execute("DROP TABLE Car_Days")

    final_df.to_sql(con=engine,name="Car_Days")
    engine.dispose()
def get_fill_value(df):
    '''Depreciated'''
    to_cal={}
    for i in df.columns:
        if i[0:5]=="Views":
            to_cal[i]=0
        elif i[0:4]=="Days":
            to_cal[i]=0
    return to_cal
