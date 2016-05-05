/*

Phant-IO
	Shows how to use Phant Ciao Connector for Arduino Ciao Library.
	Reads values from two analog sensors every 5 seconds and push them to
	Phant.io service.

How To:
	You can use "Arduino Phant Ciao Connector Test" Data Stream, a public
	data stream already set and configured for testing purpose or set up
	your own Data Stream at http://data.sparkfun.com/streams/make.

Available Fields on data.sparkfun:
	- foo_sensor
	- bar_sensor

Arduino Testing Data Stream Url:
	you can see your pushed data here: http://data.sparkfun.com/arduino_ciao_phant


Note: Please don't change Data Stream settings to allow all the users to
	use this example.
	Thank You

authors:
	created 8 Oct 2015 - giuseppe arrigo
	edited 5 Mag 2016 - sergio tomasello

*/

#include <Ciao.h>

// named constant for the pin the sensor is connected to
const int sensorFooPin = A0;
const int sensorBarPin = A1;

// Data Stream Keys
String PhantPublicKey = "9J0x4dN9b4iWMwj70ZpN";//<-- Phant.io Public Key - change with you own if set up your Data Stream
String PhantPrivateKey= "xz5XjAKpvjtZ89WYNqzB";//<-- Phant.io Private Key - change with you own if set up your Data Stream

// Data Stream Fields
String PhantFieldFoo="foo_sensor";
String PhantFieldBar="bar_sensor";

void setup() {
	Ciao.begin();
}

void loop() {

	// read the value on AnalogIn pins
	int valueFoo = analogRead(sensorFooPin);
	int valueBar = analogRead(sensorBarPin);

	// push data to phant data stream
	String PhantData = PhantFieldFoo + "=" + String(valueFoo) + ";" + PhantFieldBar + "=" + String(valueBar);
	Ciao.write("phant", PhantPublicKey, PhantPrivateKey, PhantData );

	delay(5000);

}
