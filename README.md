# TP-Link Tapo Klipper

This is a Klipper module for controlling the TP-Link Tapo P100 Plugs.

### Configuration

```
# printer.cfg

[smartplug my_name]
ip: 10.0.0.18
user: ...
password: ...
```

```
# moonraker.cfg

[update_manager tplink_tapo]
type: git_repo
path: ~/tplink_tapo
origin: https://github.com/Zergie/tplink_tapo.git
primary_branch:main
managed_services: klipper
env: ~/mobileraker-env/bin/python
requirements: requirements.txt
install_script: install.sh
```

### Usage

```
QUERY_PLUG PLUG=<name>
TURN_ON_PLUG PLUG=<name> [DELAY=<milliseconds>]
TURN_OFF_PLUG PLUG=<name> [DELAY=<milliseconds>]
```
