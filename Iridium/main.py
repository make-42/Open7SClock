import os
import subprocess
import requests
import json
import time
import cherrypy
import json


defplayer = "rhythmbox"#"plasma-browser-integration"

def runcommand(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
class StringGenerator(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        status = runcommand("playerctl status")
        volume = runcommand("playerctl volume")
        album = runcommand("playerctl metadata xesam:album")
        artist = runcommand("playerctl metadata xesam:artist")
        title = runcommand("playerctl metadata xesam:title")
        try:
            duration = float(runcommand("playerctl metadata mpris:length"))/1000000
            position = float(runcommand("playerctl position"))
        except:
            duration = 0
            position = 0
        payload = {"status":status,"volume":volume,"album":album,"artist":artist,"title":title,"duration":duration,"position":position}
        return json.dumps(payload)


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0','server.socket_port': 4215,})
    conf = {
        '/': {
            'tools.sessions.on': True
        }
    }

    cherrypy.quickstart(StringGenerator(), '/', conf)
