import subprocess
from typing import Optional


class Addr2Line:
    # All methods and variables within the class must be indented.
    def __init__(self, vmlinux_path: str):
        self.vmlinux_path = vmlinux_path

    # This method also needs to be indented.
    def symbolicate(self, addr: str) -> Optional[str]:
        try:
            # The code block within the 'try' statement must be indented.
            out = subprocess.run(["addr2line", "-e", self.vmlinux_path, "-f", "-C", addr], capture_output=True, text=True, timeout=6)

            if out.returncode != 0:
                # The code block within the 'if' statement must be indented.
                return None

            parts = out.stdout.strip().splitlines()

            if len(parts) >= 2:
                # The code block within the 'if' statement must be indented.
                return f"{parts[0].strip()} at {parts[1].strip()}"
            
            if parts:
                # The code block within the 'if' statement must be indented.
                return parts[0].strip()

            return None
        except Exception:
            # The code block within the 'except' statement must be indented.
            return None