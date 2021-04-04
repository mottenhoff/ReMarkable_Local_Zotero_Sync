def config():
    return {
        # Zotero
        "path_to_local_zotero_storage": "<path to your local zotero storage>",
        
        # ReMarkable
        # Get authentication code from https://my.remarkable.com/connect/desktop)
        #   The auth code is only necessary the first run, you can remove the
        #   code afterwards.
        "reMarkable_auth_code": "",

        # Monitor
        "check_log_every_n_minutes": 5,
        "wait_for_n_seconds_idle": 60
    }