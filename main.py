import os
from os import path
import random
from time import time , sleep
import toml

from modules.Music import Music
from modules.Obs import Obs
from modules.Logger import Logger
from modules.Db import Database


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




def shuffle_my_list(list,gate):
        if gate:
            random.shuffle(list)
            return list
        else:
            return list

def get_dir_list(dir_name):
    return os.listdir(path.join(os.getcwd(),dir_name))

def random_choice(list):
    return random.choice(list)


#---------------------------------

if __name__ == "__main__":
    try:
        obs = Obs(
            CONFIG_HOST,
            CONFIG_PORT,
            CONFIG_PASSWORD
        )

        music = Music(
            CONFIG_SONG_FOLDER,
            CONFIG_ART_FOLDER,
            CONFIG_PROMO_FOLDER,
            CONFIG_GRAD_FROM,
            CONFIG_GRAD_TO,
            CONFIG_GRAD_ANGLE
        )

        logs = Logger(
            CONFIG_LOG_FOLDER,
            CONFIG_STATIONS
        )

        db = Database("Manager.db")

        musicCounter = 0

        music.set_files_html("./backUp/indexback.html","./html/index.html")
        music.set_files_html("./backUp/nextback.html","./html/nextsong.html")
        
        print("Please wait for the script to start loading the songs ...")
        if not os.path.isfile("Manager.db"):
            db.connect()
            db.seed()
            for song in shuffle_my_list(get_dir_list(CONFIG_SONG_FOLDER),CONFIG_ENABLE_MUSIC_SHUFFLE):
                db.add_music(music.get_music_info(song))
            db.commit()
            db.disconnect()
        

        db.connect()
        musicCounter = int(db.count_rows())
        db.disconnect()
        print(f"Script Started...")
        

        counter = 0

        exited_from_promo = False

        while True:
            if musicCounter > counter:
                if logs.count() < logs.STATION:
                    if exited_from_promo:
                        obs.set_music(CONFIG_V_SONG_MEDIA,music.QUEUE)
                        exited_from_promo = False
                    else:
                        music.generate_image_url()
                        db.connect()
                        music.set_current_song_settings(db.get_first_music())
                        db.disconnect()
                        music.set_music_html()
                        obs.connect()
                        obs.refresh_source(CONFIG_V_MAIN_SCREEN)
                        obs.set_music(CONFIG_V_SONG_MEDIA,music.QUEUE)

                    print(f"Starting: {music.TITLE}")
                    showed = False
                    is_next_song_available = False

                    logs.add(music.TITLE,music.ARTIST,music.DURATION)
                    sleep(1)
                    while obs.get_music_state(CONFIG_V_SONG_MEDIA)["mediaState"] == "playing":
                        music_timestamp = obs.get_music_ms(CONFIG_V_SONG_MEDIA)["timestamp"]
                        if music.DURATION_MS < music_timestamp + 32000 and not showed:
                            try:
                                db.connect()
                                next_music_meta = music.get_next_music_meta(db.peek_next_music())
                                db.disconnect()
                                music.set_next_music_html(music.NEXT_TITLE,music.NEXT_ARTIST)
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
                    music.generate_image_url()
                    db.connect()
                    music.set_current_song_settings(db.get_first_music())
                    db.disconnect()
                    music.set_music_html()
                    print(f"Starting Break Song: {music.TITLE}")

                    obs.connect()
                    obs.refresh_source(CONFIG_V_MAIN_SCREEN)
                    obs.set_music(CONFIG_V_SONG_MEDIA,music.QUEUE)
                    logs.add(music.TITLE,music.ARTIST,music.DURATION,True)
                

                    delay = 60 * CONFIG_BREAK_LENGTH
                    close_time = time() + delay
                    while True:
                        if time() > close_time:
                            obs.set_music(CONFIG_V_SONG_MEDIA,"")
                            break

                    counter += 1

                else:
                    print(f"Switching To Promo Video ...")
                    logs.flush()
                    get_promo_lists = shuffle_my_list(get_dir_list(CONFIG_PROMO_FOLDER),True)
                    music.set_promo_video(random_choice(get_promo_lists))
                    obs.connect()
                    obs.set_music(CONFIG_V_VIDEO_MEDIA,music.PROMO)       
                    music.generate_image_url()
                    db.connect()
                    music.set_current_song_settings(db.get_first_music())
                    db.disconnect()
                    music.set_music_html()
                    obs.connect()
                    obs.refresh_source(CONFIG_V_MAIN_SCREEN)
                    exited_from_promo = True
                    while obs.get_music_state(CONFIG_V_VIDEO_MEDIA)["mediaState"] == "playing":
                        pass
            else:
                print(f"Songs Finished - Starting to reAdding the songs !")
                db.connect()
                for song in shuffle_my_list(get_dir_list(CONFIG_SONG_FOLDER),CONFIG_ENABLE_MUSIC_SHUFFLE):
                    db.add_music(music.get_music_info(song))
                db.commit()
                musicCounter = int(db.count_rows())
                counter = 0
                db.disconnect()
    except:
        print(f"Script exited !")
