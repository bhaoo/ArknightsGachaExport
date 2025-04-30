import json
import os

def find_default_uid(data):
    for app in data.get("data", {}).get("list", []):
        for binding in app.get("bindingList", []):
            if binding.get("isDefault") is True:
                return binding.get("uid")
    return None

def transform_records(raw_list):
    transformed = {}

    for record in raw_list:
        gacha_ts = str(int(record["gachaTs"]) // 1000)
        char_name = record["charName"]
        rarity = record["rarity"]
        is_new = 1 if record["isNew"] else 0
        pool_name = record["poolName"]

        if gacha_ts not in transformed:
            transformed[gacha_ts] = {
                "c": [],
                "p": pool_name
            }

        transformed[gacha_ts]["c"].append([char_name, rarity, is_new])

    return transformed

def merge_gacha_records(uid, new_records, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{uid}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    new_count = 0
    for ts, info in new_records.items():
        if ts not in existing_data:
            existing_data[ts] = info
            new_count += 1

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"[UID#{uid}] Merge {new_count} records.")