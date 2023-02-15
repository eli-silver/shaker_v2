#include <Arduino.h>

unsigned long timer = 0;
long loopTime = 150;   // microseconds
unsigned long prev_time = 0;
unsigned long curr_time = 0;

int prev_val1=0;
int prev_val2=0;
int prev_val3=0;

int upper_threshold = 512;
int lower_threshold = 475;
int rising = 0;
int camera_trig = 0;


void timeSync(unsigned long deltaT)
{
  unsigned long currTime = micros();
  long timeToDelay = deltaT - (currTime - timer);
  if (timeToDelay > 5000)
  {
    delay(timeToDelay / 1000);
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0)
  {
    delayMicroseconds(timeToDelay);
  }
  else
  {
      // timeToDelay is negative so we start immediately
  }
  timer = currTime + timeToDelay;
}

void sendToPC(int* data1, int* data2, int* data3, int* data4, int* data5)
{
  byte* byteData1 = (byte*)(data1);
  byte* byteData2 = (byte*)(data2);
  byte* byteData3 = (byte*)(data3);
  byte* byteData4 = (byte*)(data4);
  byte* byteData5 = (byte*)(data5);

  byte buf[10] = {byteData1[0], byteData1[1],
                 byteData2[0], byteData2[1],
                 byteData3[0], byteData3[1],
                 byteData4[0], byteData4[1],
                 byteData5[0], byteData5[1]};
  Serial.write(buf, 10);
}

void sendToPC(double* data1, double* data2, double* data3)
{
  byte* byteData1 = (byte*)(data1);
  byte* byteData2 = (byte*)(data2);
  byte* byteData3 = (byte*)(data3);
  byte buf[12] = {byteData1[0], byteData1[1], byteData1[2], byteData1[3],
                 byteData2[0], byteData2[1], byteData2[2], byteData2[3],
                 byteData3[0], byteData3[1], byteData3[2], byteData3[3]};
  Serial.write(buf, 12);
}

void setup() {
  Serial.begin(2000000);
  timer = micros();
  pinMode(21, INPUT);
  pinMode(22, INPUT);
  pinMode(23, INPUT);
}

void loop() {
  timeSync(loopTime);
  int val1 = analogRead(21) - 512;
  int val2 = analogRead(22) - 512;
  int val3 = analogRead(23) - 512;
  curr_time = micros();
  int delta_t = curr_time - prev_time;
  prev_time = curr_time;



  if( rising && prev_val3 < upper_threshold && val3 > upper_threshold ) camera_trig = 1;
  if( !rising && prev_val3 > lower_threshold && val3 < lower_threshold ) camera_trig = 0;
  
  //double val1 = (analogRead(21) -512) / 512.0;
  //double val2 = (analogRead(22) -512) / 512.0;
  //double val3 = (analogRead(23) -512) / 512.0;

  prev_val1 = val1;
  prev_val2 = val2;
  prev_val3 = val3;

  sendToPC(&val1, &val2, &val3, &delta_t, &camera_trig);
}