import os, sys

__all__ = [
    "SHIM_ROOT",
    "REINVENT_ROOT",
    "PKG_ROOT"
]

SHIM_ROOT = os.path.dirname(__file__)
REINVENT_ROOT = os.path.join(SHIM_ROOT, 'Reinvent')
PKG_ROOT = os.path.join(SHIM_ROOT, 'pkgs')
for root in [SHIM_ROOT, PKG_ROOT, REINVENT_ROOT]:
    if root not in sys.path: sys.path.insert(0, root)