# Yoliday Rasa Travel Assistant Bot

This is a functional "Travel Assistant Bot" developed for the Yoliday Rasa Bot Development Internship Assessment. The bot assists users with travel-related queries, including weather forecasts and packing recommendations.

## Features

- **Intent Handling**: Recognizes user intents like greeting, asking for weather, and requesting packing tips.
- **Entity Extraction**: Extracts key information like `location` and `travel_dates`.
- **Forms & Slots**: Uses a form to collect necessary details for a travel query (Destination, Start Date, End Date).
- **Custom Actions & API Integration**: Connects to the **OpenWeatherMap API** to provide real-time weather data.
- **Dynamic Responses**: Recommends what to pack based on the weather forecast.
- **FAQs & Fallback**: Answers predefined questions and handles out-of-scope queries gracefully.
- **Web Frontend**: Includes a simple web chat interface for interaction.

---

## Prerequisites

- Python 3.8+
- `pip` package manager
- [Rasa Open Source](https://rasa.com/docs/rasa/installation)
- A free **OpenWeatherMap API Key**.

---

## Setup and Running the Bot

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd yoliday-rasa-bot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Add API Key**
    -   Rename the `.env.example` file to `.env` (or create a new one).
    -   Open the `.env` file and add your OpenWeatherMap API key:
        ```
        OPENWEATHER_API_KEY="YOUR_API_KEY_HERE"
        ```

4.  **Train the Rasa Model**
    This will train the NLU and dialogue models based on the data in the `data/` folder.
    ```bash
    rasa train
    ```

5.  **Run the Servers**
    You need to run two separate servers in two different terminal windows.

    -   **Terminal 1: Run the Action Server**
        This server runs your custom Python code (`actions.py`).
        ```bash
        rasa run actions
        ```

    -   **Terminal 2: Run the Rasa Server**
        This server runs the main chatbot logic and exposes the API for the frontend.
        ```bash
        rasa run --enable-api --cors "*"
        ```

6.  **Chat with the Bot!**
    -   Open the `frontend/index.html` file in your web browser.
    -   The chat widget will appear, and you can start interacting with your travel assistant.

---

## Sample Conversation

Here is a sample conversation flow:

**User**: `Hello`
**Bot**: `Hello! I'm your Yoliday travel assistant. How can I help you plan your trip today? You can ask me for weather or packing recommendations.`

**User**: `what should I pack for my trip to London?`
**Bot**: `Sure! What city are you traveling to?` (Note: It already knows London but the form asks for confirmation or if it was missed)
**User**: `London`
**Bot**: `What is your travel start date?`
**User**: `next Monday`
**Bot**: `And what is your travel end date?`
**User**: `next Friday`
**Bot**: `Great! Let me fetch that information for you.`
**Bot**: `The current weather in London is overcast clouds with a temperature of 15.3°C.`
**Bot**: `Based on the weather, I recommend packing: a light jacket.`

**User**: `who built you?`
**Bot**: `I was built by a talented intern for the Yoliday Rasa Bot Development assessment.`

**User**: `thanks bye`
**Bot**: `Goodbye! Have a great trip!`

---

## Deployment

To make the bot publicly accessible as required:

-   **Using ngrok (for local testing):**
    1.  [Download and set up ngrok](https://ngrok.com/download).
    2.  Expose your local Rasa server (port 5005) to the internet: `ngrok http 5005`
    3.  In `frontend/index.html`, replace `http://localhost:5005` in the `socketUrl` with your public ngrok URL (e.g., `https://random-subdomain.ngrok.io`).
    4.  The action server also needs to be accessible. You can either deploy it separately or use a platform that handles both.

-   **Using Railway/Render:**
    These platforms can deploy Docker containers. You can create a `Dockerfile` for the Rasa server and another for the action server, and deploy them as separate services. Update the `endpoints.yml` and frontend URL to use the public URLs provided by the platform.