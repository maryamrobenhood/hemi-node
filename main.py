import os
import subprocess
import urllib.request
import tarfile
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# سيرفر ويب وهمي بالخلفية لخدعة Render ومنع خطأ الـ Port Scan
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"🤖 Web Hook activated on port {port}")
    server.serve_forever()

def download_and_run_hemi():
    archive = "hemi.tar.gz"
    host = "https://github.com"
    path = "/hemilabs/heminetwork/releases/download/v0.4.3/heminetwork_v0.4.3_linux_amd64.tar.gz"
    full_url = host + path
    
    print("🤖 Automated Miner -> Downloading Hemi Node...")
    try:
        urllib.request.urlretrieve(full_url, archive)
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        return
        
    print("📦 Automated Miner -> Extracting official node files...")
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall()
        
    os.chdir("heminetwork_v0.4.3_linux_amd64")
    
    private_key = os.environ.get("HEMI_PRIVATE_KEY")
    btc_key = os.environ.get("POPM_BTC_PRIVKEY", "")
    
    if not private_key or not btc_key:
        print("❌ Error: Private Keys are missing!")
        return

    print("🚀 Booting Hemi PoP Miner on Cloud Network...")
    cmd = "./popmd"
    
    env = os.environ.copy()
    env["POPMD_PRIVATE_KEY"] = private_key
    env["POPMD_BTC_PRIVKEY"] = btc_key.strip().lower()
    env["POPMD_STATIC_PEERS"] = "/dns4/popm.testnet.hemi.network/tcp/443/wss"
    
    process = subprocess.Popen(cmd, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(line, end="")

if __name__ == "__main__":
    # تشغيل سيرفر الويب الوهمي في مسار منفصل لمنع خطأ الـ Timeout
    threading.Thread(target=run_dummy_server, daemon=True).start()
    download_and_run_hemi()
