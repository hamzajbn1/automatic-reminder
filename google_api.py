import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def create_service(client_secret_file, api_name, api_version, *scopes, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    # In your code: ['https://mail.google.com/'] → full Gmail access.
    SCOPES = [scope for scope in scopes[0]] # SCOPES = list of permissions your app is requesting
    
    creds = None
    working_dir = os.getcwd() 
    token_dir = 'token files'
    token_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json'

    # Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir)) # creates a new folder inside that working directory.

    # Load previously saved Google OAuth login credentials from a JSON file So the user does NOT need to log in again.
    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)

    # The idea: If we don’t have usable credentials, try to fix them automatically.
    # If we can’t fix them, ask the user to log in again.
    # if there is no exist creds or creds is not valid.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        print(e) # "e" is the actual error object.
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        # this line Deletes the saved OAuth token file if it fail.
        os.remove(os.path.join(working_dir, token_dir, token_file))
        return None

r"""
✅"Credentials":
   - object representing OAuth2 credentials (access_token, refresh_token, expiry, scopes).

✅"token_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json'":
   - this line is to combine many variables into one string.
   - Without using f-string, it would look ugly like this:
     'token_' + API_SERVICE_NAME + '_' + API_VERSION + prefix + '.json'
   - this line is to make a unique file name so if we want to update or delete the token file, we can easily find it.
   - "_" is just a separator for readability.
   - example how it will look like: token_drive_v3.json
   - we use .json because OAuth credentials are stored as JSON, it is easy for both humans and programs to read, and
     Google's API libraries expect credentials in JSON format.
    
✅"os.getcwd()":
   - This will get the name of the folder(the folder from which the Python script is RUN).
   Ex:
    - If you run: 
     cd C:\Users\Hamza\gmail_project
     python src/main.py
    - then:
     working_dir = C:\Users\Hamza\gmail_project
    - Even though the file is in:
     C:\Users\Hamza\gmail_project\src\main.py
   - It is like when I open vs code on a specific folder but there are folder inside it and I am working with a file 
     that is specifc/working_on/w.py
     the location that will get will be in specific.

✅"creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)":
   - "creds" will be an object.
   - "Credentials.from_authorized_user_file": it will load the JSON file into memory. The loaded credentials
     include the access token, refresh token, expiry time, and the scopes that were originally granted.
   - If the scopes are incompatible, the credentials are marked invalid (creds.valid == False).
     If the scopes match, the credentials validity depends on whether the access token has expired:
    • Not expired → creds.valid == True
    • Expired → creds.valid == False and creds.expired == True
    If the date is expired the "creds.valid == False" even if the scop matches. 

✅"creds.refresh_token:
            creds.refresh(Request())":
   💳"creds.refresh_token":
      -  It is Issued by Google only once (usually on first login).
      - It will allows your app to ask Google for a new access token.
      - then why we check it: 
        We already logged in before AND Google trusted us enough to give a refresh token.
        Without it Google will NOT issue a new access token automatically that mean users must log in again.
      - The google give us the refresh token because it know that even If it allow us before, the expiary
        date may occur that will cause to envalid it, that we refresh it another time without bothering the
        user.
      - refresh token will only returns in the first login, or in other cases so Silent refresh may not work.
    💳"creds.refresh(Request())":
      - "Request()": An HTTP transport object, Used internally to make HTTPS calls to Google.
      1) It will send refresh token to Google.
      2) Google verifies it.
      3) Google returns: new access token, new expiry time.
      4) Credentials object is updated in memory: creds.valid == True, creds.expired == False.

✅"flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)":
   - The InstalledAppFlow reads the SCOPES to know what permissions to ask for, and reads the
     CLIENT_SECRET_FILE to prove to Google that this is your specific bot asking for them.

✅"creds = flow.run_local_server(port=0)":
   1) Python starts the local server.
   2) Python bundles your requirements (Scopes + Client ID) into a long URL.
   3) Python opens that URL in your browser immediately.
   4) Google's Server receives that URL, checks the requirements instantly, and IF they are valid, it
      serves you the Login Page.
   - port=0 means let Python pick any free port automatically.

✅"with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(creds.to_json())":
   - "open": Opens the file.
   - "'w'": This stands for Write. It tells Python: If this file exists, wipe it clean. If it doesn't
     exist, create it from scratch.
   - "with": Is safety manager, It ensures the file always closes, even if the code crashes halfway through so
     it doesn't get corrupted.
   - "as token": tells Python From now on, whenever I say token, I am talking about that open file on the hard drive.
   - "to_json()": It will translate complex memory that is inside creds into a simple Text String.
   - "write": Finally, it physically types that text string into the file.

✅"service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)":
   -"API_SERVICE_NAME + API_VERSION": They choose which Google API and version you are using.
   - "build": after the creds have make the connection, it will make a python object that represents the Gmail API, so 
      when we want to call it another time for adding or reading something or other things we can call it easily.
   - IN simple: Credentials prove who you are, discovery info explains how the API works, and service is the object
     that combines both so you can use Gmail API easily.
   - discovery info: description of the API, like: What methods exist (messages.list, messages.send), What URLs to call.
   - "static_discovery= ":
     - "True": that mean the discovery info must be in out laptop(less reliable)(faster).
     - "False": that mean we will take theses information from the Google at the runtime(More reliable)(slower).
"""