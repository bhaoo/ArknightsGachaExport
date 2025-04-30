from datetime import datetime

import requests
import time
import random

from apscheduler.schedulers.blocking import BlockingScheduler
from utils import *

config = load_config()

def fetch_arknights_data():
    print(f"[{datetime.now()}] Fetching Arknights Data...")

    if config["token"] is None:
        print("[Error] Please provide your Arknights API token.")
        return False

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36",
        "Referer": "https://ak.hypergryph.com/",
    })

    session.get(config["api"]["csrf_url"])

    response = session.post(config["api"]["app_token_url"], json={
        "token": config["token"],
        "appCode": "be36d44aa36bfb5b",
        "type": 1
    })
    app_token = response.json().get("data").get("token")

    response = session.get(config["api"]["binding_list_url"], params={
        "token": app_token,
        "appCode": "arknights",
    })
    uid = find_default_uid(response.json())

    response = session.post(config["api"]["u8_token_url"], json={
        "token": app_token,
        "uid": uid
    })
    u8_token = response.json().get("data").get("token")

    session.post(config["api"]["role_login_url"], json={
        "token": u8_token,
        "source_from": "",
        "share_type": "",
        "share_by": "",
    })

    session.headers.update({
        "X-Role-Token": u8_token,
    })
    params = {
        "uid": uid,
        "category": "normal",
        "size": 50
    }
    all_records = []
    while True:
        response = session.get(config["api"]["gacha_url"], params=params)
        data = response.json()
        list = data["data"]["list"]
        has_more = data["data"]["hasMore"]

        all_records.extend(list)
        print(f"Obtained {len(all_records)} records...")

        if not has_more:
            break

        last_record = list[-1]
        params["gachaTs"] = last_record["gachaTs"]
        params["pos"] = last_record["pos"]

        delay = random.uniform(1, 3)
        print(f"Delay {delay}s...")
        time.sleep(delay)

    merge_gacha_records(uid, transform_records(all_records))

def main():
    fetch_arknights_data()
    if config.get("sftp", {}).get("enabled"):
        upload_folder_via_sftp()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    minutes = config["schedule"]["minute"]
    hours = config["schedule"]["hour"]
    days = config["schedule"]["day"]
    scheduler.add_job(main, 'interval', days=days, hours=hours, minutes=minutes, next_run_time=datetime.now())
    scheduler.start()