# actions/actions.py
import os
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from dotenv import load_dotenv
from rasa_sdk.events import AllSlotsReset

load_dotenv()

class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the API key from environment variables
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            dispatcher.utter_message(text="Error: OpenWeatherMap API key is not set.")
            return []

        # Get the destination city from the slot
        city = tracker.get_slot("destination_city")
        if not city:
            dispatcher.utter_message(text="I don't know the city. Please specify a destination.")
            return []

        # API endpoint
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            if data["cod"] != 200:
                dispatcher.utter_message(text=f"Sorry, I couldn't find the weather for {city}.")
                return [SlotSet("weather_description", None)]

            # Extract weather information
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            
            message = f"The current weather in {city} is {weather_desc} with a temperature of {temp}°C."
            dispatcher.utter_message(text=message)
            
            # Set the weather description slot for the packing action
            return [SlotSet("weather_description", weather_desc)]

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"An error occurred while fetching weather data: {e}")
            return [SlotSet("weather_description", None)]
        except KeyError:
            dispatcher.utter_message(text=f"Sorry, I could not retrieve weather data for {city}. Please check the city name.")
            return [SlotSet("weather_description", None)]


class ActionRecommendPacking(Action):

    def name(self) -> Text:
        return "action_recommend_packing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        weather_desc = tracker.get_slot("weather_description")

        if not weather_desc:
            dispatcher.utter_message(text="I can't recommend what to pack without knowing the weather.")
            return []

        packing_list = []
        
        # Simple logic based on keywords in the weather description
        if "rain" in weather_desc or "drizzle" in weather_desc:
            packing_list.append("an umbrella")
            packing_list.append("a raincoat")
        if "clear" in weather_desc or "sun" in weather_desc:
            packing_list.append("sunglasses")
            packing_list.append("sunscreen")
        if "clouds" in weather_desc:
            packing_list.append("a light jacket")
        if "snow" in weather_desc:
            packing_list.append("a warm coat, gloves, and a scarf")

        if not packing_list:
            message = "Based on the weather, standard clothing should be fine. Enjoy your trip!"
        else:
            recommendation = ", ".join(packing_list)
            message = f"Based on the weather, I recommend packing: {recommendation}."
            
        dispatcher.utter_message(text=message)

        return []
    
    # Add this new class at the very end of the file
class ActionResetSlots(Action):

    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]