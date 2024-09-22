#include <WiFi.h>       

#include <HTTPClient.h>   

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

// Replace with your actual sensor pins
const int temperatureSensorPin = 35;  // Example analog pin for temperature
const int CO2SensorPin = 34;          // Example analog pin for CO2
const int waterLevelSensorPin = 32;   // Example analog pin for water level

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    Serial.println("Connected to WiFi");
}

float readTemperature() {
    
    return analogRead(temperatureSensorPin) * (3.3 / 4095.0) * 100; 
}

int readCO2() {
    
    return analogRead(CO2SensorPin); 
}

float readWaterLevel() {
    
    
    return analogRead(waterLevelSensorPin) * (3.3 / 4095.0) * 100; // Convert to percentage
}

void sendPostRequest(float temperature, int CO2, float waterLevel) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;

        // Specify the URL for the API endpoint
        http.begin("http://our_endpoint.com/api/endpoint");

        // Format the payload with sensor values
       String payload = "{\"temp\":{\"value\":\"" + temperature + "\"}, \"co2\":{\"value\":\"" + CO2 + "\"}, \"waterLevel\":{\"value\":\"" + waterLevel + "\"}}";

        
        // Specify the content type and payload
        http.addHeader("Content-Type", "application/json");

        // Send the POST request
        int httpResponseCode = http.POST(payload);

        if (httpResponseCode > 0) {
            String response = http.getString();  // Get the response to the request
            Serial.println(httpResponseCode);    // Print HTTP response code
            Serial.println(response);            // Print the response from the server
        } else {
            Serial.println("Error on sending POST");
        }

        http.end();  // Close connection
    }
}

void loop() {
    float temperature = readTemperature();
    int CO2 = readCO2();
    float waterLevel = readWaterLevel();

    sendPostRequest(temperature, CO2, waterLevel);
    delay(60000);  // Send request every 60 seconds
}
