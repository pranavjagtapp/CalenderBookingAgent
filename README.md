# 🤖 Calendar Booking Agent (LangGraph + FastAPI + Streamlit)

## 🚀 Description
A conversational AI agent that helps users book appointments via chat. It understands natural language, checks Google Calendar for availability, and confirms bookings.

## 💡 Tech Stack
- **Backend:** FastAPI
- **Agent Framework:** LangGraph
- **Frontend:** Streamlit
- **Calendar Integration:** Google Calendar API

## 🗂️ Features
- Conversational booking interface
- Smart date/time parsing using `dateparser`
- Checks availability from Google Calendar
- Suggests nearby free slots if the requested one is busy
- Confirms and creates Google Calendar events
- Session memory + graceful fallback messages

## ✅ How to Run Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/pranavjagtapp/CalenderBookingAgent.git
   cd CalenderBookingAgent
