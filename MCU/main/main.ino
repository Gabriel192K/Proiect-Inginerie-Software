/* Dependencies */
#include <Adafruit_BMP280.h>

/* Macros */
#define PACKET_MANAGER_START_BYTE (const uint8_t)0x02
#define PACKET_MANAGER_STOP_BYTE  (const uint8_t)0x03

/* Objects */
Adafruit_BMP280 bmp; // I2C

/* Prototypes */
void sendPacket(void);

void setup(void)
{
	Serial.begin(9600);
	const uint8_t status = bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID);
	if (!status)
		while(1);
	/* Default settings from datasheet. */
  	bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,   /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop(void)
{
	sendPacket()
	delay(1000);
}

void sendPacket(void)
{
	const uint8_t temperature = bmp.readTemperature();
	const uint8_t pressure = bmp.readPressure() / 1000;
	const uint16_t altitude = bmp.readAltitude(1013.25);

	Serial.write(PACKET_MANAGER_START_BYTE);
	Serial.write(temperature);
	Serial.write(pressure);
	Serial.write((const uint8_t)altitude);
	Serial.write((const uint8_t)(altitude >> 8));
	Serial.write(PACKET_MANAGER_STOP_BYTE);
}
