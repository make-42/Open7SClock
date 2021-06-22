import os
import subprocess
import requests
import json
import time

clockip = "http://192.168.1.51:4215/update" #192.168.1.51:4215/post

player = "rhythmbox"#"plasma-browser-integration"
last = ""
def runcommand(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
while 1:
    status = runcommand("playerctl status -p "+player)
    volume = runcommand("playerctl volume -p "+player)
    album = runcommand("playerctl metadata xesam:album -p "+player)
    artist = runcommand("playerctl metadata xesam:artist -p "+player)
    title = runcommand("playerctl metadata xesam:title -p "+player)
    duration = float(runcommand("playerctl metadata mpris:length -p "+player))/1000000
    position = float(runcommand("playerctl position -p "+player))

    payload = {"status":status,"volume":volume,"album":album,"artist":artist,"title":title,"duration":duration,"position":position}
    try:
        if artist+title != last:
            r = requests.post(clockip,json=json.dumps(payload),headers={"Content-Type":"application/json"})
            last = artist+title
    except:
        pass
    time.sleep(2)
