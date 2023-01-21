from os import path
from bs4 import BeautifulSoup
import os
import eyed3
import time


class Music:
    
    def __init__(self,songs_folder,album_art_folder,promo_folder,grad_from,grad_to,angle):
        self.QUEUE = "#"
        self.TITLE = "#"
        self.ARTIST = "#"
        self.ART = "#"
        self.DURATION_MS = "#"
        self.PROMO = "#"

        self.DURATION = "#"
        self.NEXT_TITLE = "#"
        self.NEXT_ARTIST = "#"

        self.ALBUM_ART_FOLDER_NAME = album_art_folder
        self.ALBUM_ART_PATH = path.join(os.getcwd(),f"{album_art_folder}")
        self.SONGS_PATH = path.join(os.getcwd(),f"{songs_folder}")
        self.PROMO_PATH = path.join(os.getcwd(),f"{promo_folder}")
        self.GRAD_FROM = grad_from
        self.GRAD_TO = grad_to
        self.GRAD_ANGLE = angle

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
            print(f"Failed to fetch the current song art")

    def set_current_song_settings(self,song_intry):
        try:
            audiofile = eyed3.load(path.join(self.SONGS_PATH,song_intry))
            self.QUEUE = path.join(self.SONGS_PATH,song_intry)
            self.TITLE  = audiofile.tag.title
            self.ARTIST = audiofile.tag.artist
            self.DURATION = time.strftime("%M:%S", time.gmtime(audiofile.info.time_secs))
            self.DURATION_MS = audiofile.info.time_secs * 1000
            if not os.path.isfile(path.join(self.ALBUM_ART_PATH,'{0}.jpg'.format(audiofile.tag.title))):
                self.ART = f"../placeholder/Placeholder.jpg"
            else:
                self.ART = f"../{self.ALBUM_ART_FOLDER_NAME}/{'{0}.jpg'.format(audiofile.tag.title)}"

        except:
            print(f"Failed to set the current song")

    def set_music_html(self):
        try:
            # music.set_files_html("./backUp/indexback.html","./html/index.html")
            with open("./html/index.html", "r") as f:
                doc = BeautifulSoup(f, "html.parser")

            doc.body.attrs["style"] = f"background-image: linear-gradient({self.GRAD_ANGLE}deg, {self.GRAD_FROM} , {self.GRAD_TO} );"

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
            print(f"Failed to set html file")

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
            print(f"Failed to set html file")

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
            print(f"Failed to set last music")

    def set_files_html(self,file_name,to_path):
        with open(file_name,"r") as f:
            doc = BeautifulSoup(f, "html.parser")

        with open(to_path,"w", encoding="utf-8") as file:
            file.write(str(doc))

    def get_next_music_meta(self,song_intry):
        try:
            audiofile = eyed3.load(path.join(self.SONGS_PATH,song_intry))
            self.NEXT_TITLE  = audiofile.tag.title
            self.NEXT_ARTIST = audiofile.tag.artist
        except:
            print(f"Failed to fetch next song")

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

    def get_music_info(self,p_song_intry):
        try:
            audiofile = eyed3.load(path.join(self.SONGS_PATH,p_song_intry))
            title  = audiofile.tag.title
            artist = audiofile.tag.artist
            duration = time.strftime("%M:%S", time.gmtime(audiofile.info.time_secs))
            return (p_song_intry,title,artist,duration)
        except:
            print(f"Failed to set the current song")