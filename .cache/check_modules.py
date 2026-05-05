import importlib
import sys

modules = ["json", "urllib.request", "random", "tkinter", "time"]
missing = []

for module_name in modules:
    try:
        importlib.import_module(module_name)
    except Exception as e:
        missing.append(module_name + ": " + str(e))

if missing:
    print("MISSING_MODULES")
    for item in missing:
        print(item)
    sys.exit(1)

print("ALL_MODULES_OK")
sys.exit(0)
