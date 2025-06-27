from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import List

# CONFIG
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_ID = 'pranavjagtappp@gmail.com'  # ✅ make sure this calendar exists and is accessible

# AUTHENTICATION
try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
except Exception as e:
    raise RuntimeError("Google Calendar setup failed. Reason: " + str(e))


# ✅ FUNCTION: Fetch free time slots
def get_free_slots(start_date: datetime, end_date: datetime, duration_minutes: int = 30) -> List[datetime]:
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_date.isoformat(),  # ✔ timezone-aware and clean
        timeMax=end_date.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    free_slots = []

    current = start_date
    while current + timedelta(minutes=duration_minutes) <= end_date:
        busy = False
        for event in events:
            # Convert event start & end times to datetime objects
            event_start = datetime.fromisoformat(event['start']['dateTime'])
            event_end = datetime.fromisoformat(event['end']['dateTime'])
            if event_start <= current < event_end:
                busy = True
                break
        if not busy:
            free_slots.append(current)
        current += timedelta(minutes=30)

    return free_slots


# ✅ FUNCTION: Create calendar event
def create_event(start_time: datetime, end_time: datetime, summary: str = "Meeting"):
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata'
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata'
        }
    }

    return service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
