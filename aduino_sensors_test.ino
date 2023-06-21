// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"

#define DHTPIN 2     // what pin we're connected to
#define red 9
#define green 10
#define blue 11
// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11 
//#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Initialize DHT sensor for normal 16mhz Arduino
DHT dht(DHTPIN, DHTTYPE);

// 수분수위센서
int water_pin = A5;
int LED2 = 3;

// RGB LED
//int red = 9;
//int green = 10;
//int blue = 11;

void setup() {
  Serial.begin(9600); 
  Serial.println("DHTxx test!");
 
  dht.begin();
  pinMode(3, OUTPUT);
  // 3색 LED의 각 핀을 OUTPUT으로 설정합니다.
	pinMode(red, OUTPUT);
	pinMode(green, OUTPUT);
	pinMode(blue, OUTPUT);
}

void loop() {
  // Wait a few seconds between measurements.
  delay(10000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit
  float f = dht.readTemperature(true);
  // 조도센서
  int val;
  val=analogRead(0);
  // 수분수위센서
  int water_val; 
  char rain = "RAIN!!";
  char norain = "dry";
  water_val = analogRead(A5);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index
  // Must send in temp in Fahrenheit!
  float hi = dht.computeHeatIndex(f, h);

  Serial.print("Humidity: "); 
  Serial.print(h);
  Serial.print(" % ");
  Serial.print("Temperature: "); 
  Serial.print(t);
  Serial.print(" *C ");
  Serial.print(f);
  Serial.print(" *F");
  Serial.print("Heat index: ");
  Serial.print(hi);
  Serial.print(" *F ");
  Serial.print(" Rain:");
  if (water_val > 400){
  digitalWrite(red, HIGH);  
  //delay(9000);
  Serial.print("RAIN!!");
  }
  else {
  Serial.print("DRY");
  digitalWrite(green, HIGH); 
  //delay(1000);  
  }
  Serial.print(" Light index: ");
  Serial.println(val,DEC);
}