import pickle
from os import path
from ctypes import Structure, windll, c_uint, sizeof, byref
import time

import schedule

from rm_sync import get_files_from_zotero_storage
from rm_sync import sync
from config import config

'''
Checks every 5 minutes if changes are made to the zotero storage
if a change is detected:
    wait until user is idle for 5 minutes
    then run sync
    update current file_log
'''
CONFIG = config()

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]


def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

def wait_for_idle(n_seconds, wait_interval):
    while get_idle_duration() < n_seconds:
        print('Idle: {}'.format(get_idle_duration()))
        time.sleep(wait_interval)

def check():
    file_log_name = './file_log.pkl'
    zotero_path = CONFIG['path_to_local_zotero_storage']
    zotero_pdfs = [file.stem for file in get_files_from_zotero_storage(zotero_path)]
    
    if path.exists(file_log_name):
        with open(file_log_name, 'rb') as f:
            logged_pdfs = pickle.load(f)
        start_sync = True if not zotero_pdfs == logged_pdfs else False
    else:
        start_sync = True

    if start_sync:
        wait_for_idle(CONFIG['wait_for_n_seconds_idle'], 1)
        sync()

        with open(file_log_name, 'wb') as f:
            pickle.dump(zotero_pdfs, f)
    

def monitor():
    schedule.every(CONFIG['check_log_every_n_minutes']).minutes.do(check)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    monitor()