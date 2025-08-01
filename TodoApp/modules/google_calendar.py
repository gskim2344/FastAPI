from __future__ import print_function
import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# 일정 추가 시 필요한 권한 범위
SCOPES = ['https://www.googleapis.com/auth/calendar']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR,  'credentials.json')

def google_calendar():
    creds = None

    # 이전 인증 정보 불러오기
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    print(creds)

    # 인증되지 않았거나 만료된 경우 새로 로그인
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # 토큰 저장
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    print("credentials loaded")
    # Google Calendar API 객체 생성
    service = build('calendar', 'v3', credentials=creds)

    # 일정 데이터 정의
    event = {
        'summary': 'AI 미용실 예약',
        'location': 'Shinjuku, Tokyo',
        'description': 'LINE 예약으로 등록된 일정입니다.',
        'start': {
            'dateTime': '2025-08-01T10:00:00+09:00',
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': '2025-08-01T11:00:00+09:00',
            'timeZone': 'Asia/Tokyo',
        },
    }
    print(event)

    # 일정 삽입
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('일정이 추가되었습니다:', event.get('htmlLink'))

