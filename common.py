# -*- coding: utf-8 -*-
"""Shared helpers for the AutomatiK conky config generators."""

import os


def detect_language():
    """Return the user's language based on the system locale."""
    installed = os.popen("locale | grep LANG").read()
    if "fr" in installed:
        return "French"
    if "de" in installed:
        return "German"
    if "pt" in installed:
        return "Portuguese"
    if "it" in installed:
        return "Italian"
    return "English"


def read_header():
    """Read the shared conky header snippet."""
    with open("header.py", "r", encoding="utf-8") as f:
        return f.read()


def write_file(name, content):
    """Write a generated conky config file atomically if changed."""
    try:
        with open(name, "r", encoding="utf-8") as f:
            if f.read() == content:
                return
    except OSError:
        pass
    tmp_name = f".{name}.tmp.{os.getpid()}"
    with open(tmp_name, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp_name, name)
