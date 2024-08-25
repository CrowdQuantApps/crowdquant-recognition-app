import subprocess
import sys
import time

required_libraries = [
    "pywebview", "flask", "flask-cors", "pywebsockets"
    "opencv-python", "numpy", "pandas", "ultralytics"
]

print("---------------------------------------")
print("[>>] Package Autoinstaller")
print("[>>] Version: v1.0")
print("[>>] Author: DevDJ")
print("---------------------------------------")


def check_installed(package_name):
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", package_name])
        return True
    except subprocess.CalledProcessError:
        return False


time.sleep(1)
print("[>>] Scanning available libraries...")
missing_libraries = [lib for lib in required_libraries if not check_installed(lib)]

if missing_libraries:
    print("[>>] WARNING! Missing libraries detected.")
    print(f"[>>] Missing libraries: {', '.join(missing_libraries)}")
    print("[>>] Installing missing libraries...")
    for library in missing_libraries:
        subprocess.call([sys.executable, "-m", "pip", "install", library])

    print("[>>] Installing completed...")
else:
    print("[>>] All required libraries are already installed.")

time.sleep(1)
print("[>>] Launching the application...")
print('[>>] Next time, run the program "main.py".')
process = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

if process.returncode == 0:
    print("[>>] App successfully started.")
    print(output.decode())
else:
    print("[>>] An error occurred while launching the application.")
    print("[>>] Error:", error.decode())
