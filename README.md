# Huemon

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Build](https://github.com/edeckers/huemon/actions/workflows/test.yml/badge.svg)](https://github.com/edeckers/huemon/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/huemon.svg?maxAge=3600)](https://pypi.org/project/huemon)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

Zabbix monitoring with low-level discovery for Philips Hue networks.

![Dashboard: sensors](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/dashboard-sensors.png?raw=true "Dashboard: sensors")

## Requirements

- Zabbix server 5.0+
- Zabbix agent 5.0+
- Python 3.7+ on Zabbix agent machine

## Installation

```bash
pip3 install huemon
```

## Configuration

1. Copy `config.example.yml` from `src/huemon` to `/path/to/config.yml`
2. Make necessary changes
3. Provide the path through environment variable `HUEMON_CONFIG_PATH`

### Enabling commands and discoveries

#### Automatically

```bash
HUEMON_CONFIG_PATH=/path/to/config.yml python3 -m huemon install_available commands
HUEMON_CONFIG_PATH=/path/to/config.yml python3 -m huemon install_available discoveries
```

#### Manually

```bash
ln -s /path/to/commands_available/command_name.py /path/to/commands_enabled/command_name.py
ln -s /path/to/discoveries_available/command_name.py /path/to/discoveries_enabled/command_name.py
```

### Zabbix agent configuration

```
# file:/path/to/zabbix/agent/conf.d/hue.conf

UserParameter=hue.discovery[*],HUEMON_CONFIG_PATH=/path/to/config.yml /usr/bin/python3 -m huemon discover $1
UserParameter=hue.value[*],HUEMON_CONFIG_PATH=/path/to/config.yml /usr/bin/python3 -m huemon $1 $2 $3
```

Or Docker

```
# file:/path/to/zabbix/agent/conf.d/hue.conf

UserParameter=hue.discovery[*],docker-compose run huemon discover $1
UserParameter=hue.value[*],docker-compose run huemon $1 $2 $3
```

Or _agent mode_

```
# file:/path/to/zabbix/agent/conf.d/hue.conf

UserParameter=hue.discovery[*],curl http://127.0.0.1:8000/discover?q=$1
UserParameter=hue.value[*],curl http://127.0.0.1:8000/$1?q=$2\&q=$3
```

## Usage

### Shell

```bash
HUEMON_CONFIG_PATH=/usr/bin/python3 -m huemon discover lights
```

Or _agent mode_

```bash
HUEMON_CONFIG_PATH=/usr/bin/python3 -m huemon agent start
```

### Docker

Provide a configuration path for the `huemon-config` volume in `docker-compose.yml` before running the commands below.

```bash
docker-compose run huemon discover lights
```

Or _agent mode_

```bash
docker-compose up -d
```

## Screenshots

### Dashboards
![Dashboard: sensors](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/dashboard-sensors.png?raw=true "Dashboard: sensors")

### Discoveries

![Discoveries: batteries](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/discoveries-batteries.png?raw=true "Discoveries: batteries")

![Discoveries: lights](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/discoveries-lights.png?raw=true "Discoveries: lights")

![Discoveries: sensors](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/discoveries-sensors.png?raw=true "Discoveries: sensors")

### Template

![Template](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/template-discoveries.png?raw=true "Template")


## License

MPL-2.0
