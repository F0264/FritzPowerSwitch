# FritzPowerSwitch
A small script to switch the power outlet on a Fritz!Powerline 546 via http request. It was developed with homeassistant and pyscipt in mind.

## Configuration

You need to enter some details in the [powerline_async.py](./powerline_async.py) file:

- USERNAME: The username for the user interface of the Powerline adapter. By default this is empty.
- PASSWORD: The password you use to log in the user interface.
- IP_ADDRESS: The IP-Address of the Powerline Adapter.

## Usage

This is an example, of how you can call the script in a homeassistant script

Turning the outlet on:
```Yaml
action: pyscript.async_switch_powerline
data:
  switchaction: "on"
```

Turning the outlet off:
```Yaml
action: pyscript.async_switch_powerline
data:
  switchaction: "off"
```
