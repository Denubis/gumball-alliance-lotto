#!/usr/bin/env python3

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#https://docs.google.com/spreadsheets/d/1fI0vVRweVKYUWK3uwkijXeal5JcZl9NFTf5os-DUBkc/edit?usp=sharing
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1fI0vVRweVKYUWK3uwkijXeal5JcZl9NFTf5os-DUBkc'
SAMPLE_RANGE_NAME = 'Alliance!A2:A'

def getMembers():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    people = {}
    if not values:
        print('No data found.')
    else:        
        for row in values:
            if row:
                people[row[0]] = row[0]
    print(people)
    return people
if __name__ == '__main__':
    print(getMembers())