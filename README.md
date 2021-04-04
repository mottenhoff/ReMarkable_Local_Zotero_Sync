# ReMarkable Local Zotero sync
Syncs your local Zotero storage to the ReMarkable Cloud service. Includes `.vbs` script to run autosync in the background.  

The script finds all PDF files in your local Zotero storage and mirrors them with a folder on the reMarkable Cloud.  

It will:
* Upload files that are in the Zotero Storage and not on the reMarkable Cloud  
* Remove files from reMarkable cloud that are not in your Zotero Storage (anymore)  

Note: items in Zotero trash are still included in the Zotero storage, so empty trash to remove from the ReMarkable Cloud.  

## Installation
Download the files and copy them to any folder.  
`pip install -r requirements.txt`  

Tested for Python 3.9.2 and a ReMarkable 2

## Setup
Edit condig.py and add:
* The path to your local zotero storage, which is at something like `C:/Users/<your_username>/Zotero/storage`
* The path to the folder on the Remarkable to sync with
* The authentication code which you need to register at my.remarkable.com/connect/desktop

Then run `python rm_sync.py`  
The authentication code is only necessary the first run, so you can remove the code from the config afterwards.  

## Usage
For manual single sync: `python rm_sync`  

**Check periodically for updates:**  
To run visibly: `python update_monitor.py`  
To run invisible: `pythonw update_monitor.py`  

**To start autosync in the background at startup:**  
Edit `launcher.vbs` and add the path to your `pythonw.exe` interpreter and the path to `update_monitor.py`  
Then press `windows + R` and got to `shell:startup`. Copy a shortcut to `launcher.vbs` into the startup folder.


### TODO
* Sync Zotero collection structures
* ...
