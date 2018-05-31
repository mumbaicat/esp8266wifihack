#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>

// char ssid[] = "esp8266-cp";            // your network SSID (name)
// char pass[] = "12345678";

String ssid = "123";
String xxx = "23";
int indexx = 0;
String message = "123";
String comdata = "";

int commaPosition;

const byte DNS_PORT = 53;
IPAddress apIP(192, 168, 1, 1);
DNSServer dnsServer;
ESP8266WebServer webServer(80);

String responseHTML = ""
                      "<!DOCTYPE html>"
                      "<html><head>"
                      "<meta charset='utf-8'><title>广告</title>"
                      "<meta name='viewport' content='width=device-width, initial-scale=1'>"
                      "</head><body>"
                      "<h1>常年招租广告位</h1>"
                      "<p>还不快来 2333</p>"
                      "</body></html>";

void setup() {
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
  WiFi.softAP("esp8266-CP", "12345678");

  // if DNSServer is started with "*" for domain name, it will reply with
  // provided IP to all DNS request
  dnsServer.start(DNS_PORT, "*", apIP);

  // replay to all requests with same HTML
  webServer.onNotFound([]() {
    webServer.send(200, "text/html", responseHTML);
  });
  webServer.begin();
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {


  while (Serial.available() > 0) {
    comdata += char(Serial.read());  //每次读一个char字符，并相加
    delay(2);
  }
  if (comdata.length() > 0) {
    // Serial.println(comdata); //打印接收到的字符
    message = comdata;
    do {
      commaPosition = message.indexOf(',');
      if (commaPosition != -1)
      {
        indexx ++ ;
        Serial.println(indexx);
        xxx = message.substring(0, commaPosition);
        if(indexx == 1){
          ssid = xxx;
        }
        if(indexx == 2){
          // pass = xxx;
          WiFi.softAP(ssid);  
        }
        Serial.println(xxx);
        message = message.substring(commaPosition + 1, message.length());
      }
      else {
        if (message.length() > 0) {
          if (indexx != 0) {
            indexx ++ ;
            Serial.println(indexx);
          }
          Serial.println(message);

        }
      }
    }
    while (commaPosition >= 0);
    indexx = 0;

    // WiFi.softAP(ssid,pass);
    comdata = "";
    digitalWrite(LED_BUILTIN, LOW);
    delay(300);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(300);
  }





  dnsServer.processNextRequest();
  webServer.handleClient();


}
