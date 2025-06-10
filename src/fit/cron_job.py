import requests
import time
import os

# Configuration
MONOLITH_URL = os.getenv("MONOLITH_URL", "http://localhost:5000")
WOD_ENDPOINT = f"{MONOLITH_URL}/users/generateWods"
INTERVAL_SECONDS = 3600  # Every hour (change as needed)

def run_cron_job():
    while True:
        try:
            print(f"⏰ Triggering WOD generation at {WOD_ENDPOINT}")
            response = requests.post(WOD_ENDPOINT)
            if response.status_code == 202:
                print(f"✅ WOD generation triggered successfully! Response: {response.json()}")
            else:
                print(f"❌ Failed to trigger WOD generation! Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"⚠️ Error triggering WOD generation: {str(e)}")
        
        print(f"⏳ Waiting for {INTERVAL_SECONDS} seconds before the next run...")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run_cron_job()
