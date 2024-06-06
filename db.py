#DataBase system!
from konfig import Config
import os
import json

dbpath = os.getcwd()
istrue = False

#니 DB 제대로 되있는지 확인함
def db_check():
    global istrue
    """Function to check if the database is okay"""
    DBtypes = ["AutoSave"]
    SaveFilse = ["Player.json"]
    if not os.path.isdir("./db"):
        os.mkdir("db")
        db_check()
    elif os.path.isfile("./db") and os.path.isfile("./db" + DBtypes):
        istrue = True
        pass
    else:
        for i in DBtypes:
            if not os.path.isdir("./db/" + i):
                os.mkdir("./db/" + i)
        for i in SaveFilse:
            data =  [
                        {
                            "name" : "Player",
                            "money" : 100000
                        }

                    ]
            if not os.path.isdir("./db/AutoSave/" + i):
                with open("./db/AutoSave/" + i, "w") as f:
                    json.dump(data,f)
                
        
        
def gamesave(Are_you_auto, money, havestocks):
    global istrue
    """Function to save"""
    os.chdir(dbpath + "save")
    if istrue == True:
        if Are_you_auto == "yes":
            #돈 저장
            
            #주식 저장
            pass
    else:
        db_check()
        