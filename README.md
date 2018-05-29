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
$ git clone https://github.com/mgeitz/npstat.git $HOME/.npstat
```

#### Run NPStat

NPStat must be run as `root`
```sh
$ sudo python npstat.py  -i [input_pin] -b [brightness 1-255] -l [led_count]
```

All arguments are optional, defaults are sourced from config.yml

#### Examples

```sh
$ sudo python npstat.py -i 18 -b 200 -l 12
```
```sh
$ sudo python npstat.py
```
```sh
$ sudo python npstat.py --help
```


### Arguments

| Argument	| Description	|
|---------------|---------------|
| -i _or_ --input| Neopixel input pin|
| -b _or_ --brightness| Starting brightness|
| -l _or_ --leds| Neopixel LED count|
| -h _or_ --help| Display usage|


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
