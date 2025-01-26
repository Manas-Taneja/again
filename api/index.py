import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Load student marks
        with open(os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json'), 'r') as f:
            student_marks = json.load(f)
        
        # Parse query parameters
        parsed_path = urlparse(self.path)
        names = parse_qs(parsed_path.query).get('name', [])
        
        # Get marks for requested names
        marks = [student_marks.get(name, None) for name in names]
        
        # Remove None values
        marks = [mark for mark in marks if mark is not None]
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps({"marks": marks})
        self.wfile.write(response.encode())