import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
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
        # 이벤트 시작/종료 시간
        start_time = datetime(2025, 8, 1, 10, 0, 0).isoformat() + '+09:00'
        end_time = datetime(2025, 8, 1, 11, 0, 0).isoformat() + '+09:00'

        # 중복 이벤트 있는지 확인
        events_result = self.service.events().list(
            calendarId=self.CALENDAR_ID,
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        existing_events = events_result.get('items', [])
        if existing_events:
            print("❌ 이미 해당 시간에 일정이 존재합니다.")
            return "이미 해당 시간에 예약이 존재합니다."

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


    def get_available_slots(self,date_str, start_hour=10, end_hour=18, interval_minutes=30):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        start_time = date.replace(hour=start_hour, minute=0).isoformat() + 'Z'
        end_time = date.replace(hour=end_hour, minute=0).isoformat() + 'Z'

        # 3. 해당 날짜의 예약된 이벤트 가져오기
        events_result = self.service.events().list(
            calendarId=self.CALENDAR_ID,
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # 4. 예약된 시간 리스트 추출
        reserved = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            reserved.append(dt.strftime("%H:%M"))

        # 5. 전체 가능한 시간 슬롯 생성
        slots = []
        current = date.replace(hour=start_hour, minute=0)
        end = date.replace(hour=end_hour, minute=0)
        while current < end:
            time_str = current.strftime("%H:%M")
            if time_str not in reserved:
                slots.append(time_str)
            current += timedelta(minutes=interval_minutes)

        print("예약할 수 있는 시간은 다음과 같습니다:"+slots)
        return slots