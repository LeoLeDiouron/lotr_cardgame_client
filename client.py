import requests, json

from guizero import App, Text, Picture, PushButton
from cleaner import Cleaner

PATH_RESSOURCES = "./ressources/"
BASE_URL = "http://192.168.1.13:8080/api/v1"

class Client:

    def __init__(self):

        self.app = App(title="LORD OF THE RINGS - THE CARD GAME", layout="grid", bg='black')
        self.app.tk.attributes("-fullscreen",True)

        self.background_menu = Picture(self.app, image=PATH_RESSOURCES+"background_menu.png", grid=[0,0,20,20])
        self.button_play = PushButton(self.app, image=PATH_RESSOURCES+"button_play.png", command=self.run, grid=[10,12])
        self.button_exit = PushButton(self.app, command=self.quit, text="QUIT", grid=[10,14])
        self.button_exit.text_color = "white"
        self.app.display()

    def run(self):
        '''
        '''

        response = str(requests.get(BASE_URL + '/access').content)[2:-1]
        self.token = json.loads(response)["id"]
        self.wait_player()
        #self.window_faction.run()

    def wait_player(self):
        '''
        '''

        Cleaner.clean_menu(self)
        self.background_wait_player = Picture(self.app, image=PATH_RESSOURCES+"background_waiting.png", grid=[0,0,20,20])
        self.img_waiting = Picture(self.app, image=PATH_RESSOURCES+"waiting_img.gif", grid=[10,12])
        self.button_exit = PushButton(self.app, command=self.quit, text="QUIT", grid=[10,14])
        self.button_exit.text_color = "white"
        self.background_wait_player.repeat(1000, self.check_players)
    
    def check_players(self):
        '''
        '''

        response = str(requests.get(BASE_URL + '/enter_room/' + self.token).content)[2:-1]
        status = json.loads(response)["status"]
        if status == 'ok':
            self.faction()

    def faction(self):
        '''
        '''

        Cleaner.clean_wait_player(self, self.check_players)
        self.background_faction = Picture(self.app, image=PATH_RESSOURCES+"background_faction.png", grid=[0,0,20,20])
        self.button_faction_1 = PushButton(self.app, image=PATH_RESSOURCES+"faction1.png", command=self.choose_faction, args=[1], grid=[7,12])
        self.button_faction_2 = PushButton(self.app, image=PATH_RESSOURCES+"faction2.png", command=self.choose_faction, args=[2], grid=[8,12])
        self.button_faction_3 = PushButton(self.app, image=PATH_RESSOURCES+"faction3.png", command=self.choose_faction, args=[3], grid=[9,12])
        self.button_faction_4 = PushButton(self.app, image=PATH_RESSOURCES+"faction4.png", command=self.choose_faction, args=[4], grid=[10,12])

    def choose_faction(self, faction_id):
        '''
        '''

        response = str(requests.get(BASE_URL + '/choose_faction/' + self.token + "/" + str(faction_id)).content)[2:-1]
        status = json.loads(response)["status"]
        print(status)
        self.wait_begin()
    
    def wait_begin(self):
        '''
        '''

        Cleaner.clean_choose_faction(self)
        #change the picture
        self.background_wait_begin = Picture(self.app, image=PATH_RESSOURCES+"background_waiting.png", grid=[0,0,20,20])
        self.background_wait_begin.repeat(1000, self.check_begin)
    
    def check_begin(self):
        '''
        '''

        response = str(requests.get(BASE_URL + '/begin/' + self.token).content)[2:-1]
        status = json.loads(response)["status"]
        if status == 'ok':
            self.play()
    
    def play(self):
        '''
        '''

        Cleaner.clean_wait_begin(self, self.check_begin)
        self.init_slot_descriptions()
        #change the picture
        self.background_wait_begin = Picture(self.app, image=PATH_RESSOURCES+"background_play.jpg", grid=[0,0,40,40])
        response = str(requests.get(BASE_URL + '/play/round/1/hand/' + self.token).content)[2:-1]
        datas = json.loads(response)
        self.cards = []
        idx_pos = 1
        for data in datas:
            self.cards.append(PushButton(self.app, image=PATH_RESSOURCES+"cards_min/card_"+data["image"]+"_min.png", command=self.show_card, args=[data], grid=[idx_pos,35]))
            idx_pos += 1
    
    def init_slot_descriptions(self):
        '''
        '''

        self.card_img_big = None
        self.name_card = None
        self.description_card = None
        self.description_power_card = None

    def show_card(self, card):
        '''
        '''

        if self.card_img_big is not None:
            Cleaner.clean_slot_descriptions(self)
        self.card_img_big = Picture(self.app, image=PATH_RESSOURCES+"cards/card_"+card["image"]+".png", grid=[30, 5, 7, 19])
        self.name_card = Text(self.app, text=card["name"], font="Impact", color="white", size=20, align="left", grid=[30,25,10,1])
        self.description_card = Text(self.app, text="\""+self.cut_line(card["description"])+"\"", font="Impact",color="white", size=18,align="left", grid=[30, 27, 10,3])
        self.description_power_card = Text(self.app, text=self.cut_line(card["description_power"]), font="Impact",color="white", size=18,align="left", grid=[30, 31, 10,3])
    
    def cut_line(self, line):
        '''
        '''

        new_line = ""
        while len(line) > 30:
            new_line += line[:30] + "\n"
            line = line[30:]
            if len(line) > 30 and new_line[-1] != " " and line[0] != " ":
                new_line += "-"
        new_line += line
        return new_line

    def quit(self):
        '''
        exit the program
        '''

        exit()


if __name__ == "__main__":
    client = Client()