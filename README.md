# ghost-cms-exporter
Simple Ghost CMS exporter which can be used to automate DB exports via API

## Prerequisites  
Needs an Ghost CMS user with administrator privileges. 

## Usage  
```
backupghost.py [-h] --ghost-url GHOST_URL --api-version API_VERSION --username USERNAME --password PASSWORD [--location LOCATION] [--retention RETENTION]
```

## Options  
```
  -h, --help            show this help message and exit
  --ghost-url GHOST_URL  URL of the Ghost CMS.
  --api-version API_VERSION API version.
  --username USERNAME   Username for Ghost CMS.
  --password PASSWORD   Password for Ghost CMS.
  --location LOCATION   Backup location. (default: script directory)
  --retention RETENTION Backup retention in days (default: never.)
```