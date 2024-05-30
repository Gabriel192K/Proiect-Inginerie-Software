#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; // I2C

char data[32];

void setup(void)
{
	Serial.begin(9600);
	const uint8_t status = bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID);
	if (!status)
		while(1);
	/* Default settings from datasheet. */
  	bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop(void)
{
	int temperature = bmp.readTemperature();
	int pressure = bmp.readPressure() / 1000;
	int altitude = bmp.readAltitude(1013.25);
	sprintf(data, "%d,%d,%d\n", temperature, pressure, altitude);
	Serial.print(data);
	delay(1000);
}
