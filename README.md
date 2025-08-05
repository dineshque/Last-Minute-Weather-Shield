# Last-Minute Weather Shield – Crop-Saving Alerts

> A Flask-based application that fetches weather data, detects risky weather for crops, and provides actionable voice alerts in Hindi and English to help farmers protect their crops from sudden hailstorms, high winds, and heavy rains.

## Table of Contents

- [Project Overview](#project-overview)  
- [Problem Statement](#problem-statement)  
- [Solution](#solution)  
- [Features](#features)  
- [Setup Instructions](#setup-instructions)  
- [Usage](#usage)  
- [API Endpoints](#api-endpoints)  
- [Voice Alert Integration](#voice-alert-integration)  
- [Frontend Demo](#frontend-demo)  


## Project Overview

This project aims to provide farmers with timely weather alerts specifically tailored to protect crops from sudden destructive weather events like hailstorms, strong winds, or heavy rainfall. Unlike generic weather apps, it delivers **actionable voice alerts in the local language (Hindi or English)**, advising farmers on how to secure their fields and reduce crop damage.

## Problem Statement

Unpredictable weather such as sudden hailstorms, gusty winds, and heavy rainfall can destroy crops overnight, leading to huge financial losses for farmers. Traditional weather apps provide forecasts but often lack localized, timely, and actionable advice.

## Solution

- Connects to **OpenWeatherMap API** to fetch real-time weather data.
- Detects **weather risks** based on defined thresholds: high wind, heavy rain, hail.
- Provides **actionable advice** addressing these risks in Hindi and English.
- Converts advisories into **voice alerts using Google Text-to-Speech (gTTS)** for better accessibility.
- Offers a simple demo **web interface** for farmers (or anyone) to input location and get instant alerts with audio playback.

## Features

- Fetches current weather data using OpenWeatherMap API.
- Risk detection for high wind (>40 km/h), heavy rain (>20 mm in 1hr/3hr), and hail events.
- Actionable advice messages mapped to each risk.
- Text-to-speech conversion of advice in Hindi and English.
- Minimal user-friendly frontend with audio playback.
- Robust error-handling with status messages.
- Modular code and unit testing support.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- OpenWeatherMap API key (free at https://openweathermap.org/api)

### Installation Steps

1. Clone the repository:
    ```
    git clone https://github.com/YOUR-USERNAME/weather-shield-hackathon.git
    cd weather-shield-hackathon
    ```

2. Set up and activate a Python virtual environment:
    ```
    python -m venv venv
    # Activate on Linux/Mac
    source venv/bin/activate
    # Activate on Windows
    venv\Scripts\activate
    ```

3. Install required Python packages:
    ```
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root and add your OpenWeatherMap API key:
    ```
    OPENWEATHERMAP_API_KEY=your_actual_api_key_here
    ```

5. Run the Flask app:
    ```
    python app.py
    ```

6. Open your browser and visit:  
    [http://localhost:5000](http://localhost:5000)

## Usage

- Enter your city name into the form on the homepage.
- Receive text advice about weather risks in **Hindi** and **English**.
- Listen to audio voice alerts directly on the page.
- The backend `/weather` endpoint can be used for programmatic access.
- The `/voice_alert` endpoint accepts text and returns speech audio.

## API Endpoints

| Endpoint        | Method | Description                                                  | Parameters                                  |
|-----------------|--------|--------------------------------------------------------------|---------------------------------------------|
| `/weather`      | GET    | Fetch weather, detect risks, and return actionable advice.  | `city` (required) <br> `lang` (optional: `hi` or `en`) |
| `/voice_alert`  | POST   | Convert advice text to speech audio (MP3).                  | JSON `{ "message": "<text>", "lang": "hi" }` |
| `/get_voice`    | GET    | Stream pre-generated voice alert audio via query parameters | `message` (required), `lang` (optional)    |
| `/`             | GET    | Demo frontend page                                            | n/a                                         |
| `/demo`         | GET    | Demo route to handle form input and show advice + audio     | `city` (required)                           |

## Voice Alert Integration

This project uses the **Google Text-to-Speech (gTTS)** Python library to convert advice strings into MP3 audio streamed from the backend.

- Use `/voice_alert` POST endpoint with JSON containing advice text and language.
- Or call `/get_voice` with query parameters for quick audio generation.
- Audio playback is supported in the frontend demo for convenience.

## Frontend Demo

The frontend demo is built with Flask-Jinja templates and includes:

- City input text box.
- Display of risk advice in Hindi and English as bullet lists.
- Audio player controls to listen to generated voice alerts.
- Clear error messaging on input or fetch errors.
- Responsive and accessible design with improved UI styling.
