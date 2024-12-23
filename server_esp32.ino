#include <WiFi.h>
#include <DHT.h>

const char* ssid = "your_wifi_name";
const char* password = "your_wifi_password";

#define DHTPIN 14
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
#define RAINDROP_PIN 34
#define LDR_PIN 35
#define MQ135_PIN 39
#define MQ135_DIGITAL_PIN 32
#define RAINDROP_DIGITAL_PIN 25

WiFiServer server(8080);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  dht.begin();
  pinMode(MQ135_DIGITAL_PIN, INPUT);
  pinMode(RAINDROP_DIGITAL_PIN, INPUT);
  server.begin();
}

void loop() {

  WiFiClient client = server.available();

  if (client) {

    Serial.println("New client connected");

    unsigned long connectionStartTime = millis(); // For timeout

    while (client.connected()) {
      if (millis() - connectionStartTime > 10000) { // Timeout
        Serial.println("Connection timed out");
        break; // If timeout exit
      }

      // Read sensor data
      float humidity = dht.readHumidity();
      float temperature = dht.readTemperature();
      int raindropValue = analogRead(RAINDROP_PIN);
      int ldrValue = analogRead(LDR_PIN);
      int mq135Value = analogRead(MQ135_PIN);
      int mq135DigitalState = digitalRead(MQ135_DIGITAL_PIN);
      int raindropDigitalState = digitalRead(RAINDROP_DIGITAL_PIN);

      // Check if sensors are working
      bool dhtWorking = !isnan(temperature) && !isnan(humidity);
      bool raindropWorking = raindropValue >= 0 && raindropValue <= 4095;
      bool ldrWorking = ldrValue >= 0 && ldrValue <= 4095;
      bool mq135Working = mq135Value >= 0 && mq135Value <= 4095;

      // Debugging
      if (!dhtWorking) {
          Serial.println("DHT11 sensor is not working correctly!");
      }
      if (!raindropWorking) {
          Serial.println("Raindrop sensor (analog) is not working correctly!");
      }
      if (!ldrWorking) {
          Serial.println("LDR sensor is not working correctly!");
      }
      if (!mq135Working) {
          Serial.println("MQ-135 sensor (analog) is not working correctly!");
      }
      // Generate data
      String data = String(temperature) + "," + String(humidity) + "," + String(raindropValue) + "," +
                    String(ldrValue) + "," + String(mq135Value) + "," +
                    String(mq135DigitalState) + "," + String(raindropDigitalState) + "\n";

      // Send data to client
      client.print(data);
      Serial.println("Data sent to client: " + data);

      // Wait
      delay(1000);
    }

    // Close connection
    client.stop();
    Serial.println("Client disconnected");
  }
}
