/*
sensor side sync esp32

Description:

Author: WAC@iowlab

cmd:
  0: idle
  1: trigger 1 adquisition rutine
  2: start to sens
  3: stop to sens

TODO

*/
#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>

//PINs
#define TRIGGER_PIN 12
#define TESTLED_PIN 2
//CMDs
#define CMD_TRIGGER 1
#define CMD_STOP    2
#define CMD_START   3
#define CMD_IDLE    0
//
#define TRIGGER_PULSE_TIME 5000 //ms
#define ADQUISITION_PULSE_TIME 500 //ms

/*
Variables and structures
*/
//Command structure
typedef struct cmd_struct
{
  uint8_t cmd;  
} cmd_struct;
cmd_struct cmd;

bool recv_CMD_Flag = false;

// TIMERS
int trigger_counter;
bool trigger_state = false;
int counter;
hw_timer_t * timer = NULL;

/*
------------------------------------
 Functions
 ------------------------------------
*/
//callback function that will be executed when data is received
void reciveCallBack(const uint8_t * mac, const uint8_t *incomingData, int len);
void IRAM_ATTR timerISR();

void setup() {
  
  Serial.begin(115200);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(TESTLED_PIN, OUTPUT);
  digitalWrite(TESTLED_PIN,0);
  digitalWrite(TRIGGER_PIN,0);
  Serial.println("Starting");

  WiFi.mode(WIFI_STA);
  Serial.println("Wifi connected ... OK");
  
  if (esp_now_init() != ESP_OK)
  {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  Serial.println("initialization ESP-NOW ... OK");
  
  esp_now_register_recv_cb(reciveCallBack); //attach the callback send function

  //TIMER
  timer = timerBegin(3, 8000, true); //We try timers interrupt on 3erd timer // 80MHz/8000 = 10kHz
  timerAttachInterrupt(timer,&timerISR,true); // timer object, pointer to ISR function anddress, mode edge (if false: level mode)
  timerAlarmWrite(timer, 50000,true);
  timerAlarmEnable(timer);
  timerStop(timer);
}
 
void loop()
{
  if(recv_CMD_Flag)
  {
    switch (cmd.cmd)
    {
      case CMD_TRIGGER: // one single pulse
        timerStop(timer);
        digitalWrite(TESTLED_PIN,1);
        digitalWrite(TRIGGER_PIN,1);
        delay(TRIGGER_PULSE_TIME);
        digitalWrite(TESTLED_PIN,0);
        digitalWrite(TRIGGER_PIN,0);
        cmd.cmd = CMD_IDLE;
        break;
      case CMD_START:
        timerRestart(timer);
        break;
      case CMD_STOP:
        digitalWrite(TESTLED_PIN,0);
        digitalWrite(TRIGGER_PIN,0);
        timerStop(timer);
        break;
      case CMD_IDLE:
        digitalWrite(TESTLED_PIN,0);
        digitalWrite(TRIGGER_PIN,0);
        timerStop(timer);
        break;
      default:
        digitalWrite(TESTLED_PIN,0);
        digitalWrite(TRIGGER_PIN,0);
        //Timer stop to pulse
        timerStop(timer);
        break;
    }//SWITCH END
    recv_CMD_Flag = false;    
  }//IF END
}//LOOP END

void reciveCallBack(const uint8_t * mac, const uint8_t *incomingData, int len)
{
  memcpy(&cmd, incomingData, sizeof(cmd));
  Serial.print("cmd recived: ");
  Serial.println(cmd.cmd);
  recv_CMD_Flag = true;
}

//Timer ISR
void IRAM_ATTR timerISR()
{
  trigger_state = !trigger_state;
  digitalWrite(TRIGGER_PIN,trigger_state);
  digitalWrite(TESTLED_PIN,trigger_state);
}