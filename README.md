# Ciao Connector Phant.io
Phant.io Connector for Arduino Ciao - Send data to Phant.io service. [Phant.io](http://phant.io/)
is a cloud service by [SparkFun](https://data.sparkfun.com/)

## Installation
### Linino OS
Open a `secure shell` to your board and login into **Linino OS**.
Install it via `opkg` running this commands:
```
$ opkg update
$ opkg install ciao-connector-phant
```

### Arduino OS
If you have **Arduino OS** installed in your
board you can use **Arduino Package Manager Application**.
Go to  *Menu -> Arduino -> Arduino Package Manger*
and then search `ciao-connector-phant`, select it an press *Install*

## Manually
Download the zip file of the latest [release](https://github.com/arduino-org/ciao-connector-phant/releases),
unzip and move it via `scp` inside you board in the desired location.
**Be sure to move `phant.ciao.conf.json` file into the ciao directory**, eg:
```
$ scp ~/Downloads/ciao-connector-smtp/phant.ciao.conf.json root@arduino.local:/usr/lib/python2.7/ciao/conf/
$ scp -r ~/Downloads/ciao-connector-phant/phant root@arduino.local:/root/.ciao/
```

## Configuration

### Ciao Core Configuration
Before start using the connector, set to `true` the `enabled` key in the `phant.ciao.json.file` file.
Change the `commands/start` values only if you installed the connector manually.

```json
{
	"name" : "phant",
	"enabled": false,
	"type" : "managed",
	"core" : ">=0.1.0",
	"commands": {
		"start": ["/root/.ciao/phant/phant.py"],
		"stop": ["/usr/bin/killall","-s", "HUP","phant.py"]
	},
	"implements" : {
		"write" : { "direction": "out", "has_params": true }
	}
}
```

### Connector Configuration/Parameters
To customize the connector to use your [phant server](https://github.com/sparkfun/phant),
please insert the correct vaules in params section of the configuration
file `phant/phant.json.conf`:

```json
...
	"params" : {
		"host" : "YOUR_PHANT_IP_OR_HOSTNAME",
		"port" : 8080,
		"base_uri" : "YOUR_BASE_URI_WITH_TRAILING_SLASH"
	}
...
```

Else use the configuration settings for data.sparkfun.com service as follow:
```
...
"params" : {
	"host" : "http://data.sparkfun.com",
	"port" : 80,
	"base_uri" : "input/"
}
...
```
## How To Use
Open [Arduino IDE](http://www.arduino.org/software), import
Arduino Ciao Library in your sketch and take a look at the
[example](https://github.com/arduino-org/ciao-connector-phant/examples)

## See Also
[Arduino Ciao](http://labs.arduino.org/Ciao)
