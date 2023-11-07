# DHT-TempAPI
A Raspberry PI; DHT 22 Temp/Humidity API Endpoint

# Description
This is an API Endpoint, that returns Temperature / Humidity in Json format.
It allows for easy integration with Home Assistant, or Grafana (with some timestamp changes)
Uses basic caching of data. So if the DHT 22 Driver fails, or times out (Which, can often happen). It won't return null or empty values in the Json values.
Farily consistant / reliable. Is being used on a very old RaspberryPi model b, so some new models may have issues. 
Can be easily changed to use DHT11. But... discourage, as DHT22 has +-1 degree. Vs +-5 degree for the DHT11.

## Concerns / issues
This App / Pi driver.. doesn't work great sometimes..

Key Points. When it first starts up, it doesn't do the Polling of the Sensor. So it will take until the Timer finally fires. Then with more detailed below, sensor timing issues. It can take 30s-2 minutes before the data is loaded into the cache.. Until that time the API call will return 500. 

So the Pi DHT driver, will attempt to Retry up to ~15 times. Every 2 seconds. If all attempts fail (Which often happens).
It will be detected in the Try/ Catch. Where you'll see an error get thrown.  ">> Sensor Timeout (This is expected).. Retrying in 3 seconds.. - Retires: 0"
Which means, The Pi DHT Driver timed out. So the app will retry the sensor.

It will warn / give a count for how many retires there has been. But it won't stop retrying the sensor.

## Configure:
Change Pin Settings, or change code pin assignment. Depending on Pi version
Install dependencies, including the DHT Raspberry Pi Driver.
Change Ports of Flask if needed, or change what IP it listens on.
Adjust timer, for how often it refreshes / retries.


# How to use:
Startup app: `python3 tempAPI.py` (require python 3, flask, DHT raspberry pi Libraries etc)
Once running, goto endpoint <raspberrypi_IP_Address>/itemps

For Auto-start / Restart when crashed.. Can be added to systemd
1. Can install anywhere you want. But Systemd file points to /opt/DHT/tempAPI.py - Change this if you plan on installing somewhere else.
2. Create config File, or copy paste from repo, place in /etc/systemd/system/
3. `sudo nano /etc/systemd/system/pi-tempapi.service`
4. Paste Config from pi.tempapi.service in Repo.
5. `sudo chmod 755 pi-tempapi.service`          - Allow it to be executed / read, execute.
6. `sudo chown root:root pi-tempapi.service`    - Change to Root fowner
7. `sudo systemctl daemon-reload`
8. `sudo systemctl enable pi-tempapi.service`
9. `sudo systemctl start pi-tempapi.service`

If it crashes or doesn't start. Run Manually with `python3 tempPAI.py` or check:
1. `sudo systemctl -u pi-tempapi.service`
2. `sudo systemctl info pi-tempapi.service`
3. `sudo systemctl status pi-tempapi.service`

Hopefully that's all it will take. GL
