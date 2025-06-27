from langgraph.graph import StateGraph
import dateparser
import pytz
from typing import TypedDict
from datetime import datetime, timedelta
from google_calendar import get_free_slots, create_event

class BookingState(TypedDict):
    intent: str | None
    date: datetime | None
    time: str | None
    duration: int
    confirmed: bool
    slots: list[datetime] | None

class BookingAgent:
    def __init__(self):
        self.graph = StateGraph(BookingState)
        self.state: BookingState = {
            "intent": None,
            "date": None,
            "time": None,
            "duration": 30,
            "confirmed": False,
            "slots": None
        }

        self.graph.add_node("start", self.start_node)
        self.graph.add_node("check_availability", self.check_availability)
        self.graph.add_node("confirm_and_book", self.confirm_and_book)
        self.graph.set_entry_point("start")

    def start_node(self, user_input):
        if not user_input.strip():
            return "start"
    
        parsed_time = dateparser.parse(
    user_input,
    settings={
        'PREFER_DATES_FROM': 'future',
        'RELATIVE_BASE': datetime.now()
    }
)

        if parsed_time:
    # Ensure it's timezone-aware and convert to UTC
         if    parsed_time.tzinfo is None:
          parsed_time = parsed_time.replace(tzinfo=pytz.timezone("Asia/Kolkata"))
          self.state["date"] = parsed_time.astimezone(pytz.UTC)
        else:
          self.state["date"] = datetime.now(tz=pytz.UTC)

# Intent detection
        if "book" in user_input or "schedule" in user_input:
          self.state["intent"] = "book"
          return "check_availability"
        elif "free" in user_input or "available" in user_input:
           self.state["intent"] = "check"
           return "check_availability"
        else:
            return "start"




    def check_availability(self, user_input):
        start = self.state["date"]
        start_of_day = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start.replace(hour=23, minute=59, second=59, microsecond=0)

        slots = get_free_slots(start_of_day, end_of_day)
        self.state["slots"] = slots[:3] if slots else []  # Suggest up to 3 slots
        return "confirm_and_book"

    def confirm_and_book(self, user_input):
        if not self.state["slots"]:
            return "No free slots available. Please try another time."

        selected = self.state["slots"][0]
        end = selected + timedelta(minutes=self.state["duration"])
        create_event(selected, end, summary="Booked via AI Agent")
        self.state["confirmed"] = True

        suggestions = "\n".join([
            f"- {slot.strftime('%I:%M %p')} on {slot.strftime('%Y-%m-%d')}" 
            for slot in self.state["slots"]
        ])

        return f"✅ Booked slot at {selected.strftime('%I:%M %p')} on {selected.strftime('%Y-%m-%d')}!\nHere are other available slots you may consider next time:\n{suggestions}"

    def run(self, user_input):
        node = "start"
        while True:
            if node == "start":
                node = self.start_node(user_input)
            elif node == "check_availability":
                node = self.check_availability(user_input)
            elif node == "confirm_and_book":
                return self.confirm_and_book(user_input)
            else:
                return "Sorry, I didn't understand that."
