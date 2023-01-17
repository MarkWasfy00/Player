import eyed3
import obswebsocket
import os
from os import path
import random
from bs4 import BeautifulSoup
from time import gmtime, strftime , time , sleep
import csv
import toml



def on_off_gate(var):
    if str(var).lower() == "on":
        return True
    else:
        return False

data = toml.load("./config.toml")


CONFIG_HOST = data["server"]["host"]
CONFIG_PORT = data["server"]["port"]
CONFIG_PASSWORD = data["server"]["password"]

CONFIG_SONG_FOLDER = data["folders"]["song_folder"]
CONFIG_ART_FOLDER = data["folders"]["art_folder"]
CONFIG_PROMO_FOLDER = data["folders"]["promo_folder"]
CONFIG_LOG_FOLDER = data["folders"]["log_folder"]

CONFIG_STATIONS = data["commercial"]["display_ad_every"]

CONFIG_V_MAIN_SCREEN = data["screens"]["main_screen"]
CONFIG_V_NEXT_SCREEN = data["screens"]["next_up_screen"]

CONFIG_V_SONG_MEDIA = data["media"]["song_media"]
CONFIG_V_VIDEO_MEDIA = data["media"]["promo_media"]

CONFIG_BREAK_LENGTH  = data["break"]["break_length"]

CONFIG_ENABLE_MUSIC_SHUFFLE = on_off_gate(data["music"]["shuffle"])

CONFIG_GRAD_FROM = data["gradient"]["from"]
CONFIG_GRAD_TO = data["gradient"]["to"]
CONFIG_GRAD_ANGLE = data["gradient"]["angle"]


class Music:
    
    def __init__(self,songs_folder,album_art_folder,promo_folder):
        self.QUEUE = "#"
        self.TITLE = "#"
        self.ARTIST = "#"
        self.ART = "#"
        self.PROMO = "#"
        self.ALBUM_ART_FOLDER_NAME = album_art_folder
        self.ALBUM_ART_PATH = path.join(os.getcwd(),f"{album_art_folder}")
        self.SONGS_PATH = path.join(os.getcwd(),f"{songs_folder}")
        self.PROMO_PATH = path.join(os.getcwd(),f"{promo_folder}")

    def generate_image_url(self):
        try:
            audiofile = eyed3.load(self.QUEUE)
            title = audiofile.tag.title
            for image in audiofile.tag.images:
                image_name = "{0}.jpg".format(title)
                image_file = open(path.join(self.ALBUM_ART_PATH,image_name), "wb")
                image_file.write(image.image_data)
                image_file.close()
        except:
            print(f"{bcolors.FAIL}Failed to fetch the current song art")

    def set_current_song_settings(self,song_intry):
        try:
            audiofile = eyed3.load(path.join(self.SONGS_PATH,song_intry))
            self.QUEUE = path.join(self.SONGS_PATH,song_intry)
            self.TITLE  = audiofile.tag.title
            self.ARTIST = audiofile.tag.artist
            self.ART = f"../{self.ALBUM_ART_FOLDER_NAME}/{'{0}.jpg'.format(audiofile.tag.title)}"
        except:
            print(f"{bcolors.FAIL}Failed to set the current song")

    def set_music_html(self):
        try:
            # music.set_files_html("./backUp/indexback.html","./html/index.html")
            with open("./html/index.html", "r") as f:
                doc = BeautifulSoup(f, "html.parser")

            doc.body.attrs["style"] = f"background-image: linear-gradient({CONFIG_GRAD_ANGLE}deg, {CONFIG_GRAD_FROM} , {CONFIG_GRAD_TO} );"

            if len(self.ARTIST) >= 24:
                artist = doc.find("div", class_= "artist")
                new_marquee = doc.new_tag("marquee")
                new_marquee.attrs["behavior"] = "alternate"
                new_marquee.attrs["scrolldelay"] = "200"
                new_marquee.string = self.ARTIST
                artist.clear()
                artist.append(new_marquee)
            else:
                artist = doc.find("div", class_= "artist")
                artist.string = self.ARTIST

            songname = doc.find("div", class_="songname")
            songname.string = self.TITLE

            photo = doc.find("img", class_="musicphoto")
            photo.attrs["src"] = self.ART

            with open("./html/index.html", "w", encoding="utf-8") as file:
                file.write(str(doc))
        except:
            print(f"{bcolors.FAIL}Failed to set html file")

    def set_next_music_html(self,song_name,artist_name):
        try:
            # music.set_files_html("./backUp/nextback.html","./html/nextsong.html")
            with open("./html/nextsong.html", "r") as f:
                doc = BeautifulSoup(f, "html.parser")

            indicator = doc.find("div", class_="indicator")
            indicator.string = "Next up"

            songname = doc.find("div", class_="songname")
            songname.string = song_name

            artist = doc.find("div", class_= "artist")
            artist.string = artist_name

            with open("./html/nextsong.html", "w", encoding="utf-8") as file:
                file.write(str(doc))
        except:
            print(f"{bcolors.FAIL}Failed to set html file")

    def set_last_music_html(self):
        try:
            # self.set_files_html("./backUp/nextback.html","./html/nextsong.html")
            with open("./html/nextsong.html", "r") as f:
                doc = BeautifulSoup(f, "html.parser")

            indicator = doc.find("div", class_="indicator")
            indicator.string = ""

            songname = doc.find("div", class_="songname")
            songname.string = ""

            artist = doc.find("div", class_= "artist")
            artist.string = ""

            with open("./html/nextsong.html", "w", encoding="utf-8") as file:
                file.write(str(doc))
        except:
            print(f"{bcolors.FAIL}Failed to set last music")

    def set_files_html(self,file_name,to_path):
        with open(file_name,"r") as f:
            doc = BeautifulSoup(f, "html.parser")

        with open(to_path,"w", encoding="utf-8") as file:
            file.write(str(doc))

    def get_next_music_meta(self,song_intry):
        try:
            audiofile = eyed3.load(path.join(self.SONGS_PATH,song_intry))
            title  = audiofile.tag.title
            artist = audiofile.tag.artist
            return [title,artist]
        except:
            print(f"{bcolors.FAIL}Failed to fetch next song")

    def toggle_next_song(self,visible):
        with open("./html/nextsong.html", "r") as f:
            doc = BeautifulSoup(f, "html.parser")

        if visible:
            change_vis = doc.find("div", class_="nextsong")
            change_vis.attrs["style"] = "animation: 1s fade forwards;"
        else:
            change_vis = doc.find("div", class_="nextsong")
            change_vis.attrs["style"] = "animation: 1s fadeout forwards;"
        
        with open("./html/nextsong.html", "w",encoding="utf-8") as file:
            file.write(str(doc))

    def set_promo_video(self,video_intry):
        self.PROMO = path.join(self.PROMO_PATH,video_intry)

class Logger:
    LIST = []

    def __init__(self,rounds=8):
        self.STATION = rounds
        self.PROMO = rounds + 1
        with open(CONFIG_LOG_FOLDER, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Artist", "Start Time Played","Play Length","Played at commercial"])
            

    def add(self,song_name,artist_name,duration,played_at_comm=False):
        self.LIST.append(song_name)
        try:
            with open(CONFIG_LOG_FOLDER,"a", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([f"{song_name}", f"{artist_name}", f"{get_time()}",f"{ms_format(duration)}",f"{played_at_comm}"])
        except:
            print(f"{bcolors.FAIL}Failed to Add")

    def count(self):
        return len(self.LIST)

    def flush(self):
         self.LIST = []

class Obs:
    def  __init__(self,host,port,password):
        self.client = obswebsocket.obsws(host, port, password)

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()

    def send_payload(self,payload):
        result = self.client.send(payload)
        return result

    def set_music(self,source_name,song_path):
        payload = {
            "request-type": "SetSourceSettings",
            "sourceName": source_name,
            "sourceSettings": {
                "local_file": song_path
            },
            "message-id": 1
        }
        self.send_payload(payload)

    def refresh_source(self,source_name):
        payload = {
            "request-type": "RefreshBrowserSource",
            "sourceName": source_name,
            "message-id": 1
        }
        self.send_payload(payload)

    def get_music_ms(self,source_name):
        payload = {
            "request-type": "GetMediaTime",
            "sourceName": source_name,
            "message-id": 1
        }
        return self.send_payload(payload)

    def get_music_duration(self,source_name):
        payload = {
            "request-type": "GetMediaDuration",
            "sourceName": source_name,
            "message-id": 1
        }
        return self.send_payload(payload)

    def get_music_state(self,source_name):
        payload = {
            "request-type": "GetMediaState",
            "sourceName": source_name,
            "message-id": 1
        }
        return self.send_payload(payload)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def shuffle_my_list(list,gate):
        if gate:
            random.shuffle(list)
            return list
        else:
            return list

def get_dir_list(dir_name):
    return os.listdir(path.join(os.getcwd(),dir_name))

def ms_format(milliseconds):
    total_seconds= int(milliseconds / 1000)
    minutes= int(total_seconds / 60)
    seconds= int(total_seconds - minutes * 60)
    return "{}:{:02}".format(minutes, seconds)

def get_time():
    return strftime("%H:%M:%S", gmtime())

def random_choice(list):
    return random.choice(list)


#---------------------------------

if __name__ == "__main__":
    try:
        obs = Obs(CONFIG_HOST,CONFIG_PORT,CONFIG_PASSWORD)
        music = Music(CONFIG_SONG_FOLDER,CONFIG_ART_FOLDER,CONFIG_PROMO_FOLDER)
        logs = Logger(CONFIG_STATIONS)

        print(f"{bcolors.WARNING}Script Started...")

        music.set_files_html("./backUp/indexback.html","./html/index.html")
        music.set_files_html("./backUp/nextback.html","./html/nextsong.html")

        shuffled_list = shuffle_my_list(get_dir_list(CONFIG_SONG_FOLDER),CONFIG_ENABLE_MUSIC_SHUFFLE)
        counter = 0
        while True:
            if len(shuffled_list) > counter:
                if logs.count() < logs.STATION:
                    music.set_current_song_settings(shuffled_list[counter])
                    music.generate_image_url()
                    music.set_music_html()
                    print(f"{bcolors.OKCYAN}Starting: {music.TITLE}")

                    obs.connect()
                    obs.refresh_source(CONFIG_V_MAIN_SCREEN)
                    obs.set_music(CONFIG_V_SONG_MEDIA,music.QUEUE)

                    music_duration = obs.get_music_duration(CONFIG_V_SONG_MEDIA)["mediaDuration"]
                    logs.add(music.TITLE,music.ARTIST,music_duration)

                    showed = False
                    is_next_song_available = False

                    sleep(1)
                    while obs.get_music_state(CONFIG_V_SONG_MEDIA)["mediaState"] == "playing":
                        # time.sleep(1)
                        music_timestamp = obs.get_music_ms(CONFIG_V_SONG_MEDIA)["timestamp"]
                        if music_duration < music_timestamp + 30000 and not showed:
                            try:
                                next_music_meta = music.get_next_music_meta(shuffled_list[counter+1])
                                music.set_next_music_html(next_music_meta[0],next_music_meta[1])
                                music.toggle_next_song(True)
                                obs.refresh_source(CONFIG_V_NEXT_SCREEN)
                                showed = True
                                is_next_song_available = True
                            except:
                                music.set_last_music_html()
                                music.toggle_next_song(True)
                                obs.refresh_source(CONFIG_V_NEXT_SCREEN)
                                showed = True

                    if(is_next_song_available):
                        music.toggle_next_song(False)
                        obs.refresh_source(CONFIG_V_NEXT_SCREEN)
                    counter += 1

                elif logs.count() == logs.STATION:
                    music.set_current_song_settings(shuffled_list[counter])
                    music.generate_image_url()
                    music.set_music_html()
                    print(f"{bcolors.OKCYAN}Starting Break Song: {music.TITLE}")

                    obs.connect()
                    obs.refresh_source(CONFIG_V_MAIN_SCREEN)
                    obs.set_music(CONFIG_V_SONG_MEDIA,music.QUEUE)
                    music_duration = obs.get_music_duration(CONFIG_V_SONG_MEDIA)["mediaDuration"]
                
                    logs.add(music.TITLE,music.ARTIST,music_duration,True)

                    delay = 60 * CONFIG_BREAK_LENGTH
                    close_time = time() + delay
                    while True:
                        if time() > close_time:
                            obs.set_music(CONFIG_V_SONG_MEDIA,"")
                            break

                    counter += 1

                else:
                    print(f"{bcolors.BOLD}Switching To Promo Video ...")
                    logs.flush()
                    get_promo_lists = shuffle_my_list(get_dir_list(CONFIG_PROMO_FOLDER),True)
                    music.set_promo_video(random_choice(get_promo_lists))
                    obs.connect()
                    obs.set_music(CONFIG_V_VIDEO_MEDIA,music.PROMO)
                    sleep(1)
                    while obs.get_music_state(CONFIG_V_VIDEO_MEDIA)["mediaState"] == "playing":
                        pass
            else:
                print(f"{bcolors.WARNING}Songs Finished !")
                break

            obs.disconnect()
        print(f"{bcolors.OKGREEN}Done !")
    except:
        print(f"{bcolors.FAIL}Script exited !")
