#!/usr/bin/env python3
"""
Mock API Server - 快速创建模拟 API 接口
"""
import argparse
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import random
import string

DEFAULT_CONFIG = {
    "port": 3000,
    "host": "0.0.0.0",
    "cors": True,
    "endpoints": [
        {
            "path": "/mock/status",
            "method": "GET",
            "response": {"status": "ok", "timestamp": time.time()},
            "status": 200
        },
        {
            "path": "/mock/echo",
            "method": "POST",
            "response": {"message": "echo", "data": {}},
            "status": 200
        },
        {
            "path": "/mock/random",
            "method": "GET",
            "response": {
                "random_int": 0,
                "random_string": "",
                "random_list": []
            },
            "status": 200
        },
        {
            "path": "/mock/delay/:ms",
            "method": "GET",
            "response": {"delayed": True},
            "status": 200
        },
        {
            "path": "/api/users",
            "method": "GET",
            "response": {
                "users": [
                    {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
                    {"id": 2, "name": "李四", "email": "lisi@example.com"}
                ]
            },
            "status": 200
        },
        {
            "path": "/api/users/:id",
            "method": "GET",
            "response": {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
            "status": 200
        },
        {
            "path": "/api/login",
            "method": "POST",
            "response": {"token": "mock_token_" + ''.join(random.choices(string.ascii_lowercase, k=10)), "expiresIn": 3600},
            "status": 200
        }
    ]
}

class MockAPIHandler(BaseHTTPRequestHandler):
    config = DEFAULT_CONFIG

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_OPTIONS(self):
        self.send_response(200)
        if self.config.get('cors', True):
            self.send_cors_headers()
        self.end_headers()

    def find_endpoint(self, path, method):
        for ep in self.config.get('endpoints', []):
            ep_path = ep['path']
            # 精确匹配
            if ep_path == path and ep.get('method', 'GET').upper() == method.upper():
                return ep
            # 路径参数匹配
            if ':' in ep_path:
                ep_parts = ep_path.split('/')
                req_parts = path.split('/')
                if len(ep_parts) == len(req_parts) and ep.get('method', 'GET').upper() == method.upper():
                    params = {}
                    match = True
                    for i, part in enumerate(ep_parts):
                        if part.startswith(':'):
                            params[part[1:]] = req_parts[i]
                        elif part != req_parts[i]:
                            match = False
                            break
                    if match:
                        ep['_params'] = params
                        return ep
        return None

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_PUT(self):
        self.handle_request('PUT')

    def do_DELETE(self):
        self.handle_request('DELETE')

    def handle_request(self, method):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        ep = self.find_endpoint(path, method)
        
        if not ep:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            if self.config.get('cors', True):
                self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found", "path": path}).encode())
            return

        # 处理延迟
        delay = ep.get('delay', 0)
        if delay > 0:
            time.sleep(delay / 1000)

        # 处理动态响应
        response = ep.get('response', {}).copy()
        
        # 替换路径参数
        if '_params' in ep:
            for k, v in ep['_params'].items():
                if isinstance(response, dict):
                    for key in response:
                        if isinstance(response[key], str):
                            response[key] = response[key].replace(f':{k}', v)

        # 特殊端点处理
        if path == '/mock/random':
            response['random_int'] = random.randint(1, 1000)
            response['random_string'] = ''.join(random.choices(string.ascii_letters, k=10))
            response['random_list'] = [random.randint(1, 100) for _ in range(5)]
        
        if path.startswith('/mock/delay/'):
            ms = int(path.split('/')[-1])
            response = {"delayed_ms": ms, "timestamp": time.time()}

        self.send_response(ep.get('status', 200))
        self.send_header('Content-Type', 'application/json')
        if self.config.get('cors', True):
            self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())

def main():
    parser = argparse.ArgumentParser(description='Mock API Server')
    parser.add_argument('--port', type=int, default=3000, help='服务端口')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='绑定地址')
    parser.add_argument('--config', type=str, help='配置文件路径')
    parser.add_argument('--cors', type=bool, default=True, help='启用CORS')
    args = parser.parse_args()

    config = DEFAULT_CONFIG.copy()
    config['port'] = args.port
    config['host'] = args.host

    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                config.update(user_config)
        except Exception as e:
            print(f"加载配置文件失败: {e}")

    MockAPIHandler.config = config

    server = HTTPServer((config['host'], config['port']), MockAPIHandler)
    print(f"🚀 Mock API Server 启动于 http://{config['host']}:{config['port']}")
    print(f"📋 内置端点:")
    for ep in config.get('endpoints', [])[:5]:
        print(f"   {ep.get('method', 'GET'):6} {ep['path']}")
    print(f"   ... 共 {len(config.get('endpoints', []))} 个端点")
    print(f"🛑 按 Ctrl+C 停止服务")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        server.shutdown()

if __name__ == '__main__':
    main()