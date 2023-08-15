import requests,base64,hashlib
from itertools import cycle

def xor(data, key):
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
def gjp_encrypt(data):
        return base64.b64encode(xor(data,"37526").encode()).decode()
def gjp_decrypt(data):
        return xor(base64.b64decode(data.encode()).decode(),"37526")
def generate_chk(values: [int, str] = [], key: str = "", salt: str = "") -> str:
    values.append(salt)

    string = ("").join(map(str, values))

    hashed = hashlib.sha1(string.encode()).hexdigest()
    xored = xor(hashed, key)
    final = base64.urlsafe_b64encode(xored.encode()).decode()

    return final
def generate_upload_seed(data: str, chars: int = 50) -> str:
    if len(data) < chars:
        return data
    step = len(data) // chars
    return data[::step][:chars]

def getGJUsers(target):
    data={
        "secret":"Wmfd2893gb7",
        "str":target
    }
    request =  requests.post(url2+"/getGJUsers20.php",data=data,headers={"User-Agent": ""}).text.split(":")[1::2]
    username = request[0]
    uuid = request[2]
    accountid = request[10]
    return (username,accountid,uuid)

def downloadGJLevel(level):
        data={
                "secret":"Wmfd2893gb7",
                "levelID":level,
        }
        return requests.post(url1+"/downloadGJLevel22.php",data=data,headers={"User-Agent": ""}).text.split(":")

def uploadGJLevel(name,accid,passw,levelString,gjver,lvlName,desc,ver,length,audio,password,original,twoP,songID,objects,coins,reqStars,unlisted,ldm):
    data = {
        "gameVersion": gjver,
        "accountID": accid,
        "gjp": gjp_encrypt(passw),
        "userName": name,
        "levelID": 0,
        "levelName": lvlName,
        "levelDesc": base64.b64encode(desc.encode()).decode(),
        "levelVersion": ver,
        "levelLength": length,
        "audioTrack": audio,
        "auto": 0,
        "password": password,
        "original": original,
        "twoPlayer": twoP,
        "songID": songID,
        "objects": objects,
        "coins": coins,
        "requestedStars": reqStars,
        "unlisted": unlisted,
        "ldm": ldm,
        "levelString": levelString,
        "seed2": generate_chk(key="41274", values=[generate_upload_seed(levelString)], salt="xI25fpAapCQg"),
        "secret": "Wmfd2893gb7"
    }
    return requests.post(url2+"/uploadGJLevel21.php", data=data, headers={"User-Agent":""}).text

print(" /\_/\                       GDReuploader v1.0")
print("( . . )                         by NumbersTada")
print(">)-A-(< Reupload levels from server to server.")
print("----------------------------------------------")
while True:
        url1 = input("Server URL:               ")
        lvl1 = input("Level ID:                 ")
        url2 = input("Reupload Server URL:      ")
        user = input("Reupload Server Username: ")
        passw = input("Reupload Server Password: ")
        levelInfo = downloadGJLevel(lvl1)
        accid = getGJUsers(user)[1]
        print("[Information] Level reuploaded with ID "+uploadGJLevel(user,accid,gjp_encrypt(passw),levelInfo[7],21,levelInfo[3],"This level has been reuploaded using NumbersTada's GDReuploader.",1,0,levelInfo[19],0,levelInfo[1],1,levelInfo[49],levelInfo[37],levelInfo[53],0,0,1))
        print()
