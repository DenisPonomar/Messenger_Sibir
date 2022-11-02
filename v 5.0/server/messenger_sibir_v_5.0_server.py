import time
import http.server
from io import BytesIO
import hashlib
import os
import base64
hostName = ""
serverPort = 15421 #You can choose any available port; by default, it is 8000
class MyServer(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        pass
    def do_GET(self): #the do_GET method is inherited from BaseHTTPRequestHandler
        zapros = self.requestline.split()[1][1:].split("!")
        try:
            if zapros[0] == "a":
                token_otpravitel = zapros[1]
                hash_token_otpravitel = hashlib.sha256(token_otpravitel.encode("utf-8")).hexdigest()
                if os.path.isdir(hash_token_otpravitel):
                    papka = os.listdir(hash_token_otpravitel)
                    otpravka = False
                    if len(papka) > 0:
                        for i in range(len(papka)):
                            pod_papka = os.listdir(str(hash_token_otpravitel+"/"+papka[i]))
                            if len(pod_papka) == 0:
                                continue
                            else:
                                f = open(str(hash_token_otpravitel+"/"+papka[i]+"/"+pod_papka[0]), 'r')
                                soob = str(f.read())
                                f.close()
                                self.send_response(200)
                                self.send_header("Content-type", "text/html;charset=utf-8")
                                self.end_headers()
                                self.wfile.write((papka[i]+"!"+pod_papka[0]+"!"+soob).encode("utf-8"))
                                os.remove(str(hash_token_otpravitel+"/"+papka[i]+"/"+pod_papka[0]))
                                otpravka = True
                                break
                        if otpravka == False:
                            self.send_response(404)
                            self.send_header("Content-type", "text/html;charset=utf-8")
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.send_header("Content-type", "text/html;charset=utf-8")
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html;charset=utf-8")
                    self.end_headers()
            if zapros[0] == "b":
                server_time = time.time()
                token_otpravitel = zapros[1]
                hash_token_otpravitel = hashlib.sha256(token_otpravitel.encode("utf-8")).hexdigest()
                hash_token_poluchatel = zapros[2]
                soob_otpravitel = zapros[3][:12000]
                #text = base64.b64decode(soob_otpravitel[2:].encode("utf-8")).decode("utf-8")
                
                if not os.path.isdir(hash_token_poluchatel):
                    os.mkdir(hash_token_poluchatel)
                if not os.path.isdir(str(hash_token_poluchatel+"/"+hash_token_otpravitel)):
                    os.mkdir(str(hash_token_poluchatel+"/"+hash_token_otpravitel))
                f = open(str(hash_token_poluchatel+"/"+str(hash_token_otpravitel)+"/"+str(server_time)), 'w')
                f.write(soob_otpravitel)
                f.close()
                
                self.send_response(200)
                self.send_header("Content-type", "text/html;charset=utf-8")
                self.end_headers()
                self.wfile.write(str(server_time).encode("utf-8"))
            else:
                pass
        except Exception:
            self.send_response(500)
            self.send_header("Content-type", "text/html;charset=utf-8")
            self.end_headers()
if __name__ == "__main__":        
  webServer = http.server.ThreadingHTTPServer((hostName, serverPort), MyServer)
  print("Server started http://%s:%s" % (hostName, serverPort))  #Server starts
try:
          webServer.serve_forever()
except KeyboardInterrupt:
	pass
webServer.server_close()  #Executes when you hit a keyboard interrupt, closing the server
print("Server stopped")
