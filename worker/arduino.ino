
#define R_PIN 3
#define G_PIN 9
#define B_PIN 10
#define R_CALIBRATION_COEFFICIENT 0.3125
#define G_CALIBRATION_COEFFICIENT 0.4347
#define B_CALIBRATION_COEFFICIENT 0.85

struct RGBData
{
  byte red;
  byte green;
  byte blue;
};

String x;
RGBData rgb_data;
RGBData rgb_data_old;
bool first_iter = true;

void setup()
{
  // initialize pinout
  pinMode(R_PIN, OUTPUT);
  pinMode(G_PIN, OUTPUT);
  pinMode(B_PIN, OUTPUT);
  Serial.begin(9600);

  while (!Serial)
    ;
  delay(10);
}

void loop()
{
  if (Serial.available() == 0)
  {
    delay(10);
    return;
  }
  x = Serial.readStringUntil('E');
  if (x.startsWith("H"))
  {
    Serial.print(x + "E");
    return;
  }
  rgb_data = parse_rgbdata_from_string(x);

  if (first_iter)
  {
    first_iter = false;
    memcpy(&rgb_data_old, &rgb_data, sizeof(RGBData));
    set_rgb_value(rgb_data);
    Serial.println("Done!");
    return;
  }

  fade(rgb_data, rgb_data_old, 100);
  memcpy(&rgb_data_old, &rgb_data, sizeof(RGBData));
  delay(100);
  Serial.println("Done!");
}

void fade(const RGBData &new_data, const RGBData &old_data, byte number_of_iterations)
{
  float difference[3];

  difference[0] = (1.0 * ((int)new_data.red - (int)old_data.red)) / (int)number_of_iterations;
  difference[1] = (1.0 * ((int)new_data.green - (int)old_data.green)) / (int)number_of_iterations;
  difference[2] = (1.0 * ((int)new_data.blue - (int)old_data.blue)) / (int)number_of_iterations;

  for (byte i = 0; i < number_of_iterations; i++)
  {
    RGBData faded = {
        old_data.red + floor(i * difference[0]),
        old_data.green + floor(i * difference[1]),
        old_data.blue + floor(i * difference[2]),
    };
    set_rgb_value(faded);
    delay(10);
  }
}

void set_rgb_value(const RGBData &data)
{
  analogWrite(R_PIN, floor(data.red * R_CALIBRATION_COEFFICIENT));
  analogWrite(G_PIN, floor(data.green * G_CALIBRATION_COEFFICIENT));
  analogWrite(B_PIN, floor(data.blue * B_CALIBRATION_COEFFICIENT));
}

RGBData parse_rgbdata_from_string(const String &data)
{
  RGBData temp;
  temp.red = (byte)(x.substring(x.indexOf('r') + 1, x.indexOf('g') + 1).toInt());
  temp.green = (byte)x.substring(x.indexOf('g') + 1, x.indexOf('b') + 1).toInt();
  temp.blue = (byte)x.substring(x.indexOf('b') + 1, x.indexOf('E')).toInt();
  return temp;
}