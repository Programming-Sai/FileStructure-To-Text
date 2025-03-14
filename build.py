import os
import shutil
import sys
import subprocess
import sys

if sys.platform.startswith("win"):
    import winreg
else:
    winreg = None  # Or handle it differently


# Determine OS-specific installation path
if sys.platform.startswith("win"):
    install_dir = os.path.join(os.environ["LOCALAPPDATA"], "Programs", "FTT")
    exe_name = "ftt.exe"
    path_var = "Path"
else:
    install_dir = "/usr/local/bin"
    exe_name = "ftt"

# Ensure the installation directory exists
os.makedirs(install_dir, exist_ok=True)

# Build the standalone executable
print("🔧 Building FTT...")
os.system(f'pyinstaller --onefile --name {exe_name} main.py')

# Define paths
src_path = os.path.join("dist", exe_name)
dest_path = os.path.join(install_dir, exe_name)

# Move the executable to the global installation path
if os.path.exists(dest_path):
    print("♻️ Updating existing installation...")
    os.remove(dest_path)

shutil.copy(src_path, dest_path)

# Make it executable (Linux/macOS)
if not sys.platform.startswith("win"):
    os.chmod(dest_path, 0o755)

# Add to system PATH dynamically

def add_to_path_windows():
    command = f'[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";{install_dir}", "User")'

    subprocess.run(["powershell", "-Command", command], shell=True)

    print("✅ FTT added to PATH. Restart your terminal for changes to take effect.")


def add_to_path_linux():
    bashrc_path = os.path.expanduser("~/.bashrc")
    profile_path = os.path.expanduser("~/.profile")
    export_cmd = f'\nexport PATH="{install_dir}:$PATH"\n'

    if install_dir not in os.environ["PATH"]:
        print("🔧 Adding FTT to system PATH...")
        try:
            with open(bashrc_path, "a") as f:
                f.write(export_cmd)
            with open(profile_path, "a") as f:
                f.write(export_cmd)
            print("✅ FTT added to PATH. Restart your terminal or run `source ~/.bashrc`.")
        except Exception as e:
            print(f"⚠️ Failed to add FTT to PATH automatically: {e}")
            print(f"➡️ Please add `{install_dir}` to your system PATH manually.")

# Apply changes based on OS
if sys.platform.startswith("win"):
    add_to_path_windows()
else:
    add_to_path_linux()

print(f"✅ FTT installed globally! Run it using: `{exe_name}`")

