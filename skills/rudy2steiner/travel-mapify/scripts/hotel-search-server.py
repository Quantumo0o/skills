#!/usr/bin/env python3
"""
Simple HTTP server to handle FlyAI hotel search requests
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class HotelSearchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/hotel-search'):
            self.handle_hotel_search()
        else:
            self.send_error(404, "Not Found")
    
    def handle_hotel_search(self):
        try:
            print(f"Received request: {self.path}")
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            destination = query_params.get('destination', [None])[0]  # City name
            poi_name = query_params.get('poi', [None])[0]           # Specific attraction
            checkin_date = query_params.get('checkin', [None])[0]
            checkout_date = query_params.get('checkout', [None])[0]
            
            print(f"Parsed params - destination: {destination}, poi: {poi_name}, checkin: {checkin_date}, checkout: {checkout_date}")
            
            if not destination:
                self.send_error(400, "Missing destination parameter")
                return
            
            # Use provided dates or default to tomorrow + day after tomorrow
            if not checkin_date or not checkout_date:
                today = datetime.now()
                checkin = (today + timedelta(days=1)).strftime('%Y-%m-%d')
                checkout = (today + timedelta(days=3)).strftime('%Y-%m-%d')
            else:
                checkin = checkin_date
                checkout = checkout_date
            
            # Call FlyAI CLI to search for hotels
            cmd = [
                '/Users/xuandu/.nvm/versions/node/v22.22.1/bin/flyai', 'search-hotel',
                '--dest-name', destination,
                '--check-in-date', checkin,
                '--check-out-date', checkout
            ]
            
            # Add POI name if provided
            if poi_name:
                cmd.extend(['--poi-name', poi_name])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Log the raw output for debugging
                print(f"FlyAI stdout length: {len(result.stdout)}")
                print(f"FlyAI stdout preview: {result.stdout[:200]}")
                # Parse JSON output
                try:
                    hotel_data = json.loads(result.stdout)
                    print(f"Parsed hotel_data: {hotel_data.get('data') is not None}")
                    # Return the full response as-is since it already has the correct structure
                    self.send_json_response(hotel_data)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Problematic output: {result.stdout}")
                    self.send_error(500, "Invalid JSON response from FlyAI")
            else:
                error_msg = result.stderr or f"FlyAI command failed with code {result.returncode}"
                print(f"FlyAI command failed: {error_msg}")
                self.send_error(500, f"Hotel search failed: {error_msg}")
                
        except subprocess.TimeoutExpired:
            self.send_error(500, "Hotel search timed out")
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_response = {'error': message}
        self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 hotel-search-server.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    server = HTTPServer(('localhost', port), HotelSearchHandler)
    print(f"Hotel search server running on http://localhost:{port}")
    server.serve_forever()

if __name__ == '__main__':
    main()