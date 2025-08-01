import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 구글 캘린더 권한 범위


class GoogleCalendar:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # 서비스 계정 키 경로
        self.SERVICE_ACCOUNT_FILE = os.path.join(self.BASE_DIR, '..', 'credentials', 'service_account.json')
        self.CALENDAR_ID = "68182829d703e8372b86f5f3aca3f8db0ad256866fbe939d804ee1449f5a6824@group.calendar.google.com"
        # 서비스 계정 인증 객체 생성
        creds = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES
        )
        # Google Calendar API 객체 생성
        self.service = build('calendar', 'v3', credentials=creds)

    def add_calendar(self):
        # 삽입할 일정 정보
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

        # calendar_id = "googlecalendar4store@neural-caldron-467700-j1.iam.gserviceaccount.com"
        # 일정 등록 (⚠️ 공유된 캘린더 ID 필요 시 calendarId 수정)
        event = self.service.events().insert(calendarId=self.CALENDAR_ID, body=event).execute()
        print('✅ 일정이 추가되었습니다:', event.get('htmlLink'))

        calendar_list = self.service.calendarList().list().execute()
        for calendar_entry in calendar_list['items']:
            print('✅ TEST:',calendar_entry['id'], calendar_entry.get('summary'))
