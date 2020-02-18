# Justin Santer (111501672)
# SBU Email: justin.santer@stonybrook.edu
# CSE 310 ~ Programming Assignment 1
# Professor Aruna Balasubramanian
# February 24, 2020

import dns.query
import dns.message
import sys


def main(argc, argv):

    # Checks to see if the arguments are in a valid form
    if argc == 1:
        print("No argument given")
        return
    elif argc > 2:
        print("Invalid number of arguments given")
        return

    # Set the domain to be resolved
    domain_name = argv[1]

    # Calls mydig function starting with root server
    mydig(domain_name, "198.41.0.4")

    return


def mydig(domain_name, ip_address):
    """Recursive DNS resolver function"""

    message = dns.message.make_query(domain_name, "A")
    response = dns.query.udp(message, ip_address, timeout=15)
    print(response.to_text())

    return


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)




