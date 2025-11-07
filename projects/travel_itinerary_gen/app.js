#!/usr/bin/env node
/**
 * Travel Itinerary Generator - Creates personalized trip plans using OpenAI and Google Maps
 */

const fs = require('fs');
const path = require('path');
require('dotenv').config();
const OpenAI = require('openai');
const express = require('express');
const { Client } = require('@googlemaps/google-maps-services-js');

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const googleMaps = new Client({});

class TravelItineraryGenerator {
    constructor() {
        if (!process.env.OPENAI_API_KEY) {
            throw new Error('OPENAI_API_KEY not set in environment variables');
        }
        if (!process.env.GOOGLE_MAPS_API_KEY) {
            console.warn('⚠️  GOOGLE_MAPS_API_KEY not set. Location features will be limited.');
        }
    }

    async generateItinerary(tripData) {
        const { destination, startDate, endDate, interests, budget, travelers } = tripData;
        
        // Calculate number of days
        const start = new Date(startDate);
        const end = new Date(endDate);
        const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;

        // Build prompt for OpenAI
        const prompt = `Create a detailed ${days}-day travel itinerary for ${destination}.
        
Requirements:
- Start date: ${startDate}
- End date: ${endDate}
- Interests: ${interests.join(', ')}
- Budget level: ${budget}
- Number of travelers: ${travelers}

Please provide a day-by-day itinerary with:
1. Morning activities
2. Afternoon activities
3. Evening activities
4. Restaurant recommendations
5. Transportation tips
6. Estimated costs per day

Format the response as a structured JSON object with daily plans.`;

        try {
            const completion = await openai.chat.completions.create({
                model: "gpt-3.5-turbo",
                messages: [
                    {
                        role: "system",
                        content: "You are a professional travel planner. Create detailed, practical itineraries with specific recommendations."
                    },
                    {
                        role: "user",
                        content: prompt
                    }
                ],
                temperature: 0.7,
                max_tokens: 2000
            });

            const itineraryText = completion.choices[0].message.content;
            
            // Try to parse as JSON, if not, return as structured text
            let itinerary;
            try {
                itinerary = JSON.parse(itineraryText);
            } catch (e) {
                // If not JSON, create structured object from text
                itinerary = {
                    destination,
                    startDate,
                    endDate,
                    days,
                    itinerary: itineraryText,
                    raw: itineraryText
                };
            }

            // Enhance with Google Maps data if available
            if (process.env.GOOGLE_MAPS_API_KEY) {
                itinerary = await this.enhanceWithMapsData(itinerary, destination);
            }

            return itinerary;
        } catch (error) {
            throw new Error(`Failed to generate itinerary: ${error.message}`);
        }
    }

    async enhanceWithMapsData(itinerary, destination) {
        if (!process.env.GOOGLE_MAPS_API_KEY) {
            return itinerary;
        }

        try {
            // Get destination coordinates
            const geocodeResponse = await googleMaps.geocode({
                params: {
                    address: destination,
                    key: process.env.GOOGLE_MAPS_API_KEY
                }
            });

            if (geocodeResponse.data.results.length > 0) {
                const location = geocodeResponse.data.results[0].geometry.location;
                itinerary.location = {
                    lat: location.lat,
                    lng: location.lng,
                    formattedAddress: geocodeResponse.data.results[0].formatted_address
                };
            }
        } catch (error) {
            console.warn('⚠️  Could not fetch location data:', error.message);
        }

        return itinerary;
    }
}

// CLI Mode
async function main() {
    const args = process.argv.slice(2);
    const inputIndex = args.indexOf('--input') !== -1 ? args.indexOf('--input') : args.indexOf('-i');
    const outputIndex = args.indexOf('--output') !== -1 ? args.indexOf('--output') : args.indexOf('-o');
    const webMode = args.includes('--web');

    if (webMode) {
        const app = express();
        app.use(express.json());
        app.use(express.static('public'));

        const generator = new TravelItineraryGenerator();

        app.get('/', (req, res) => {
            res.send(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Travel Itinerary Generator</title>
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
                        form { display: flex; flex-direction: column; gap: 15px; }
                        input, select, textarea { padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
                        button { padding: 12px 24px; background: #007bff; color: white; border: none; cursor: pointer; }
                        button:hover { background: #0056b3; }
                        .result { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
                    </style>
                </head>
                <body>
                    <h1>🌍 Travel Itinerary Generator</h1>
                    <form id="itineraryForm">
                        <input type="text" name="destination" placeholder="Destination (e.g., Paris, France)" required>
                        <input type="date" name="startDate" required>
                        <input type="date" name="endDate" required>
                        <input type="text" name="interests" placeholder="Interests (comma-separated, e.g., museums, food, architecture)" required>
                        <select name="budget">
                            <option value="budget">Budget</option>
                            <option value="moderate" selected>Moderate</option>
                            <option value="luxury">Luxury</option>
                        </select>
                        <input type="number" name="travelers" placeholder="Number of travelers" value="2" min="1" required>
                        <button type="submit">Generate Itinerary</button>
                    </form>
                    <div id="result"></div>
                    <script>
                        document.getElementById('itineraryForm').addEventListener('submit', async (e) => {
                            e.preventDefault();
                            const formData = new FormData(e.target);
                            const data = {
                                destination: formData.get('destination'),
                                startDate: formData.get('startDate'),
                                endDate: formData.get('endDate'),
                                interests: formData.get('interests').split(',').map(i => i.trim()),
                                budget: formData.get('budget'),
                                travelers: parseInt(formData.get('travelers'))
                            };
                            const resultDiv = document.getElementById('result');
                            resultDiv.innerHTML = '<p>Generating itinerary...</p>';
                            try {
                                const response = await fetch('/api/generate', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify(data)
                                });
                                const result = await response.json();
                                resultDiv.innerHTML = '<div class="result"><h2>Your Itinerary:</h2><pre>' + JSON.stringify(result, null, 2) + '</pre></div>';
                            } catch (error) {
                                resultDiv.innerHTML = '<div class="result" style="background: #f8d7da; color: #721c24;">Error: ' + error.message + '</div>';
                            }
                        });
                    </script>
                </body>
                </html>
            `);
        });

        app.post('/api/generate', async (req, res) => {
            try {
                const generator = new TravelItineraryGenerator();
                const itinerary = await generator.generateItinerary(req.body);
                res.json(itinerary);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        const PORT = process.env.PORT || 3000;
        console.log(`🌐 Web server starting on http://localhost:${PORT}`);
        app.listen(PORT);
    } else if (inputIndex !== -1 && inputIndex < args.length - 1) {
        const inputFile = args[inputIndex + 1];
        const outputFile = outputIndex !== -1 && outputIndex < args.length - 1 
            ? args[outputIndex + 1] 
            : inputFile.replace('.json', '_itinerary.json');

        try {
            const tripData = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
            const generator = new TravelItineraryGenerator();
            
            console.log('🔄 Generating itinerary...');
            const itinerary = await generator.generateItinerary(tripData);
            
            fs.writeFileSync(outputFile, JSON.stringify(itinerary, null, 2));
            console.log(`✅ Itinerary saved to ${outputFile}`);
            
            console.log('\n' + '='.repeat(50));
            console.log('ITINERARY SUMMARY:');
            console.log('='.repeat(50));
            console.log(JSON.stringify(itinerary, null, 2));
        } catch (error) {
            console.error(`❌ Error: ${error.message}`);
            process.exit(1);
        }
    } else {
        console.log(`
Usage:
  node app.js --input trip.json [--output itinerary.json]
  node app.js --web

Options:
  --input, -i    Input JSON file with trip details
  --output, -o   Output JSON file (optional)
  --web          Run as web server
        `);
        process.exit(1);
    }
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = { TravelItineraryGenerator };

