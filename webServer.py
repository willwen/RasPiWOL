import tornado.ioloop
import tornado.web
import RPi.GPIO as GPIO
import time
import hashlib

#Python 2.7+

def getIsPoweredOn():
    if(GPIO.input(7)):
        return True
    return False

class HandleToggle(tornado.web.RequestHandler):
    def post(self):
        try: 
            global isPoweredOn
            isPoweredOn = getIsPoweredOn();
            if(isPoweredOn):
                self.write({'status': 'disabled shutting off computer'})
                return
            body = tornado.escape.json_decode(self.request.body)
            passPhrase = body['passphrase']
            #print(passPhrase)
            if(hashlib.sha256(passPhrase).hexdigest() == "b111e1fa18a72c65d09e75307f0fde21ae29f60193f651106a719285a5e0a91f"):
                GPIO.output(3, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(3, GPIO.LOW)
                response = {'status' : 'ok'}
                isPoweredOn = getIsPoweredOn();
            else:
                response = {'status' : 'bad password'}
            self.write(response)
        except:
            self.write({'status': 'error, check logs.'})
        return

class FindStatus(tornado.web.RequestHandler):
    
    def get(self):
        global isPoweredOn
        if(isPoweredOn):
            self.write("on")
        else:
            self.write("off")
        return
    
class StaticFiles(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path):
        print(url_path)
        if not url_path or url_path.endswith('/'):
            url_path = url_path + 'index.html'
        return url_path
      
def make_app():
    return tornado.web.Application([
        (r'/tryToggle', HandleToggle),
        (r'/getStatus' , FindStatus),
        (r'/(.*)', StaticFiles , {'path': 'webpage/'})
    ])

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(7, GPIO.IN)
    GPIO.output(3, GPIO.LOW)
    isPoweredOn = getIsPoweredOn()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
