import network # Library to connect WiFi
import socket # Library for communication
import time # Library for time and delays
import machine # Library to control GPIO and hardware
import urequests  # Library for making HTTP requests
from machine import I2C, Pin 
from ssd1306 import SSD1306_I2C # Libraries for OLED screen

# My WiFi info
ssid = "your_wifi_name"
password = "your_wifi_password"

# My Adafruit IO info
AIO_USERNAME = "your_adafruit_username"
AIO_KEY = "your_adafruit_key"
AIO_BASE_URL = f"https://io.adafruit.com/api/v2/{AIO_USERNAME}/feeds"

# Feeds' names
TEMP_FEED = "temperature"
HUM_FEED = "humidity"
RAIN_FEED = "rain-possibility"
LDR_FEED = "ldr"
AIR_QUALITY_FEED = "air-quality"

# Initialize OLED display
WIDTH = 128
HEIGHT = 64
i2c = machine.SoftI2C(scl=Pin(15), sda=Pin(4))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# LED pins
RED_LED = Pin(18, Pin.OUT)
GREEN_LED = Pin(19, Pin.OUT)
BLUE_LED = Pin(20, Pin.OUT)

# Turn off all LEDs
def turn_off_leds():
    RED_LED.value(0)
    GREEN_LED.value(0)
    BLUE_LED.value(0)

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        time.sleep(1)
        print("Connecting to WiFi...")
    
    print("Connected to WiFi")
    print("IP address:", wlan.ifconfig()[0])

# Publish data to Adafruit IO using REST API
def publish_data(feed, value):
    url = f"{AIO_BASE_URL}/{feed}/data"
    headers = {"X-AIO-Key": AIO_KEY, "Content-Type": "application/json"}
    data = {"value": value}
    response = urequests.post(url, json=data, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        print(f"Published to {feed}: {value}")
    else:
        print(f"Failed to publish to {feed}: {response.text}")
    response.close()

# Connect to ESP32 server and fetch data
def fetch_data_from_esp32_persistent():
    addr = socket.getaddrinfo('192.168.112.125', 8080)[0][-1]
    s = socket.socket()
    s.settimeout(10)  # 10 second timeout for connection and data reception
    try:
        s.connect(addr)
        s.send(b'Hello ESP32')  # Request data from server
        data = s.recv(1024)     # Get data from server
        if data:
            print("Data received from server:", data.decode())
            return data.decode().split(',')
    except OSError as e:
        print("Error fetching data:", e)
    finally:
        print("Closing socket")
        s.close()  # Close connection
    return None




# Main loop
def main():
    connect_wifi()
    
    while True:
        sensor_data = fetch_data_from_esp32_persistent()
        
        if sensor_data:
            temp = float(sensor_data[0])
            hum = sensor_data[1]
            raindrop_value = int(sensor_data[2])
            ldr_value = int(sensor_data[3])
            mq135_value = int(sensor_data[4])
            
            # Display data on OLED
            oled.fill(0)
            oled.text(f"Temp: {temp:.1f} C", 0, 10)
            oled.text(f"Humidity: {hum} %", 0, 20)
            oled.text(f"Rain: {'Yes' if raindrop_value < 3000 else 'No'}", 0, 30)
            oled.text(f"Light: {'Night' if ldr_value > 3000 else 'Daytime'}", 0, 40)
            oled.text(f"Air Q: {'Good' if mq135_value < 1000 else 'Bad'}", 0, 50)
            oled.show()
            
            # Convert analog values
            nraindrop_value = 100 - ((raindrop_value - 0) / 4095) * 100
            print(nraindrop_value)
            nldr_value = 100 - (((ldr_value - 0) / 4095) * 100)
            print(nldr_value)
            nmq135_value = ((mq135_value - 0) / 4095) * 100
            print(nmq135_value)
            
            # Publish data to Adafruit IO
            publish_data(TEMP_FEED, temp)
            publish_data(HUM_FEED, hum)
            publish_data(RAIN_FEED, nraindrop_value)
            publish_data(LDR_FEED, nldr_value)
            publish_data(AIR_QUALITY_FEED, nmq135_value)
            
            # LED logic
            turn_off_leds()
            if raindrop_value < 3000: # if there is rain blink BLUE twice
                BLUE_LED.value(1)
                time.sleep(1)
                BLUE_LED.value(0)
                time.sleep(0.5)
                BLUE_LED.value(1)
                time.sleep(1)
                BLUE_LED.value(0)
            turn_off_leds()
            if temp > 30: # if too hot blink GREEN twice
                GREEN_LED.value(1)
                time.sleep(1)
                GREEN_LED.value(0)
                time.sleep(0.5)
                GREEN_LED.value(1)
                time.sleep(1)
                GREEN_LED.value(0)
            turn_off_leds()
            if temp < 20: # if too cold blink BLUE and GREEN once
                BLUE_LED.value(1)
                GREEN_LED.value(1)
                time.sleep(1)
                BLUE_LED.value(0)
                GREEN_LED.value(0)
                time.sleep(0.5)
            turn_off_leds()
            if 20 <= temp <= 30: # if air condition normal blink RED twice
                RED_LED.value(1)
                time.sleep(1)
                RED_LED.value(0)
                time.sleep(0.5)
                RED_LED.value(1)
                time.sleep(1)
                RED_LED.value(0)
            turn_off_leds()
            if mq135_value > 1000: # if air quailty bad blink BLUE, RED and GREEN
                BLUE_LED.value(1)
                RED_LED.value(1)
                GREEN_LED.value(1)
                time.sleep(1)
                BLUE_LED.value(0)
                RED_LED.value(0)
                GREEN_LED.value(0)
            turn_off_leds()
            if mq135_value < 1000: # if air quailty good blink BLUE and RED
                BLUE_LED.value(1)
                RED_LED.value(1)
                time.sleep(1)
                BLUE_LED.value(0)
                RED_LED.value(0)
        else:
            turn_off_leds()

        time.sleep(10)

# Run the program
main()

