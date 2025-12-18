"""
Utility helper functions for loading test fixtures.

This module provides functions to load and retrieve test data fixtures used in the CV creator agent tests.
It includes functions to load a master CV from a JSON fixture file and to load a dummy job description from a text fixture file.
"""
import json


def get_master_cv(): 
    with open("tests/fixtures/public_cv.json", encoding="utf-8") as f:
        return json.load(f)

def get_dummy_jd():
    with open("tests/fixtures/dummy_jd") as f:
        return f.read()