from argparse import ArgumentParser
from util import Vendom

parser = ArgumentParser(prog="Vendom", usage="%(prog)s [options]", description="OUI to vendor name and address")
parser.add_argument("oui", action="store", nargs="+")
parser.add_argument("-f", "--file", help="Data file", default="data.json")

args = parser.parse_args()

ouis = args.oui
file = args.file

if ouis:
    vendom = Vendom(file=file)
    for o in ouis:
        o = str(o).lower()

        data = vendom.get(o)

        if data.get(o):
            org = data[o]['org']
            address = data[o]['address']

            print("[+] " + str(o) + ":")
            print(f"\t   {org}")
            print(f"\t   {address}")
        else:
            o = o[:6]

            print("[-] " + str(o).rjust(6, ' ') + ": Not found")