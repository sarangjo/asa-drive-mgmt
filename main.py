import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

ASA_DRIVE_ID = "0ANxIVFZCT5MfUk9PVA"


class DriveHelper:
    def __init__(self):
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def run(self):
        service = build('drive', 'v3', credentials=self.creds)

        # Call the Drive v3 API
        query = "name = 'Circuit Archive'"

        results = service.files().list(q=query, corpora="drive", driveId=ASA_DRIVE_ID,
                                       includeItemsFromAllDrives=True, supportsAllDrives=True,
                                       fields="items(name,parents)").execute()
        items = results.get('files', [])

        if not items:
            print('Nothing found.')
        else:
            print('Items:')
            for item in items:
                print(item)


if __name__ == '__main__':
    h = DriveHelper()
    h.run()
