#!/usr/bin/env python3
"""
API Integration – Weather Fetcher (Keyless Version)
Internship Submission – Codveda Technologies
Author: Suresh Das
Date: 2026-08-28

Description:
    Fetches current weather data from wttr.in (free, no API key required).
    Displays formatted weather information and optionally saves to CSV.

Usage:
    python weather.py --city Kolkata
    python weather.py --city "New York" --units metric --output weather.csv
"""

import sys
import csv
import argparse
from dataclasses import dataclass
from typing import Optional, Dict, Any
import requests


@dataclass
class WeatherData:
    """Simple container for weather information."""
    city: str
    region: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float
    pressure: int
    uv_index: float


class WeatherFetcher:
    """Handles API calls to wttr.in (no API key required)."""

    BASE_URL = "https://wttr.in"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "WeatherApp/1.0"})

    def fetch(self, city: str, units: str = "metric") -> Optional[WeatherData]:
        """
        Fetch weather for a given city.
        Returns a WeatherData object or None on error.
        """
        # wttr.in query parameters: ?m = metric, ?u = imperial, ?M = standard
        unit_flag = "?m" if units == "metric" else "?u" if units == "imperial" else "?M"
        url = f"{self.BASE_URL}/{city}{unit_flag}&format=j1"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return self._parse_response(data, city)
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
        except ValueError as e:
            print(f"❌ Invalid JSON response: {e}")
        except KeyError as e:
            print(f"❌ Unexpected API response structure: missing {e}")
        return None

    def _parse_response(self, data: Dict[str, Any], city: str) -> WeatherData:
        """Extract relevant fields from the wttr.in response."""
        current = data.get("current_condition", [{}])[0]
        location = data.get("nearest_area", [{}])[0]

        # Determine unit system based on returned data
        if "temp_C" in current:
            temp = float(current.get("temp_C", 0))
            feels = float(current.get("FeelsLikeC", 0))
        else:  # imperial
            temp = float(current.get("temp_F", 0))
            feels = float(current.get("FeelsLikeF", 0))

        return WeatherData(
            city=location.get("areaName", [{}])[0].get("value", city),
            region=location.get("region", [{}])[0].get("value", ""),
            country=location.get("country", [{}])[0].get("value", ""),
            temperature=temp,
            feels_like=feels,
            humidity=int(current.get("humidity", 0)),
            description=current.get("weatherDesc", [{}])[0].get("value", ""),
            wind_speed=float(current.get("windspeedKmph", 0)),
            pressure=int(current.get("pressure", 0)),
            uv_index=float(current.get("uvIndex", 0)),
        )


def display_weather(weather: WeatherData, units: str) -> None:
    """Pretty‑print weather data with emojis."""
    temp_symbol = "°C" if units == "metric" else "°F"
    wind_symbol = "km/h" if units == "metric" else "mph"

    # Emoji mapping
    desc = weather.description.lower()
    if "sunny" in desc or "clear" in desc:
        emoji = "☀️"
    elif "cloud" in desc or "overcast" in desc:
        emoji = "☁️"
    elif "rain" in desc or "drizzle" in desc:
        emoji = "🌧️"
    elif "thunder" in desc or "storm" in desc:
        emoji = "⛈️"
    elif "snow" in desc or "ice" in desc:
        emoji = "❄️"
    elif "fog" in desc or "mist" in desc:
        emoji = "🌫️"
    else:
        emoji = "🌡️"

    print("\n" + "=" * 50)
    print(f"📍 {weather.city}, {weather.region}, {weather.country}")
    print(f"{emoji} {weather.description}")
    print("=" * 50)
    print(f"🌡️ Temperature  : {weather.temperature:.1f}{temp_symbol} (feels like {weather.feels_like:.1f}{temp_symbol})")
    print(f"💧 Humidity     : {weather.humidity}%")
    print(f"💨 Wind Speed   : {weather.wind_speed:.1f} {wind_symbol}")
    print(f"📊 Pressure     : {weather.pressure} hPa")
    print(f"☀️ UV Index     : {weather.uv_index}")
    print("=" * 50 + "\n")


def save_to_csv(weather: WeatherData, filename: str) -> None:
    """Save weather data to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=weather.__annotations__.keys())
            writer.writeheader()
            writer.writerow(weather.__dict__)
        print(f"💾 Data saved to {filename}")
    except IOError as e:
        print(f"❌ Failed to write CSV: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch current weather from wttr.in (no API key required).")
    parser.add_argument("--city", required=True, help="City name (e.g., 'London', 'New York')")
    parser.add_argument("--units", choices=["metric", "imperial"], default="metric",
                        help="Units: metric (°C, km/h) or imperial (°F, mph)")
    parser.add_argument("--output", help="Save data to CSV file (optional)")
    args = parser.parse_args()

    fetcher = WeatherFetcher()
    weather = fetcher.fetch(args.city, args.units)

    if weather is None:
        print("❌ Failed to fetch weather data. Please check the city name.")
        sys.exit(1)

    display_weather(weather, args.units)

    if args.output:
        save_to_csv(weather, args.output)


if __name__ == "__main__":
    main()