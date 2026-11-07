# -*- encoding: utf-8 -*-
import os
from common import detect_language, read_header
from translations import *

Language = detect_language()
header = read_header()

CardVendor = os.popen(
    "clinfo 2>/dev/null | grep -i 'Platform Vendor:'").read().rstrip().lower().split("\n")
if not any(CardVendor):
    CardVendor = os.popen(
        "lspci | grep -i ' vga '").read().rstrip().lower().split("\n")

if len(CardVendor) > 1:
    for i in range(len(CardVendor)):
        if CardVendor[i].find('intel') != -1:
            CardVendor[i] = ""

if CardVendor and CardVendor[0].find('amd') != -1:
    import amd
elif CardVendor and CardVendor[0].find('nvidia') != -1:
    import nvidia
