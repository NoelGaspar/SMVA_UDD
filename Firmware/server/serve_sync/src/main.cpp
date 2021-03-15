/*

Server sync esp32

Description:

Author: WAC@iowlab

cmd:
  0: idle
  1: start sens
  2: stop sens

*/


/*
------------------------------------
 Libs and includes
 ------------------------------------
*/
#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>

/*
------------------------------------
 Defines and vars
 ------------------------------------
*/

//PINs
#define TRIGGER_PIN 12
#define TESTLED_PIN 2
//CMDs
#define CMD_TRIGGER 1
#define CMD_STOP    2
#define CMD_START   3
#define CMD_IDLE    0

//Recivers MACs

uint8_t SensorAddr1[] = {0x7C,0x9E,0xBD,0xF4,0xF3,0x54};
//uint8_t SensorAddr1[] = {0x24,0x6F,0x28,0xAA,0xB3,0x64};
uint8_t SensorAddr2[] = {0x24,0x6F,0x28,0xAA,0x0C,0x13};

//Command structure
typedef struct cmd_struct
{
  uint8_t cmd;  
} cmd_struct;
cmd_struct cmd;

/*
------------------------------------
 Functions
 ------------------------------------
*/
void sendCallback(const uint8_t *mac_addr, esp_now_send_status_t status) ;
void processCMD(int msg);

void setup() 
{
  Serial.begin(115200);
  pinMode(TESTLED_PIN,OUTPUT);

  WiFi.mode(WIFI_STA);
  if (esp_now_init() != ESP_OK)
  {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_send_cb(sendCallback); //assign callback to send flag

  // register peer
  esp_now_peer_info_t peerInfo;
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // register first peer  
  memcpy(peerInfo.peer_addr, SensorAddr1, 6);
  if (esp_now_add_peer(&peerInfo) != ESP_OK)
  {
    Serial.println("Failed to add peer");
    return;
  }
  
  // register second peer  
  memcpy(peerInfo.peer_addr, SensorAddr2, 6);
  if (esp_now_add_peer(&peerInfo) != ESP_OK)
  {
    Serial.println("Failed to add peer");
    return;
  }
}

void loop() 
{
  if(Serial.available())
  {
    processCMD(Serial.read());
  }
}

void sendCallback(const uint8_t *mac_addr, esp_now_send_status_t status) 
{
  char macStr[18];
  Serial.print("Packet to: ");
  // Copies the sender mac address to a string
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.print(macStr);
  Serial.print(" send status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

void processCMD(int msg)
{
  
  switch (msg)
  {
  case '1':
    cmd.cmd = CMD_TRIGGER;
    digitalWrite(TESTLED_PIN,1);
    break;
  case '2':
    cmd.cmd = CMD_STOP;
    digitalWrite(TESTLED_PIN,1);
    break;
  case '3':
    cmd.cmd = CMD_START;
    digitalWrite(TESTLED_PIN,1);
    break;
  default:
    cmd.cmd = CMD_IDLE;
    digitalWrite(TESTLED_PIN,0);
    break;
  }

  Serial.print("Message to broadcast : ");
  Serial.println(cmd.cmd);
  esp_err_t result = esp_now_send(0, (uint8_t *) &cmd, sizeof(cmd_struct));
  Serial.println((result==ESP_OK)?"Sent with success":"Error sending the data");
}