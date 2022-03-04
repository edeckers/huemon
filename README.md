# Huemon

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Build](https://github.com/edeckers/huemon/actions/workflows/test.yml/badge.svg)](https://github.com/edeckers/huemon/actions/workflows/test.yml)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

Zabbix monitoring for Philips Hue networks.

## Requirements

- Zabbix server 5.0+
- Zabbix agent 5.0+
- Python 3.0+ on Zabbix agent machine

## Running

### Shell

```bash
docker run -v /path/to/huemon/config:/etc/huemon huemon:0.0.3 discover lights
```

### Docker

```bash
HUEMON_CONFIG_PATH=/usr/bin/python3 -m huemon discover lights
```

## Installation

### Dependencies and environment

```bash
make install
```

### Configuration

1. Copy `config.example.yml` from `src/huemon` to `/path/to/config.yml`
2. Make necessary changes
3. Provide the path through environment variable `HUEMON_CONFIG_PATH`

For example:

```bash
HUEMON_CONFIG_PATH=/path/to/config.yml python3 -m huemon discover lights
```

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

UserParameter=hue.discovery[*],HUEMON_CONFIG_PATH=/usr/bin/python3 -m huemon discover $1
UserParameter=hue.value[*],HUEMON_CONFIG_PATH=/usr/bin/python3 -m huemon $1 $2 $3
```

## License

MPL-2.0
