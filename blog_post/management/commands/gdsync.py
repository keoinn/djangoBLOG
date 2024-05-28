from typing import Any
from django.core.management.base import BaseCommand, CommandError
from djangoBLOG.settings import BASE_DIR
import tomllib, os.path, datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    
    def getLoggerMsgWithTime(self, msg):
        return '[{}] {}'.format(datetime.datetime.now().replace(microsecond=0), msg)
    
    def findTargetInDrive(self, searcher = None, file_id = None, target_title = None):
        get_target = None
        
        if target_title == None or file_id == None or searcher == None:
            return None
        
        if file_id == 'root':
            query_str = "'root' in parents and trashed=false"
        else:
            query_str = "\'" + file_id + "\'" + " in parents and trashed=false"
        
        file_list = searcher.ListFile({'q': query_str}).GetList()
        
        if len(file_list) == 0:
            return None
        
        for file_info in file_list:
            if(file_info['title'] == target_title):
                get_target = file_info['id']
        
        return get_target
 
    def uploadFileToDrive(self, uploader = None, file_id = None, file_name = None, drive_folder_id = None, local_file_path = None):
        if file_name == None or drive_folder_id == None or local_file_path == None:
            self.stdout.write(self.style.ERROR(self.getLoggerMsgWithTime('Wrong parameter in uploading file, SyncProcess is stop.')))
            return False
        
        if os.path.exists(local_file_path) == False:
            self.stdout.write(self.style.ERROR(self.getLoggerMsgWithTime('{} is not found in path: {}'.format(file_name, local_file_path))))
            return False
        
        if file_id == None:
            self.stdout.write(self.style.WARNING(self.getLoggerMsgWithTime('{} is not exist in drive, then SyncProcess created and upload to driver.'.format(file_name))))
            update_file = uploader.CreateFile({'parents' : [{'id' : drive_folder_id}], 'title' : file_name})
        else:
            self.stdout.write(self.style.SUCCESS(self.getLoggerMsgWithTime('SyncProcess update file: {} in driver.'.format(file_name))))
            update_file = uploader.CreateFile({'id': file_id})
        update_file.SetContentFile(local_file_path)
        update_file.Upload()   
        
    def handle(self, *args: Any, **options: Any) -> str | None:
        
        # loading config (path: APP/management/commands/gd_filepath.toml)
        with open(BASE_DIR / 'blog_post/management/commands/gd_filepath.toml', "rb") as f:
            config = tomllib.load(f)
            
        gauth = GoogleAuth(settings_file= BASE_DIR / 'blog_post/management/commands/client_screct.yaml')
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        # query_folder_ids
        for config_item in config['gd_dest']:
            idx = config['gd_dest'].index(config_item)
            if config_item['order'] == 0:
                config_item['id'] = self.findTargetInDrive(drive, 'root', config_item['name'])  
            else:
                config_item['id'] = self.findTargetInDrive(drive, config['gd_dest'][idx-1]['id'], config_item['name'])  

        # query_files_ids
        for config_item in config['sync_files']:
            deepest_folder_id = config['gd_dest'][len(config['gd_dest'])-1]['id']
            config_item['id'] = self.findTargetInDrive(drive, deepest_folder_id, config_item['name'])
            
            # upload files
            self.uploadFileToDrive(drive, config_item['id'], config_item['name'], deepest_folder_id, BASE_DIR / config_item['path'])
        
        self.stdout.write(self.style.SUCCESS(self.getLoggerMsgWithTime('Finish SyncProceess: Backup database and files.')))
        
        