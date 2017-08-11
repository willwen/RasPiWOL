import tornado.ioloop
import tornado.web
import RPi.GPIO as GPIO
import time

isPoweredOn = False
class HandleToggle(tornado.web.RequestHandler):
    def post(self):
        global isPoweredOn
	body = tornado.escape.json_decode(self.request.body)
        passPhrase = body['passphrase']
	#print(passPhrase)
        if(passPhrase == '0xffff'):
            GPIO.output(3, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(3, GPIO.LOW)
            response = {'status' : 'ok'}
            isPoweredOn = not isPoweredOn;
        else:
            response = {'status' : 'bad password'}
        self.write(response)
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
    GPIO.setup(3,GPIO.OUT)
    GPIO.output(3, GPIO.LOW)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()