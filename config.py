def config():
    return {
        # Zotero
        "path_to_local_zotero_storage": "<path to your local zotero storage>",
        
        # ReMarkable
        # Get authentication code from https://my.remarkable.com/connect/desktop)
        #   The auth code is only necessary the first run, you can remove the
        #   code afterwards.
        "reMarkable_auth_code": "",

        # If you want to sync to a folder called papers at
        # ./papers on your reMarkable. then only "papers" as
        # reMarkable_folder_name
        "reMarkable_folder_name": "",


        # Monitor
        "check_log_every_n_minutes": 5,
        "wait_for_n_seconds_idle": 60
    }