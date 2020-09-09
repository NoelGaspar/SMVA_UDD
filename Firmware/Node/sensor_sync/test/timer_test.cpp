/*
Code to test timers on esp32

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

//PINs
#define TESTLED_PIN 2
//CMDs
#define CMD_STOP    1
#define CMD_START   2
#define CMD_IDLE    3

/*
Variables and structures
*/
//Command structure
uint8_t cmd;
bool recv_CMD_Flag = false;

// TIMERS
bool trigger_state = false;
hw_timer_t * timer = NULL;

/*
------------------------------------
 Functions
 ------------------------------------
*/
void IRAM_ATTR timerISR();

void setup() {
  
    Serial.begin(115200);
    pinMode(TESTLED_PIN, OUTPUT);
    digitalWrite(TESTLED_PIN,0);

    Serial.println("Starting");

    //setup Timer
    timer = timerBegin(3, 8000, true);    // params: n timer, prescaler, up or down // f_{timer source clock} = f_mclk/prescaler = 80MHz/8000 = 10kHz
    timerAttachInterrupt(timer,&timerISR,true); //params: timer object, pointer to ISR function anddress, mode edge (if false: level mode)
    timerAlarmWrite(timer, 50000,true);   // params: timer object, counter_limit, restart counter on top.// to get T= 1s, n=T*f_{timer source clock}
    timerAlarmEnable(timer);              // enable CTC mode
    timerStop(timer);                     //start timer off
}
 
void loop()
{
    if(Serial.available())
    {
        cmd = Serial.read();
    }
    if(cmd == 's')
    {
        timerStop(timer);
    }
    else if(cmd == 'p')
    {
        timerStop(timer);
    }
    cmd = 'd';// dummy to keep actual state
}//LOOP END


//Timer ISR
void IRAM_ATTR timerISR()
{
  trigger_state = !trigger_state;
  digitalWrite(TESTLED_PIN,trigger_state);
}