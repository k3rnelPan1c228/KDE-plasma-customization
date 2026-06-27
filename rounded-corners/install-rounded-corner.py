import os
import subprocess
import sys

# Define color codes for pretty terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def run_command(command, use_sudo=False):
    """Utility to run a system command and handle errors."""
    if use_sudo:
        command = f"sudo {command}"

    print(f"{YELLOW}Running:{RESET} {command}")
    process = subprocess.run(command, shell=True)

    if process.returncode != 0:
        print(f"{RED}Error executing last command. Exiting.{RESET}")
        sys.exit(1)


def main():
    print(f"{GREEN}=== Starting KDE Plasma 6 Rounded Corners Setup ==={RESET}")

    # 1. Install dependencies via Zypper
    print(f"\n{GREEN}[1/4] Installing development dependencies...{RESET}")
    dependencies = (
        "git cmake extra-cmake-modules kwin6-devel plasma6-dev "
        "qt6-base-devel qt6-declarative-devel qt6-quickcomponents-devel "
        "kf6-extra-cmake-modules kf6-kwindowsystem-devel kf6-kcoreaddons-devel kf6-kconfig-devel"
    )
    run_command(f"zypper in -y {dependencies}", use_sudo=True)

    # 2. Clone repository
    print(f"\n{GREEN}[2/4] Cloning the KDE-Rounded-Corners repository...{RESET}")
    repo_url = "https://github.com/matinlotfali/KDE-Rounded-Corners.git"
    repo_dir = "KDE-Rounded-Corners"

    if os.path.exists(repo_dir):
        print(f"{YELLOW}Directory already exists. Wiping to start fresh...{RESET}")
        run_command(f"rm -rf {repo_dir}")

    run_command(f"git clone {repo_url}")

    # 3. Build and Install
    print(f"\n{GREEN}[3/4] Compiling and installing the plugin...{RESET}")
    os.chdir(repo_dir)
    os.makedirs("build", exist_ok=True)
    os.chdir("build")

    run_command("cmake ..")
    run_command("make")
    run_command("make install", use_sudo=True)

    # 4. Reload KWin
    print(f"\n{GREEN}[4/4] Reloading KWin configuration...{RESET}")
    # Try the openSUSE specific path first, fallback to standard qdbus
    qdbus_path = (
        "/usr/lib64/qt6/bin/qdbus"
        if os.path.exists("/usr/lib64/qt6/bin/qdbus")
        else "qdbus"
    )
    run_command(f"{qdbus_path} org.kde.KWin /KWin reconfigure")

    print(f"\n{GREEN}=== Success! ==={RESET}")
    print("The effect has been installed.")
    print("Now open 'System Settings' -> 'Desktop Effects' to enable it manually.")


if __name__ == "__main__":
    main()
