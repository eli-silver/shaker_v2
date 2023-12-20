#include <Arduino.h>
#include <Audio.h>
#include <Wire.h>
#include <SD.h>
#include <SPI.h>
#include <SerialFlash.h>
#include <stdlib.h>

#define x_acc_pin 14
#define y_acc_pin 16
#define z_acc_pin 17

unsigned long timer = 0;
long loopTime = 150;   // microseconds
unsigned long prev_time = 0;
unsigned long curr_time = 0;

int prev_val1=0;
int prev_val2=0;
int prev_val3=0;

int upper_threshold = 100;
int lower_threshold = 70;
int rising = 1;
int camera_trig = 0;

int incomingByte = 0;
int num_bytes = 4;

/*AudioSynthWaveform    waveform1;
AudioOutputI2S        i2s1;
AudioConnection       patchCord1(waveform1, 0, i2s1, 0);
AudioConnection       patchCord2(waveform1, 0, i2s1, 1);
AudioControlSGTL5000  sgtl5000_1;
*/

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
 return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

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
  //Serial.begin(2000000);
  Serial.begin(115200);
  timer = micros();
  pinMode(x_acc_pin, INPUT);
  pinMode(y_acc_pin, INPUT);
  pinMode(z_acc_pin, INPUT);

  //AudioMemory(10);
  //pinMode(13, OUTPUT);
  //sgtl5000_1.enable();
  //sgtl5000_1.volume(0.8);
  //waveform1.begin(WAVEFORM_SINE);
  //pinMode(7, OUTPUT);
  //pinMode(8, OUTPUT);
  //pinMode(9, OUTPUT);
  //digitalWrite(7, HIGH);
  //digitalWrite(8, LOW);
  //digitalWrite(9, LOW);
}

/*
void get_input(){
  int input_buff[num_bytes];
  byte* ddata = reinterpret_cast<byte*>(&input_buff); // pointer for transferData()
  size_t pcDataLen = sizeof(input_buff);
  for (byte n = 0; n < pcDataLen; n++){
    ddata[n] = Serial.read();
  }

  for (int i = 0; i< num_bytes; i++){
    Serial.print(ddata[i]);
    Serial.print(",");
  }
  Serial.println();
}


void parse_input(){

  int amp = Serial.parseInt();
  int freq = 0;

  Serial.print("Amplitude: ");
  Serial.print(amp);
  Serial.print(" Frequency: ");
  Serial.println(freq);

}
*/

void loop() {
    //if (Serial.available() == num_bytes) {
    // read the incoming byte:
    //parse_input();
    //get_input();
    /*incomingByte = Serial.parseInt();

    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
    float byte_to_float = float(incomingByte);
    float amplitude = mapfloat(byte_to_float, 0, 1024, 0, 1);
    waveform1.frequency(220);
    waveform1.amplitude(amplitude);*/
  //}

  timeSync(loopTime);
  int val1 = analogRead(x_acc_pin) - 512;
  int val2 = analogRead(y_acc_pin) - 512;
  int val3 = analogRead(z_acc_pin) - 512;
  curr_time = micros();
  int delta_t = curr_time - prev_time;
  prev_time = curr_time;

  if( val3 >= upper_threshold && rising == 1){
    camera_trig = 1;
    rising = 0;
    //digitalWrite(8, HIGH);
    //digitalWrite(9, HIGH);
  }
  else if( val3 <= lower_threshold && rising == 0){
    camera_trig = 0;
    rising = 1;
    //digitalWrite(8, LOW);
    //digitalWrite(9, LOW);
  }


  //if( rising && prev_val3 < upper_threshold && val3 > upper_threshold ) camera_trig = 1;
  //if( !rising && prev_val3 > lower_threshold && val3 < lower_threshold ) camera_trig = 0;
  
  //double val1 = (analogRead(21) -512) / 512.0;
  //double val2 = (analogRead(22) -512) / 512.0;
  //double val3 = (analogRead(23) -512) / 512.0;

  prev_val1 = val1;
  prev_val2 = val2;
  prev_val3 = val3;

  sendToPC(&val1, &val2, &val3, &delta_t, &camera_trig);
}