# NPStat

## NCurses Neopixel Status Indicator

![NPStat][NPStat1]
![NPStat][NPStat2]

[NPStat1]: https://i.imgur.com/NKSv8hO.png
[NPStat2]: https://i.imgur.com/5JdSpmi.png

### Dependencies

#### Debian

Install dependencies
```sh
$ apt-get install build-essential python-dev git scons swig python-yaml
```

Install [rpi_ws281x](https://learn.adafruit.com/neopixels-on-raspberry-pi/software)
```sh
$ git clone https://github.com/jgarff/rpi_ws281x.git
$ cd rpi_ws281x
$ scons
$ cd python
$ sudo python setup.py install
```


### Getting Started

#### Clone NPStat

```sh
$ git clone https://github.com/mgeitz/npstat.git
```

#### Run NPStat

NPStat must be run as `root`
```sh
$ sudo python npstat  -i [input_pin] -b [brightness 1-255] -l [led_count]
```

All arguements are optional, defaults are sourced from config.yml

#### Examples

```sh
$ sudo python npstat -i 18 -b 200 -l 12
```


### Arguements

| Argument	| Description	|
|---------------|---------------|
| -i		| Neopixel input pin|
| -b		| Starting brightness|
| -l		| Neopixel LED count|


### Commands

| Command	| Description	|
|---------------|---------------|
| F2		| Set light profile to `Status Indicator - wipe`|
| F3		| Toggle breath|
| PgUp		| Increase brightness|
| PgDn		| Decrease brightness|
| F11		| Refresh screen|
| F12		| Toggle help display|


### Contributing
View the section on [how to contribute](./CONTRIBUTING.md)
