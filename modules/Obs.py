import obswebsocket


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
