import json
import requests
from tkinter import *
from PIL import Image, ImageTk

window = Tk()
labels = []
images = []

API_KEY = "RGAPI-23869e03-45cc-4ffe-a6f5-bb55c926890f"
nbBaseURL = 'https://americas.api.riotgames.com'
PLATFORM_URL = "https://na1.api.riotgames.com"

def getPuuid(gameName, tagLine):
    nbApiURL = f'/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={API_KEY}'
    nbApiQuestion = nbBaseURL + nbApiURL

    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(nbApiQuestion, headers = headers)
    data = response.json()
    puuid = data["puuid"]
    return puuid 

def getMastery(PUUID):
    nbApiURL = f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{PUUID}"  
    nbApiQuestion = PLATFORM_URL + nbApiURL
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(nbApiQuestion, headers = headers)
    data = response.json()
    print(response)
    return data    

def displayChampions(name, tag):
    for label in labels:
        label.destroy()
    labels.clear()
    images.clear()

    with open("champion.json", "r", encoding="utf-8") as f:
        champ_data = json.load(f)

    id_to_name = {
        int(info["key"]): info["name"]
        for info in champ_data["data"].values()
    }

    puuid = getPuuid(name, tag)
    print(puuid)
    champ_id = getMastery(puuid)
   
    topMasteries = []
    topMasteriresImages = []
    for i in range(10):
        topMasteries.append(f"{i+1}. {id_to_name[champ_id[i]["championId"]]}: {champ_id[i]["championPoints"]} points")
        topMasteriresImages.append(f"imgs\{id_to_name[champ_id[i]["championId"]]}.png")

    for i in range(len(topMasteries)):
        img = Image.open(topMasteriresImages[i])
        img = img.resize((50,50))
        photo = ImageTk.PhotoImage(img)
        images.append(photo) 
        label = Label(window, text=topMasteries[i], image=photo, compound="left", padx=10, width=190, height=55, anchor="w")
        label.pack(pady=0)
        labels.append(label)

def onEnter(entry1, entry2):
    name = entry1.get()
    tag = entry2.get()

    name = name.replace(" ","").lower()
    tag = tag.replace(" ","").lower()

    if name:
        displayChampions(name, tag)

def GUI():
    window.title("Champion Mastery")
    window.geometry("900x600")
    window.configure(bg='gray25')
    label1 = Label(window, text="Game Name:")
    label1.pack(pady=4)

    entry1 = Entry(window, width=30)
    entry1.pack(pady = 4)

    label2 = Label(window, text="Riot Tag (ex: 12345) :")
    label2.pack(pady=4)
    entry2 = Entry(window, width=30)
    entry2.pack(pady = 2)

    entry1.bind("<Return>", lambda event: onEnter(entry1,entry2))
    entry2.bind("<Return>", lambda event: onEnter(entry1,entry2))

    window.mainloop()

def main():
    GUI()
   
if __name__ == "__main__":
    main()