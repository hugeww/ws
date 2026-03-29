#!/usr/bin/env python3
import os,sys,socket,struct,hashlib,base64,threading
from http.server import HTTPServer,BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
A=os.environ.get('UUID','7bd180e8-1142-4387-93f5-03e8d750a896')
B=os.environ.get('DOMAIN','')
C=os.environ.get('SUB_PATH','sub')
D=os.environ.get('NAME','')
E=os.environ.get('WSPATH',A[:8])
F=int(os.environ.get('PORT')or os.environ.get('SERVER_PORT')or 8080)
G=os.environ.get('DEBUG','').lower()=='true'
H=B or'your-domain.com'
I=443
J='tls'if B else'none'
K='Unknown'
L=['speedtest.net','fast.com','librespeed.org']
def M(N):
 if not N:return False
 O=N.lower()
 return any(O==P or O.endswith('.'+P)for P in L)
def Q(R):
 try:socket.inet_aton(R);return R
 except:pass
 try:return socket.gethostbyname(R)
 except:return R
class S(BaseHTTPRequestHandler):
 def log_message(self,format,*args):
  if G:print(f"[{self.log_date_time_string()}]{format%args}")
 def do_GET(self):
  if self.path=='/':
   self.send_response(200)
   self.send_header('Content-type','text/html')
   self.end_headers()
   self.wfile.write(b'<!DOCTYPE html><html><head><title>WS</title></head><body><h1>Proxy</h1></body></html>')
  elif f'/{C}'in self.path:
   self.send_response(200)
   self.send_header('Content-type','text/plain')
   self.end_headers()
   T=D or K
   U=f"vless://{A}@{H}:{I}?encryption=none&security={J}&sni={H}&fp=chrome&type=ws&host={H}&path=%2F{E}#{T}"
   V=f"trojan://{A}@{H}:{I}?security={J}&sni={H}&fp=chrome&type=ws&host={H}&path=%2F{E}#{T}"
   W=base64.b64encode(f"none:{A}".encode()).decode()
   X='tls;'if J=='tls'else''
   Y=f"ss://{W}@{H}:{I}?plugin=v2ray-plugin;mode%3Dwebsocket;host%3D{H};path%3D%2F{E};{X}sni%3D{H};skip-cert-verify%3Dtrue;mux%3D0#{T}"
   Z=f"{U}\n{V}\n{Y}"
   self.wfile.write((base64.b64encode(Z.encode()).decode()+'\n').encode())
  else:
   self.send_response(404)
   self.end_headers()
   self.wfile.write(b'Not Found')
 def do_POST(self):self.do_GET()
class T(ThreadingMixIn,HTTPServer):daemon_threads=True
def run():
 global H,I,J
 if not B:H='your-domain.com';J='none';I=F
 else:H=B;J='tls';I=443
 S1=T(('0.0.0.0',F),S)
 print(f"Port:{F}");print(f"Path:/{E}");print(f"Sub:/{C}");print(f"Domain:{H}")
 try:S1.serve_forever()
 except KeyboardInterrupt:print("\nStop")
if __name__=='__main__':run()
