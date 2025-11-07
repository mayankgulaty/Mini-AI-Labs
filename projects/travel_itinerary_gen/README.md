# 🌍 Travel Itinerary Generator

Generates personalized trip plans from JSON input using OpenAI and Google Maps API.

## 📋 Description

A Node.js tool that creates detailed, personalized travel itineraries based on user preferences, destination, dates, and interests. Uses OpenAI GPT for intelligent planning and Google Maps API for location data.

## 🚀 Features

- Generate personalized travel itineraries
- Support for multiple destinations
- Integration with Google Maps for accurate locations
- JSON input/output format
- Web and CLI interfaces

## 🛠️ Installation

```bash
cd projects/travel_itinerary_gen
npm install
```

## ⚙️ Setup

1. Set your API keys:
```bash
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_MAPS_API_KEY="your-google-maps-key"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-openai-key
GOOGLE_MAPS_API_KEY=your-google-maps-key
```

## 💻 Usage

### CLI Mode

```bash
node app.js --input trip.json --output itinerary.json
```

### Web Mode

```bash
node app.js --web
```

Then visit `http://localhost:3000`

## 📝 Example Input (trip.json)

```json
{
  "destination": "Paris, France",
  "startDate": "2024-06-01",
  "endDate": "2024-06-05",
  "interests": ["museums", "food", "architecture"],
  "budget": "moderate",
  "travelers": 2
}
```

## 🧪 Testing

```bash
npm test
```

## 📄 License

MIT

