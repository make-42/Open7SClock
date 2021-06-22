import cherrypy
import json

class StringGenerator(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        savefile = open('file.txt', 'r+')
        data = savefile.read()
        savefile.close()
        return data

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def update(self):
        rawbody = str(cherrypy.request.json)
        print(rawbody)
        body = json.loads(rawbody)
        savefile = open('file.txt', 'w')
        savefile.write(str(body))
        savefile.close()
        return "done"


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '127.0.0.1','server.socket_port': 4215,})
    conf = {
        '/': {
            'tools.sessions.on': True
        }
    }

    cherrypy.quickstart(StringGenerator(), '/', conf)
