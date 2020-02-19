# Justin Santer (111501672)
# SBU Email: justin.santer@stonybrook.edu
# CSE 310 ~ Programming Assignment 1
# Professor Aruna Balasubramanian
# February 24, 2020

import dns.query
import dns.message
import dns.name
import sys


def main(argc: int, argv: list):

    # Sets the domain name accordingly
    if argc == 1:
        domain_name = input("Enter a domain: ")
    elif argc > 2:
        print("Invalid number of arguments given")
        domain_name = input("Enter a domain: ")
    else:
        domain_name = argv[1]

    domain_list = domain_name.split(".")
    domain_list = [x + "." for x in domain_list]

    # Calls mydig function starting with root server
    response = mydig("198.41.0.4", domain_list, len(domain_list), domain_name)

    return


def mydig(ip_address: str, domain_list: list, domain_size: int, domain_name: str):
    """Recursive DNS resolver function"""

    # Make a Message object
    message = dns.message.make_query(domain_name, "A")

    # Send the Message as a query and save the response
    response = dns.query.udp(message, ip_address, timeout=10)
    print(response.to_text())

    # Find the RRset
    rrset = response.get_rrset(dns.message.AUTHORITY, dns.name.from_text(domain_list[domain_size-1]),
                               dns.rdataclass.IN, dns.rdatatype.NS)
    if rrset is None:
        print("Error: query failed")
        return None

    print()
    print(rrset.to_text())
    print()
    print(rrset[0])

    return response


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)




