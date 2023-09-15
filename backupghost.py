import requests
import os
import json
from datetime import datetime
import glob
import argparse
import sys

def get_ghost_session(GHOST_URL, API_VERSION, USERNAME, PASSWORD):
    session = requests.Session()

    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    headers = {
        "Origin": GHOST_URL,
        "Accept-Version": API_VERSION,
        "Content-Type": "application/json"
    }

    # Create a session and store the cookie
    session.post(f"{GHOST_URL}/ghost/api/admin/session/", json=login_data, headers=headers)
    return session

def get_ghost_data(session, GHOST_URL, API_VERSION, LOCATION, RETENTION):
    headers = {
        "Accept-Version": API_VERSION,
        "Origin": GHOST_URL
    }

    # Use the session cookie to access the API
    response = session.get(f"{GHOST_URL}/ghost/api/admin/db/", headers=headers)
    if response.status_code != 200:
        print("Ghost website seems to be down or not reachable!")
        sys.exit(1)
    else:
        save_backup(response.json(), LOCATION, RETENTION)

def save_backup(data, LOCATION, RETENTION):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{LOCATION}/ghost_backup_{timestamp}.json"

    with open(filename, 'w') as file:
        json.dump(data, file)

    cleanup_backups(RETENTION)

def cleanup_backups(RETENTION):
    # Clean old backups
    if RETENTION != 0:
        backups = sorted(glob.glob("/mnt/disk2/FAHMEDBACKUP/ghost_backup_*.json"), reverse=True)

        for backup in backups[int(RETENTION):]:
            os.remove(backup)

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description='Ghost CMS backup script.')
    parser.add_argument('--ghost-url', required=True, help='URL of the Ghost CMS.')
    parser.add_argument('--api-version', required=True, help='API version.')
    parser.add_argument('--username', required=True, help='Username for Ghost CMS.')
    parser.add_argument('--password', required=True, help='Password for Ghost CMS.')
    parser.add_argument('--location', required=False, default=script_directory, help='Backup location. (default: script directory)')
    parser.add_argument('--retention', required=False, default=0, help='Backup retention in days (default: never.)')

    
    args = parser.parse_args()
    
    session = get_ghost_session(args.ghost_url, args.api_version, args.username, args.password)
    get_ghost_data(session, args.ghost_url, args.api_version, args.location, args.retention)
