import os
from dreampylib import DreampyLib

password = os.environ.get("DREAMHOST_APIKEY") or raw_input("API key: ")
ZONE_OUTPUT_TEMPLATE = "{record:<30} IN {type:<6} {value:<30} ; {comment}"

if __name__ == '__main__':
    import pprint

    # Set this to true to enable debugging
    DEBUG = False

    # Specify the default returntype.
    # Can be either 'dict' or 'list'
    defaultReturnType = 'dict'

    # Initialize the library and open a connection
    connection = DreampyLib(password)

    # If the connection is up, do some tests.
    if not connection.IsConnected():
        print "Error connecting!"
        print connection.Status()

        import sys
        sys.exit(1)

    response = connection.dns.list_records()
    if DEBUG:
        pprint.pprint(response)
    dns_data = {}
    for d in response:
        account_entries = dns_data.setdefault(d["account_id"], {})
        zone_entries = account_entries.setdefault(d["zone"], [])
        zone_entries.append(d)
    if DEBUG:
        pprint.pprint(dns_data)

    for a in dns_data:
        print "# ", "-" * 50, "Account: %s" % a, "-" * 50
        zones = dns_data[a]
        for z in zones:
            print "# ", "." * 50, "Zone: %s" % z, "." * 50
            zone = zones[z]
            print "$ORIGIN %s" % z
            print "$TTL 600s"
            for e in zone:
                e["record"] += "."
                print ZONE_OUTPUT_TEMPLATE.format(**e)
