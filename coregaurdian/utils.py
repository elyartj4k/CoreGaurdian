# small utilities used by multiple modules
import re

def safe_strip(s: str) -> str:
    return s.strip() if s else ''