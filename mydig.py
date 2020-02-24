# Justin Santer (111501672)
# SBU Email: justin.santer@stonybrook.edu
# CSE 310 ~ Programming Assignment 1
# Professor Aruna Balasubramanian
# February 24, 2020

import dns.query
import dns.message
import dns.name
import dns.exception
import sys
import time
import datetime

global_cname = []  # Keeps track of CNAMEs


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
    domain_name = domain_name + "."

    # Calls mydig function starting with chosen root server
    start = time.perf_counter()
    answer = mydig("198.41.0.4", domain_name, len(domain_list)-1)
    end = time.perf_counter()
    if answer is None:
        return

    query_time = end - start
    query_time = int(query_time * 1000)

    # Prints result
    print("QUESTION SECTION:")
    print(domain_name + " IN A")
    print("ANSWER SECTION:")
    for i in global_cname:
        print(i)
    print(answer)
    print()
    print("Query time: " + str(query_time) + " msec")
    print("WHEN: " + str(datetime.datetime.now()))

    return


def mydig(ip_address: str, domain_name: str, domain_index: int):
    """Recursive DNS resolver function"""
    # Make a Message object
    message = dns.message.make_query(domain_name, "A")

    # Send the Message as a query and save the response
    try:
        response = dns.query.udp(message, ip_address, timeout=10)
    except dns.exception.Timeout:
        print("Error: query timed out")
        return None

    # First check if Answer RRset has answer A
    answer = response.get_rrset(dns.message.ANSWER, dns.name.from_text(domain_name), dns.rdataclass.IN, dns.rdatatype.A)
    if answer is not None:
        return answer

    # BONUS: check if Answer RRset has answer CNAME and resolve it
    cname = response.get_rrset(dns.message.ANSWER, dns.name.from_text(domain_name),
                               dns.rdataclass.IN, dns.rdatatype.CNAME)
    if cname is not None:
        global_cname.append(cname)
        cname_list = cname[0].to_text().split(".")
        cname_list = cname_list[:-1]
        return mydig("198.41.0.4", cname[0].to_text(), len(cname_list)-1)

    # Find the Authority RRset
    authority = response.get_rrset(dns.message.AUTHORITY, dns.name.from_text(parse_domain(domain_name, domain_index)),
                                   dns.rdataclass.IN, dns.rdatatype.NS)
    if authority is None:
        print("Error: no AUTHORITY section found")
        return None

    # Find the Additional RRset
    additional = response.get_rrset(dns.message.ADDITIONAL, dns.name.from_text(authority[0].to_text()),
                                    dns.rdataclass.IN, dns.rdatatype.A)
    if additional is None:
        print("Error: no ADDITONAL section found")
        return None

    # Recursive call with new IP
    return mydig(additional[0].to_text(), domain_name, domain_index-1)


def parse_domain(domain_name: str, index: int) -> str:
    """Parses together specified pieces of the split domain name"""
    domain_list = domain_name.split(".")
    domain_list = domain_list[:-1]
    domain_list = [x + "." for x in domain_list]
    if index == len(domain_list)-1:
        return domain_list[len(domain_list)-1]

    parsed = ""
    while index < len(domain_list):
        parsed = parsed + domain_list[index]
        index += 1

    return parsed


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)




