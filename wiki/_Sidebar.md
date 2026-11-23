### [[Home]]

---

### Hardware
* [[Pre-assembled boxes|Pre-assembled-Boxes]]
* [[Components]]
* [[Motor control with GPIO|Motor-Control-with-GPIO]]

---

### Installation
* [[Installation guide|Installation-Guide]]
  * [Download the right image](/olliemaller/ESPSomfy-RTS/wiki/Installation-Guide#3-download-the-right-image)
  * [Flash over USB](/olliemaller/ESPSomfy-RTS/wiki/Installation-Guide#5-flash-over-usb)
  * [First start-up](/olliemaller/ESPSomfy-RTS/wiki/Installation-Guide#6-first-start-up)
  * [Coming from rstrouse's firmware](/olliemaller/ESPSomfy-RTS/wiki/Installation-Guide#7-if-you-were-on-rstrouses-firmware)

---

[Factory Reset](/olliemaller/ESPSomfy-RTS/wiki/Factory-Reset)

[Serial monitor](/olliemaller/ESPSomfy-RTS/wiki/Serial-Monitor)

[Backup file anatomy](/olliemaller/ESPSomfy-RTS/wiki/Backup-File-Anatomy)

---

* [[Dashboard]]
  * [Device cards](Dashboard#8-device-cards)
  * [The two sliding windows](Dashboard#9-the-two-sliding-windows)

---

### 💻 Interface configuration
* **System setup**
  * [[Options]]
  * [[Security]]
  * [[Firmware]]
    * [Backup and restore](Firmware#backup-and-restore)
  * [[Updating]]
    * [The files in a release](Updating#2-the-files-in-a-release)
    * [GitHub Update](Updating#3-github-update)
    * [Moving between v2.x.x and v3](Updating#moving-between-v2xx-and-v3)
* **Network setup**
  * [[Network connection|Network-Connection]]
    * [WI-FI](/olliemaller/ESPSomfy-RTS/wiki/Network-Connection#using-a-wi-fi-connection)
    * [Ethernet](/olliemaller/ESPSomfy-RTS/wiki/Network-Connection#using-an-ethernet-connection)
    * [Wi-Fi troubleshooting](/olliemaller/ESPSomfy-RTS/wiki/Network-Connection#the-device-wont-join-my-wi-fi)
  * [DHCP / Static IP](/olliemaller/ESPSomfy-RTS/wiki/DHCP-and-Static-IP)
    * [DHCP reservation](/olliemaller/ESPSomfy-RTS/wiki/DHCP-and-Static-IP#the-right-way-a-dhcp-reservation)
    * [Static IP](/olliemaller/ESPSomfy-RTS/wiki/DHCP-and-Static-IP#static-ip-advanced-users)
* **Somfy setup**
  * [[Rooms]]
  * [[Devices]]
    * [Travel times](/olliemaller/ESPSomfy-RTS/wiki/Devices#3-travel-times)
    * [Pairing the motor](/olliemaller/ESPSomfy-RTS/wiki/Devices#5-pairing-the-motor)
    * [Linking your remotes](/olliemaller/ESPSomfy-RTS/wiki/Devices#6-linking-your-physical-remotes)
    * [Linking a sensor](/olliemaller/ESPSomfy-RTS/wiki/Devices#7-linking-a-sensor)
    * [Setting the rolling code](/olliemaller/ESPSomfy-RTS/wiki/Devices#8-setting-the-rolling-code)
  * [[Groups]]
    * [Creating a group](/olliemaller/ESPSomfy-RTS/wiki/Groups#2-creating-a-group)
    * [The settings](/olliemaller/ESPSomfy-RTS/wiki/Groups#3-the-settings)
    * [Linking a device](/olliemaller/ESPSomfy-RTS/wiki/Groups#4-linking-a-device)
    * [Removing a device](/olliemaller/ESPSomfy-RTS/wiki/Groups#5-removing-a-device)
  * [[Repeaters]]
  * [[Virtual Remote|Virtual-Remote]]
* **Radio setup**
  * [[Radio setup|Radio-Setup]]
    * [GPIO Assignment](Radio-Setup#gpio-assignment)
    * [Tuning the radio](Radio-Setup#tuning-the-radio)
    * [Example: 6 out of 8 respond](Radio-Setup#example-6-out-of-8-devices-respond)
  * [[Radio logs|Radio-Logs]]
    * [Identifying the protocol](Radio-Logs#identifying-the-protocol-bits-column)
    * [Troubleshooting](Radio-Logs#troubleshooting-guide)
  * [[Frequency scan|Frequency-Scan]]

---

### Integration
* **[[Integrations]]**
  * [Connectivity options](Integrations#connectivity-options-available)
  * [REST API](Integrations#rest-interface-api)
* **[[MQTT]]**
  * [Published topics](MQTT#published-topics)
  * [Subscribed topics](MQTT#subscribed-topics)
  * [Auto-discovery](MQTT#mqtt-auto-discovery)
* **[[Home Assistant|Home-Assistant]]**
  * [Installing via HACS](Home-Assistant#installation-via-hacs)
  * [rstrouse's integration](Home-Assistant#compatibility-with-rstrouses-integration-espsomfy-rts-ha)
