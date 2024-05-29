from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from djangoBLOG.settings import BASE_DIR, GCP_API_CONSOLE_ID, GCP_API_CONSOLE_SECRET, GCP_API_CONSOLE_APP_PATH, GCP_API_CONSOLE_CLIENT_SCRECT_FILENAME


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--gen-cert",
            action='store_true'
        )
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        
        if options['gen_cert']:
            print('--gen-cert Option Start.')
            client_screct_path = BASE_DIR / (GCP_API_CONSOLE_APP_PATH + GCP_API_CONSOLE_CLIENT_SCRECT_FILENAME)
            f = open(client_screct_path, "w")
            f.write("client_config_backend: settings\n")
            f.write("client_config:\n")
            f.write("  client_id: {}\n".format(GCP_API_CONSOLE_ID))
            f.write("  client_secret: {}\n".format(GCP_API_CONSOLE_SECRET))
            f.write("save_credentials: True\n")
            f.write("save_credentials_backend: file\n")
            f.write("save_credentials_file: credentials.json\n")
            f.write("get_refresh_token: True\n")
            f.write("\n")
            f.write("oauth_scope:\n")
            f.write("  - https://www.googleapis.com/auth/drive.file\n")
            f.write("  - https://www.googleapis.com/auth/drive.install\n")
            f.write("  - https://www.googleapis.com/auth/drive.metadata\n")
            f.close()
            
        else: 
            print("Default Action")