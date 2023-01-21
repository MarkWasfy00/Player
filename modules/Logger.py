import csv
from time import gmtime, strftime
import os
from datetime import date

def get_time():
    return strftime("%H:%M:%S", gmtime())


class Logger:
    LIST = []

    def __init__(self,config_log_folder,rounds=8):
        self.STATION = rounds
        self.PROMO = rounds + 1
        self.CONFIG_LOG_FOLDER = config_log_folder
            

    def add(self,song_name,artist_name,duration,played_at_comm=False):
        try:
            date_file_name = str(date.today()) + ".csv"
            if not os.path.isfile(os.path.join(self.CONFIG_LOG_FOLDER,date_file_name)):
                with open(os.path.join(self.CONFIG_LOG_FOLDER,date_file_name), 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Title", "Artist", "Start Time Played","Play Length","Played at commercial"])

            self.LIST.append(song_name)
        
            with open(os.path.join(self.CONFIG_LOG_FOLDER,date_file_name),"a", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([f"{song_name}".replace(",", "-"), f"{artist_name}".replace(",", "-"), f"{get_time()}",f"{duration}",f"{played_at_comm}"])
        except:
            print(f"Failed to Add")

    def count(self):
        return len(self.LIST)

    def flush(self):
         self.LIST = []
