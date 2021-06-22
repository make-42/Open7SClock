import os
import subprocess
import requests
import json
import time
import cherrypy
import json


player = "rhythmbox"#"plasma-browser-integration"

def runcommand(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")

class StringGenerator(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        status = runcommand("playerctl status -p "+player)
        volume = runcommand("playerctl volume -p "+player)
        album = runcommand("playerctl metadata xesam:album -p "+player)
        artist = runcommand("playerctl metadata xesam:artist -p "+player)
        title = runcommand("playerctl metadata xesam:title -p "+player)
        duration = float(runcommand("playerctl metadata mpris:length -p "+player))/1000000
        position = float(runcommand("playerctl position -p "+player))

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
