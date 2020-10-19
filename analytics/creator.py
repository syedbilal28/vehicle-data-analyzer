from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings
import os
def Create_df():
    engine=create_engine("sqlite:///"+"C:/Users/Bilal/PycharmProjects/car-analysis/car/db.sqlite3")
    df= pd.read_sql_query(sql="SELECT * from Cars",con=engine)
    lst1=['Model','Make','Year']
    lst2=[col for col in df if col.startswith('Views')]
    #lst3=[col for col in df if col.startswith("Days")]
    columns=lst1+lst2
    print(df.columns)
    print(columns)
    clean_df=df[columns]
    clean_df["Year"]=clean_df["Year"].astype(int).astype(str)
    l=int(((len(clean_df.columns)-5)/2))
    print("length",l)
    engine.dispose()
    return clean_df,l
def Create_df_Days():
    engine = create_engine("sqlite:///" + "C:/Users/Bilal/PycharmProjects/car-analysis/car/db.sqlite3")
    df = pd.read_sql_query(sql="SELECT * from Car_Days", con=engine)
    lst1 = ['Model', 'Make', 'Year']
    lst3 = list(df.filter(like="Days").columns)
    columns = lst1 + lst3
    clean_df=df[columns]
    clean_df["Year"]=clean_df["Year"].astype(int).astype(str)
    engine.dispose()
    return clean_df
def Plot(df,constraints,mode):
    main = pd.DataFrame(df.loc[(df['Make'] == constraints[0]) & (df['Model'] == constraints[1]) & (df['Year'] == constraints[2])])
    columns=[col for col in df if col.startswith("Days")]
    main=main[columns]
    main=main.iloc[0]
    l=len(main)
    plt.figure(figsize=(9, 6))
    plt.plot(range(1,l+1),[i for i in main])
    plt.xlabel('Time')
    plt.ylabel('Days Online')
    plt.title("{} {} {}".format(constraints[0], constraints[1], constraints[2]))
    file_path=os.path.join(settings.MEDIA_ROOT,f"{mode}")
    path = file_path + "/"
    filelist = [ f for f in os.listdir(path)]
    for f in filelist:
        os.remove(os.path.join(path, f))
    #os.remove(path+"Days Online {} {} {}.jpg".format(constraints[0], constraints[1], constraints[2])))
    plt.savefig(path+"Days Online {} {} {}.jpg".format(constraints[0], constraints[1], constraints[2]))
    plt.close()
def Plot_Views(df,constraints,mode):
    main = pd.DataFrame(df.loc[(df['Make'] == constraints[0]) & (df['Model'] == constraints[1]) & (df['Year'] == constraints[2])])
    columns=[col for col in df if col.startswith("Views Per Day")]
    print("columns",columns)
    main = main[columns]
    main = main.iloc[0]
    l = len(main)
    plt.figure(figsize=(9, 6))
    plt.plot(range(1, l + 1), [i for i in main])
    plt.xlabel('Time')
    plt.ylabel('Views Per Day')
    plt.title("{} {} {}".format(constraints[0], constraints[1], constraints[2]))
    file_path = os.path.join(settings.MEDIA_ROOT, f"{mode}")
    path = file_path+"/"
    #os.remove(path+"Views Per Day.jpg")
    
    plt.savefig(path+"Views Per Day {} {} {}.jpg".format(constraints[0], constraints[1], constraints[2]))
    plt.close()
def Pre_Plot(df_views,df_days,l,mode):
    if mode=="weekly":
        to_sub=7
    elif mode=="monthly":
        to_sub=30
    starting_point_views = ((l - to_sub) * 2)+3
    df_views=df_views.iloc[:,:-2]
    df_pre = df_views.iloc[:, :3]
    df_views = df_views.iloc[:, starting_point_views:]
    df_views = pd.concat([df_pre, df_views], axis=1)
    starting_point_days = (l - 7)+3
    df_days=df_days.iloc[:,:-1]
    df_pre = df_days.iloc[:, :3]
    df_days = df_days.iloc[:, starting_point_days:]
    df_days = pd.concat([df_pre, df_days], axis=1)
    return df_views,df_days