#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import plistlib
import sys
from collections import OrderedDict
from pathlib import Path
from urllib.parse import unquote

def convert_map(elem):
    """
    Convert <map>…</map> into an OrderedDict.
    """
    d = OrderedDict()
    for child in elem:
        # decode percent‑escapes in the key name
        key = unquote(child.get("name"))
        d[key] = convert_element(child)
    return d

def convert_element(elem):
    """
    Recursively convert an Android XML Element into a Python object plistlib understands.
    """
    tag = elem.tag.lower()
    if tag == "map":
        return convert_map(elem)
    if tag == "list":
        return [convert_element(c) for c in elem]
    text = elem.text or ""
    # numeric / bool types come in attributes, too
    if tag in ("int", "integer"):
        return int(elem.get("value", text))
    if tag in ("float", "double"):
        return float(elem.get("value", text))
    if tag in ("bool", "boolean"):
        v = elem.get("value", text).lower()
        return v in ("true", "1", "yes")
    # fallback to string
    return text

def android_xml_to_plist(android_xml_path, plist_out_path):
    # 1. Parse Android XML
    tree = ET.parse(android_xml_path)
    root = tree.getroot()
    if root.tag.lower() != "map":
        raise ValueError("Expected top‑level <map> element")

    # 2. Convert to Python OrderedDict
    data = convert_map(root)

    # 3. Dump to XML plist, preserving key order
    with open(plist_out_path, "wb") as f:
        plistlib.dump(data, f,
            fmt=plistlib.FMT_XML,
            sort_keys=False
        )

    print(f"Wrote iOS plist: {plist_out_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: android_to_ios_plist.py input_android.xml output_ios.plist")
    android_xml_to_plist(Path(sys.argv[1]), Path(sys.argv[2]))
