# SSD1306-Minimal
Custom driver for the SSD1306 family of screens written in MicroPython. Designed to have a smaller memory footprint than the official driver. Can be integrated directly into your code or uploaded to your board as a separate file. Currently only supports I2C, however I am working on an SPI version as well.

I created this driver after I was having trouble running the official driver on my RP2040 & ESP32 boards. After some failed troubleshooting I took it upon myself to make my own driver so I could understand exactly how everything worked and implement whatver features I required.

| Parameter | Specification |
| :--- | :--- |
| **Firmware Language** | MicroPython |
| **Display** | SSD1306 OLED |
| **Serial Protocol** | I2C |
