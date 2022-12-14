#include <Arduino.h>

unsigned long timer = 0;
long loopTime = 150;   // microseconds
unsigned long prev_time = 0;
unsigned long curr_time = 0;


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

void sendToPC(int* data1, int* data2, int* data3, int* data4)
{
  byte* byteData1 = (byte*)(data1);
  byte* byteData2 = (byte*)(data2);
  byte* byteData3 = (byte*)(data3);
  byte* byteData4 = (byte*)(data4);

  byte buf[8] = {byteData1[0], byteData1[1],
                 byteData2[0], byteData2[1],
                 byteData3[0], byteData3[1],
                 byteData4[0], byteData4[1]};
  Serial.write(buf, 8);
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

  //double val1 = (analogRead(21) -512) / 512.0;
  //double val2 = (analogRead(22) -512) / 512.0;
  //double val3 = (analogRead(23) -512) / 512.0;

  sendToPC(&val1, &val2, &val3, &delta_t);
}