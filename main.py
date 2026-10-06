import os
import subprocess
import requests
import tarfile

def download_and_run_hemi():
    # تحميل الإصدار الرسمي الأحدث والمستقر لعقدة Hemi
    version = "v0.4.3"
    url = f"https://github.com{version}/heminetwork_{version}_linux_amd64.tar.gz"
    archive = "hemi.tar.gz"
    
    print("🤖 Downloading official Hemi PoP Miner archive...")
    response = requests.get(url, stream=True)
    with open(archive, "wb") as f:
        f.write(response.content)
        
    print("📦 Extracting official node files...")
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall()
        
    # الانتقال إلى مجلد العقدة المستخرج
    folder_name = f"heminetwork_{version}_linux_amd64"
    os.chdir(folder_name)
    
    # قراءة المفتاح الخاص الآمن من إعدادات Render
    private_key = os.environ.get("HEMI_PRIVATE_KEY")
    if not private_key:
        print("❌ Error: HEMI_PRIVATE_KEY environment variable is missing!")
        return

    print("🚀 Booting Hemi PoP Miner on Cloud Network...")
    cmd = "./popmd"
    
    # تهيئة بيئة الاتصال المباشر بالسيرفر بدون بروكسيات وهمية
    env = os.environ.copy()
    env["POPMD_PRIVATE_KEY"] = private_key
    env["POPMD_STATIC_PEERS"] = "/dns4/popm.testnet.hemi.network/tcp/443/wss"
    
    # تشغيل العقدة الرسمية بالخلفية وطباعة السجلات أولاً بأول
    process = subprocess.Popen(cmd, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(line, end="")

if __name__ == "__main__":
    download_and_run_hemi()
