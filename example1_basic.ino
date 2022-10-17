/*
  example1-basic
​
  This example shows the basic settings and functions for retrieving accelerometer
	and gyroscopic data. 
	Please refer to the header file for more possible settings, found here:
	..\SparkFun_6DoF_ISM330DHCX_Arduino_Library\src\sfe_ism330dhcx_defs.h
​
  Written by Elias Santistevan @ SparkFun Electronics, August 2022
​
	Product:
​
		https://www.sparkfun.com/products/19764
​
  Repository:
​
		https://github.com/sparkfun/SparkFun_6DoF_ISM330DHCX_Arduino_Library
​
  SparkFun code, firmware, and software is released under the MIT 
	License	(http://opensource.org/licenses/MIT).
*/

#include <Wire.h>
#include "SparkFun_ISM330DHCX.h"
#include <cmath>

SparkFun_ISM330DHCX myISM; 

// Structs for X,Y,Z data
sfe_ism_data_t accelData; 
sfe_ism_data_t gyroData; 


int arr_len = 1000;
float accel_mag;
float accel_vect[3];
float accel[3];
//float array[arr_len][3];
int count = 0;

float array_avg(){
  long x_avg=0;
  long y_avg=0;
  long z_avg=0;
/*
  for (i=0; i<arr_len; i++){
    x_avg += array[i][0];
    y_avg += array[i][1];
  }
  */
}

void setup(){

	Wire.begin();

	Serial.begin(115200);

	if( !myISM.begin() ){
		Serial.println("Did not begin.");
		while(1);
	}

	// Reset the device to default settings. This if helpful is you're doing multiple
	// uploads testing different settings. 
	myISM.deviceReset();

	// Wait for it to finish reseting
	while( !myISM.getDeviceReset() ){ 
		delay(1);
	} 

	Serial.println("Reset.");
	Serial.println("Applying settings.");
	delay(100);
	
	myISM.setDeviceConfig();
	myISM.setBlockDataUpdate();
	
	// Set the output data rate and precision of the accelerometer
	myISM.setAccelDataRate(ISM_XL_ODR_6667Hz);
	myISM.setAccelFullScale(ISM_4g); 

	// Set the output data rate and precision of the gyroscope
	myISM.setGyroDataRate(ISM_XL_ODR_6667Hz);
	myISM.setGyroFullScale(ISM_500dps); 

	// Turn on the accelerometer's filter and apply settings. 
	myISM.setAccelFilterLP2();
	myISM.setAccelSlopeFilter(ISM_LP_ODR_DIV_100);

	// Turn on the gyroscope's filter and apply settings. 
	myISM.setGyroFilterLP1();
	myISM.setGyroLP1Bandwidth(ISM_MEDIUM);


}

int square(int value){
  return value*value;
}

float get_accel_mag(){
  int mag_squared = square(accelData.xData) + square(accelData.yData) + square(accelData.zData);
  accel_mag = sqrt(mag_squared);
  return accel_mag/1000; // convert from milliG to G 
}

float* get_accel_vect(){
  accel_vect[0] = accelData.xData/accel_mag;
  accel_vect[1] = accelData.yData/accel_mag;
  accel_vect[2] = accelData.zData/accel_mag;
  return accel_vect;
}

void print_arr_elem(int i){
  String printstring = String("string to print");
  printstring = "X: " + String(array[i][0]) + " Y: " + String(array[i][1]) + " Z: " + String(array[i][2]);
  Serial.println(printstring);
}

float* get_accel(){
  accel[0] = accelData.xData;
  accel[1] = accelData.yData;
  accel[2] = accelData.zData;
  return accel;
}

void add_to_array(int number){
  array[number][0] = accelData.xData;
  array[number][1] = accelData.yData;
  array[number][2] = accelData.zData;
  
}




/*
long int get_data_array(int counter){
  array[counter] = {accelData.xData, accelData.yData, accelData.zData};

  return array;
}
*/


void loop(){
	// Check if both gyroscope and accelerometer data is available.
	if( myISM.checkStatus() ){
		myISM.getAccel(&accelData);
		myISM.getGyro(&gyroData);
    /*
		Serial.print("X: ");
		Serial.println(accelData.xData);
		Serial.print("Y: ");
		Serial.println(accelData.yData);
		Serial.print("Z: ");
		Serial.println(accelData.zData);
    
    Serial.print("Mag: ");
    Serial.println(get_accel_mag());  
    Serial.print("Unit Vector: ");
    get_accel_vect();
    Serial.print(accel_vect[0]);
    Serial.print(" ");
    Serial.print(accel_vect[1]);
    Serial.print(" ");
    Serial.println(accel_vect[2]); 
    */
   // Serial.println(get_data_array(count));

    //count = count + 1;
    add_to_array(count);

    if (count == arr_len - 1) {
      print_arr_elem(count);
      /*
      Serial.println("x:  ");
      Serial.print(array[0][0]);
      Serial.print(" ");
      Serial.print("y:  ");
      Serial.print(array[0][1]);
      */
      count = 0;
    }
  count++;
	/*
  	Serial.print("Gyroscope: ");
		Serial.print("X: ");
		Serial.print(gyroData.xData);
		Serial.print(" ");
		Serial.print("Y: ");
		Serial.print(gyroData.yData);
		Serial.print(" ");
		Serial.print("Z: ");
		Serial.print(gyroData.zData);
		Serial.println(" ");
  */    
  }
	//delay(1);
}


