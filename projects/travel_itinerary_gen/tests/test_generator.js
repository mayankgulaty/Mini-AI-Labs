/**
 * Tests for travel itinerary generator
 */

const { TravelItineraryGenerator } = require('../app');

describe('TravelItineraryGenerator', () => {
    let generator;

    beforeEach(() => {
        // Mock environment variables
        process.env.OPENAI_API_KEY = 'test-key';
        generator = new TravelItineraryGenerator();
    });

    test('should initialize with API key', () => {
        expect(generator).toBeDefined();
    });

    test('should throw error if OPENAI_API_KEY is missing', () => {
        delete process.env.OPENAI_API_KEY;
        expect(() => new TravelItineraryGenerator()).toThrow('OPENAI_API_KEY not set');
    });

    // Note: Full integration tests would require mocking OpenAI and Google Maps APIs
});

