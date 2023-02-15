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

