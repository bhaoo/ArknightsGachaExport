import json
import os
import paramiko
import yaml

def load_config():
    with open('config.yml', 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

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


def upload_folder_via_sftp():
    print("Running data upload task...")

    config = load_config()
    sftp_cfg = config["sftp"]
    remote_folder = sftp_cfg["remote_dir"]
    hostname = sftp_cfg["host"]
    port = sftp_cfg.get("port", 22)
    username = sftp_cfg["username"]
    private_key_path=os.path.expanduser(sftp_cfg["private_key"])

    key = paramiko.RSAKey.from_private_key_file(private_key_path)

    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, pkey=key)
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        try:
            sftp.chdir(remote_folder)
        except IOError:
            print(f"Remote directory not found. Creating: {remote_folder}.")
            sftp.mkdir(remote_folder)
            sftp.chdir(remote_folder)

        local_dir = "./data"
        for filename in os.listdir(local_dir):
            local_path = os.path.join(local_dir, filename)
            remote_path = f"{remote_folder.rstrip('/')}/{filename}"

            if os.path.isfile(local_path):
                print(f"Uploading: {filename}")
                sftp.put(local_path, remote_path)

        print("All files uploaded completed.")
    finally:
        sftp.close()
        transport.close()