import threading 
import requests
import json
import random
import ctypes
import sys
import os
from time import strftime, gmtime

banner = ("""
        \u001b[36;1m╔═╗\x1b[0m╦ ╦\u001b[36;1m╦\x1b[0m╔═╗\u001b[36;1m╔╦╗\x1b[0m  
        \u001b[36;1m╚═╗\x1b[0m║║║\u001b[36;1m║\x1b[0m╠╣ \u001b[36;1m ║\x1b[0m   
        \u001b[36;1m╚═╝\x1b[0m╚╩╝\u001b[36;1m╩\x1b[0m╚  \u001b[36;1m ╩\x1b[0m     
        """)

class Log:
    def time():
        return strftime("%H:%M:%S", gmtime())

    def info(text: str):
        print("\t\u001b[36;1m[\u001b[0m%s\u001b[36;1m]\u001b[0m %s\u001b[0m" % (Log.time(), text))

    def error(text: str):
        print("\t\u001b[36;1m[\u001b[0m%s\u001b[36;1m]\u001b[0m %s\u001b[0m" % (Log.time(), text))

class Twitch: 

    def __init__(self):
        self.logging = Log()
        self.name = 0

        if sys.platform == "linux":
            self.cls = lambda: os.system("clear")
        else:
            #self.cls = lambda: os.system("cls")
            self.cls = lambda: os.system("cls & mode 80,24")

        self.cls()
        print(banner)
        ctypes.windll.kernel32.SetConsoleTitleW(f"[Swift] - Menu")
        self.id = Twitch.get_id(input("\tChannel \u001b[36;1m>\u001b[0m "))
        self.tokens = open("data/tokens.txt", "r").read().splitlines()
        self.proxies = open("data/proxies.txt", "r").read().splitlines()
    
        self.valid = 0
        self.invalid = 0

    def get_id(name: str):  
        data = {
            "operationName": "ChannelShell",
            "variables": {
                "login": name
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "580ab410bcd0c1ad194224957ae2241e5d252b2c5173d8e0cce9d32d5bb14efe"
                }
            }
        }

        headers = {
            'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'
        }

        r = requests.post('https://gql.twitch.tv/gql', json=data, headers=headers)
        return r.json()['data']['userOrError']['id']

    def check(self):
        headers = {
            "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
            'Authorization': f"OAuth {random.choice(self.tokens)}"
        }
        json = [{"operationName":"BitsCard_Bits","variables":{},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"fe1052e19ce99f10b5bd9ab63c5de15405ce87a1644527498f0fc1aadeff89f2"}}},{"operationName":"BitsCard_MainCard","variables":{"name":"679087745","withCheerBombEventEnabled":False},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"88cb043070400a165104f9ce491f02f26c0b571a23b1abc03ef54025f6437848"}}}]
        r = requests.post("https://gql.twitch.tv/gql", headers=headers, json=json)
        ctypes.windll.kernel32.SetConsoleTitleW("[Swift] - Checked (%s/%s)" % (self.valid, (self.invalid + self.valid)))
        if "token is invalid." in r.text:
            Log.info(f"Invalid")
            self.invalid += 1
        else:
            data = r.json()[0]["data"]["currentUser"]
            username = data["login"]
            self.valid += 1
            Log.info(f"Validated {username}")

    def report(self):
        headers = {
            'Accept': '*/*',
            'Client-Id': "kimne78kx3ncx6brgo4mv6wki5h1ko", 
            'Authorization': f"OAuth {random.choice(self.tokens)}"
            }
        data = "[{\"operationName\":\"ReportUserModal_ReportWhisper\",\"variables\":{\"input\":{\"description\":\"report context: USER_REPORT\\n\\nwhisper > spam > scam\\n\\ndescription: Scammed me!\",\"reason\":\"spam\",\"targetID\":\"" + self.id + "\",\"wizardPath\":[\"whisper\",\"spam\",\"scam\"]}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"86d6e21ca493b14433662a518a4076ffc0340f6409b3a3a39d434d37730edd5e\"}}}]"
        r = requests.post("https://gql.twitch.tv/gql", json=json.loads(data), headers=headers, proxies={"http": random.choice(self.proxies), "https": random.choice(self.proxies)})
        ctypes.windll.kernel32.SetConsoleTitleW("[Swift] - Reported (%s/%s)" % (self.valid, (self.invalid + self.valid)))
        if "fast" or "RATE" in r.text:
            Log.info("Failed")
            self.invalid += 1
        elif r.status_code == 404:
            Log.info("Failed")
            self.invalid += 1            
        else:
            Log.info(f"Successfully Reported {self.id}")
            self.valid += 1
    
    def follow(self):
        headers = {
            'Client-Id': "kimne78kx3ncx6brgo4mv6wki5h1ko", 
            'Authorization': f"OAuth {random.choice(self.tokens)}"
            }
        data = [{"operationName":"AvailableEmotesForChannel","variables":{"channelID":self.id,"withOwner":True},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"b9ce64d02e26c6fe9adbfb3991284224498b295542f9c5a51eacd3610e659cfb"}}},{"operationName":"FollowButton_FollowUser","variables":{"input":{"disableNotifications":False,"targetID":self.id}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"800e7346bdf7e5278a3c1d3f21b2b56e2639928f86815677a7126b093b2fdd08"}}}]
        r = requests.post("https://gql.twitch.tv/gql", json=data, headers=headers, proxies={"http": random.choice(self.proxies), "https": random.choice(self.proxies)})
        ctypes.windll.kernel32.SetConsoleTitleW("[Swift] - Followed (%s/%s)" % (self.valid, (self.invalid + self.valid)))
        if r.status_code == 200:
            Log.info(f"Attempted to follow {self.id}")
            self.valid += 1
        else:
            Log.info(f"Failed")
            self.invalid += 1
    
    def unfollow(self):
        headers = {
            'Client-Id': "kimne78kx3ncx6brgo4mv6wki5h1ko", 
            'Authorization': f"OAuth {random.choice(self.tokens)}"
            }
        data = [{"operationName":"AvailableEmotesForChannel","variables":{"channelID":self.id,"withOwner":True},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"b9ce64d02e26c6fe9adbfb3991284224498b295542f9c5a51eacd3610e659cfb"}}},{"operationName":"FollowButton_UnfollowUser","variables":{"input":{"targetID":self.id}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"f7dae976ebf41c755ae2d758546bfd176b4eeb856656098bb40e0a672ca0d880"}}}]
        r = requests.post("https://gql.twitch.tv/gql", json=data, headers=headers, proxies={"http": random.choice(self.proxies), "https": random.choice(self.proxies)})
        ctypes.windll.kernel32.SetConsoleTitleW("[Swift] - Unfollowed (%s/%s)" % (self.valid, (self.invalid + self.valid)))    
        if r.status_code == 200:
            Log.info(f"Attempted to unfollow {self.id}")
            self.valid += 1
        else:
            Log.info(f"Failed")
            self.invalid += 1

    def run(self):
        self.cls()
        print(banner)
        print("\t\u001b[36;1m[\u001b[0m0\u001b[36;1m]\u001b[0m Check")
        print("\t\u001b[36;1m[\u001b[0m1\u001b[36;1m]\u001b[0m Follow")
        print("\t\u001b[36;1m[\u001b[0m2\u001b[36;1m]\u001b[0m Unfollow")
        print("\t\u001b[36;1m[\u001b[0m3\u001b[36;1m]\u001b[0m Report")
        print()
        option = input("        Option \u001b[36;1m>\u001b[0m ")
        if option == "0":
            for i in range(len(self.tokens)):
                threading.Thread(target=self.check).start()
        elif option == "1":
            for i in range(len(self.tokens)):
                threading.Thread(target=self.follow).start()
        elif option == "2":
            for i in range(len(self.tokens)):
                threading.Thread(target=self.unfollow).start()
        elif option == "3":
            for i in range(300):
                threading.Thread(target=self.report).start()
        else:
            print("\u001b[31;1m[!]\u001b[0m Invalid Option")
            self.run()

if __name__ == '__main__':
    report = Twitch()
    report.run()
