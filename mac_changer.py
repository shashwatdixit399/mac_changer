#!/usr/bin/env python3

import subprocess
import argparse
import re

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", "-i", dest="interface", help="the interface for which the mac is to be changed")
    parser.add_argument("--mac", "-m", dest="new_mac", help="the new mac address")
    arg= parser.parse_args()
    if not arg.interface:
        parser.error("[-]Please enter the interface to be modified.")
    if not arg.new_mac:
        parser.error("[-]Please enter the new MAC address.")
    return arg

def change_mac(iface,new_mac):
    print("[+]Changing mac of " + iface + " to " + new_mac)
    subprocess.call(["ifconfig", iface, "down"])
    subprocess.call(["ifconfig", iface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", iface, "up"])

def get_cur_mac(interface):
    ifconf_result = subprocess.check_output(["ifconfig", interface])
    # print(ifconf)
    ifconfig_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconf_result)
    # print(ifconfig_search_output.group(0))
    if ifconfig_mac:
        return ifconfig_mac.group(0)
    else:
        print("[-]The inteface " + arg.interface + " does not have a MAC")
        exit()

def check_interface_exists(interface):
    ifconfig_result=subprocess.check_output(["ifconfig"])
    print(ifconfig_result)
    get_ifaces_name=re.search(r"\w*:",ifconfig_result)
    print(get_ifaces_name.group(1))
    #check if interface exists in get_ifaces_name and print message


arg=get_arguments()
check_interface_exists(arg.interface)
cur_mac=get_cur_mac(arg.interface)
print("[+]The Current MAC Address is "+cur_mac)
change_mac(arg.interface,arg.new_mac)
cur_mac=get_cur_mac(arg.interface)
if cur_mac==arg.new_mac:
    print("[+]The MAC address was successfully changed")
else:
    print("[-]The MAC address could not be changed")


