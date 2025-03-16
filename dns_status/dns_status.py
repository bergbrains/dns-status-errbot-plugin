from errbot import BotPlugin, botcmd
import dns.resolver
import dns.exception
import ipaddress
import socket
import time
import concurrent.futures


class DnsStatus(BotPlugin):
    """
    A plugin to perform DNS lookups and check DNS server status
    """

    def activate(self):
        """
        Activate the plugin
        """
        super().activate()
        self.log.info("DNS Status plugin activated")

    @botcmd(split_args_with=None)
    def dns_lookup(self, msg, args):
        """
        Perform a DNS lookup for a domain
        Usage: !dns lookup example.com [record_type]
        """
        if not args:
            return "Please provide a domain name to lookup"

        domain = args[0]
        record_type = "A"

        if len(args) > 1:
            record_type = args[1].upper()

        try:
            answers = dns.resolver.resolve(domain, record_type)
            result = f"DNS lookup for {domain} ({record_type} records):\n"

            for rdata in answers:
                result += f"- {rdata}\n"

            return result

        except dns.resolver.NoAnswer:
            return f"No {record_type} records found for {domain}"
        except dns.resolver.NXDOMAIN:
            return f"Domain {domain} does not exist"
        except dns.exception.DNSException as e:
            return f"DNS lookup error: {str(e)}"

    @botcmd(split_args_with=None)
    def dns_reverse(self, msg, args):
        """
        Perform a reverse DNS lookup for an IP address
        Usage: !dns reverse 8.8.8.8
        """
        if not args:
            return "Please provide an IP address for reverse lookup"

        ip = args[0]

        try:
            # Validate IP address
            ipaddress.ip_address(ip)

            result = socket.gethostbyaddr(ip)
            return f"Reverse DNS for {ip}: {result[0]}"
        except socket.herror:
            return f"No reverse DNS record found for {ip}"
        except ValueError:
            return f"Invalid IP address: {ip}"
        except Exception as e:
            return f"Error performing reverse lookup: {str(e)}"

    @botcmd(split_args_with=None)
    def dns_check(self, msg, args):
        """
        Check if specified DNS servers are responding
        Usage: !dns check 8.8.8.8 8.8.4.4
        """
        if not args:
            # Default to checking Google DNS if no servers specified
            servers = ["8.8.8.8", "8.8.4.4"]
        else:
            servers = args

        results = []

        for server in servers:
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [server]
                resolver.timeout = 2
                resolver.lifetime = 2

                start_time = time.time()
                resolver.resolve("google.com", "A")
                response_time = (time.time() - start_time) * 1000

                results.append(f"✅ DNS server {server} is responding (response time: {response_time:.2f}ms)")
            except Exception as e:
                results.append(f"❌ DNS server {server} failed: {str(e)}")

        return "\n".join(results)

    @botcmd(split_args_with=None)
    def dns_propagation(self, msg, args):
        """
        Check DNS propagation across multiple public DNS servers
        Usage: !dns propagation example.com [record_type]
        """
        if not args:
            return "Please provide a domain name to check"

        domain = args[0]
        record_type = "A"

        if len(args) > 1:
            record_type = args[1].upper()

        # List of public DNS servers to check
        public_dns = {
            "Google DNS": "8.8.8.8",
            "Cloudflare": "1.1.1.1",
            "Quad9": "9.9.9.9",
            "OpenDNS": "208.67.222.222",
            "AdGuard DNS": "94.140.14.14"
        }

        results = []
        results.append(f"DNS propagation check for {domain} ({record_type} records):")

        def check_dns(name, server):
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [server]
                resolver.timeout = 3
                resolver.lifetime = 3

                answers = resolver.resolve(domain, record_type)
                records = [str(rdata) for rdata in answers]
                return name, True, records
            except Exception as e:
                return name, False, str(e)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(public_dns)) as executor:
            future_to_dns = {
                executor.submit(check_dns, name, server): name
                for name, server in public_dns.items()
            }

            for future in concurrent.futures.as_completed(future_to_dns):
                name, success, data = future.result()
                if success:
                    results.append(f"✅ {name}: {', '.join(data)}")
                else:
                    results.append(f"❌ {name}: Error - {data}")

        return "\n".join(results)

    @botcmd
    def dns_flush(self, msg, args):
        """
        Flush the DNS resolver cache
        Usage: !dns flush
        """
        try:
            dns.resolver.reset_default_resolver()
            return "DNS resolver cache has been flushed."
        except Exception as e:
            return f"Error flushing DNS cache: {str(e)}"