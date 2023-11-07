# DHT-TempAPI
A Raspberry PI, DHT 22 Sensor, FLASK Powered Python Script.


#Configure:
Change Pin Settings Depending on Pi version
Install dependencies, including the DHT Raspberry Pi Driver.
Change Ports of Flask if needed, or change what IP it listens on.
Adjust timer, for how often it refreshes.



# Concerns..
This App / Pi driver.. doesn't work great sometimes..

Key Points. When it first starts up, it doesn't do the Polling of the Sensor. So it will take until the Timer finally fires. Then with more detailed below, sensor timing issues. It can take 30s-2 minutes before the data is loaded into the cache.. Until that time the API call will return 500. 

So the Pi DHT driver, will attempt to Retry up to ~15 times. Every 2 seconds. If all attempts fail (Which often happens).
It will be detected in the Try/ Catch. Where you'll see an error get thrown.  ">> Sensor Timeout (This is expected).. Retrying in 3 seconds.. - Retires: 0"
Which means, The Pi DHT Driver timed out. So the app will retry the sensor.

It will warn / give a count for how many retires there has been. But it won't stop retrying the sensor.

# How to use:
Startup app, (require python 3, flask, DHT raspberry pi Libraries)
Once running, goto endpoint <raspberrypi_IP_Address>/itemps

For Auto-start / Restart when crashed.. Can be added to systemd
1. Create folder in /etc/systemd/system/
2. `sudo nano pi-tempapi.service`
3. Paste Config from pi.tempapi.service in Repo.
4. `sudo chmod 755 pi-tempapi.service`
5. `sudo chown root:root pi-tempapi.service`
6. `sudo systemctl daemon-reload`
7. `sudo systemctl enable pi-tempapi.service`
8. `sudo systemctl start pi-tempapi.service`

If it crashes or doesn't start. Run Manually with python3 tempPAI.py or check:
1. `sudo systemctl -u pi-tempapi.service`
2. `sudo systemctl info pi-tempapi.service`
3. `sudo systemctl status pi-tempapi.service`

Hopefully that's all it will take. GL
