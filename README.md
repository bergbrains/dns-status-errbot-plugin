# DNS Status Errbot Plugin

An Errbot plugin for performing DNS lookups, checking DNS server status, and monitoring DNS propagation.

## Features

- DNS lookups for various record types
- Reverse DNS lookups
- DNS server status checking
- DNS propagation monitoring across multiple public DNS servers
- DNS resolver cache flushing

## Installation

### From pip

```bash
pip install dns-status-errbot-plugin
```

### From source

```bash
git clone https://github.com/yourusername/dns-status-errbot-plugin.git
cd dns-status-errbot-plugin
pip install -e .
```

### Errbot plugin installation

Once installed, activate the plugin in your Errbot instance:

```
!plugin install dns-status-errbot-plugin
```

## Usage

### DNS Lookup

Perform a DNS lookup for a domain:

```
!dns lookup example.com [record_type]
```

If no record type is specified, it defaults to A records.

### Reverse DNS Lookup

Perform a reverse DNS lookup for an IP address:

```
!dns reverse 8.8.8.8
```

### DNS Server Check

Check if specified DNS servers are responding:

```
!dns check 8.8.8.8 8.8.4.4
```

If no servers are specified, it defaults to checking Google DNS servers (8.8.8.8 and 8.8.4.4).

### DNS Propagation Check

Check DNS propagation across multiple public DNS servers:

```
!dns propagation example.com [record_type]
```

This checks the domain against the following public DNS servers:

- Google DNS (8.8.8.8)
- Cloudflare (1.1.1.1)
- Quad9 (9.9.9.9)
- OpenDNS (208.67.222.222)
- AdGuard DNS (94.140.14.14)

### DNS Cache Flush

Flush the DNS resolver cache:

```
!dns flush
```

## Requirements

- Python 3.6+
- Errbot 6.0+
- dnspython
- ipaddress

## Development

1. Clone the repository
2. Set up a virtual environment:
   ```bash
   pipenv install --dev
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT License
