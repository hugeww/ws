#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VLESS/Trojan/Shadowsocks WebSocket Proxy
使用标准库，无需额外依赖
"""

import os
import sys
import socket
import struct
import hashlib
import base64
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# ============== 配置 ==============
UUID = os.environ.get('UUID', '7bd180e8-1142-4387-93f5-03e8d750a896')
DOMAIN = os.environ.get('DOMAIN', '')
SUB_PATH = os.environ.get('SUB_PATH', 'sub')
NAME = os.environ.get('NAME', '')
WSPATH = os.environ.get('WSPATH', UUID[:8])
PORT = int(os.environ.get('PORT') or os.environ.get('SERVER_PORT') or 8080)
DEBUG = os.environ.get('DEBUG', '').lower() == 'true'

# ============== 全局变量 ==============
CurrentDomain = DOMAIN or 'your-domain.com'
CurrentPort = 443
Tls = 'tls' if DOMAIN else 'none'
ISP = 'Unknown'

# 屏蔽的测速域名
BLOCKED_DOMAINS = ['speedtest.net', 'fast.com', 'librespeed.org']


def is_blocked_domain(host):
    if not host:
        return False
    host_lower = host.lower()
    return any(host_lower == b or host_lower.endswith('.' + b) for b in BLOCKED_DOMAINS)


def resolve_host(host):
    """简单 DNS 解析"""
    try:
        socket.inet_aton(host)
        return host
    except:
        pass
    try:
        return socket.gethostbyname(host)
    except:
        return host


class ProxyHandler(BaseHTTPRequestHandler):
    """HTTP 处理"""
    
    def log_message(self, format, *args):
        if DEBUG:
            print(f"[{self.log_date_time_string()}] {format % args}")
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = b'''<!DOCTYPE html>
<html><head><title>Python WS Proxy</title></head>
<body><h1>Python WS Proxy</h1>
<p>VLESS + Trojan + Shadowsocks</p>
<p>Subscription: /sub</p>
</body></html>'''
            self.wfile.write(response)
        
        elif f'/{SUB_PATH}' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            name_part = NAME or ISP
            
            vless_url = f"vless://{UUID}@{CurrentDomain}:{CurrentPort}?encryption=none&security={Tls}&sni={CurrentDomain}&fp=chrome&type=ws&host={CurrentDomain}&path=%2F{WSPATH}#{name_part}"
            trojan_url = f"trojan://{UUID}@{CurrentDomain}:{CurrentPort}?security={Tls}&sni={CurrentDomain}&fp=chrome&type=ws&host={CurrentDomain}&path=%2F{WSPATH}#{name_part}"
            
            ss_method_password = base64.b64encode(f"none:{UUID}".encode()).decode()
            ss_tls = 'tls;' if Tls == 'tls' else ''
            ss_url = f"ss://{ss_method_password}@{CurrentDomain}:{CurrentPort}?plugin=v2ray-plugin;mode%3Dwebsocket;host%3D{CurrentDomain};path%3D%2F{WSPATH};{ss_tls}sni%3D{CurrentDomain};skip-cert-verify%3Dtrue;mux%3D0#{name_part}"
            
            subscription = f"{vless_url}\n{trojan_url}\n{ss_url}"
            base64_content = base64.b64encode(subscription.encode()).decode()
            
            self.wfile.write((base64_content + '\n').encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        self.do_GET()


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """多线程 HTTP 服务器"""
    daemon_threads = True


def run_server():
    global CurrentDomain, CurrentPort, Tls
    
    # 设置域名
    if not DOMAIN:
        CurrentDomain = 'your-domain.com'
        Tls = 'none'
        CurrentPort = PORT
    else:
        CurrentDomain = DOMAIN
        Tls = 'tls'
        CurrentPort = 443
    
    server = ThreadingHTTPServer(('0.0.0.0', PORT), ProxyHandler)
    print(f"Server running on port {PORT}")
    print(f"WebSocket path: /{WSPATH}")
    print(f"Subscription: /{SUB_PATH}")
    print(f"Domain: {CurrentDomain}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == '__main__':
    run_server()
