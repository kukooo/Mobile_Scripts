#!/bin/python3

import plistlib
import subprocess


def get_installed_apps():
    try:
        # Fetch installed apps in XML format
        # Depending on the version the command changes
        result = subprocess.run(
            ["ideviceinstaller", "-l", "-o", "xml"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            result = subprocess.run(
                ["ideviceinstaller", "list", "--xml"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(f"Error: {result.stderr.strip()}")
                return None

        # Parse the output plist
        apps_plist = plistlib.loads(result.stdout.encode("utf-8"))
        return apps_plist

    except Exception as e:
        print(f"An error occurred while fetching apps: {e}")
        return None


if __name__ == "__main__":
    apps = get_installed_apps()
    if apps:
        # Find max lengths for dynamic formatting
        max_display_name_length = max(len(app.get("CFBundleDisplayName", "Unknown")) for app in apps)
        max_version_length = max(len(app.get("CFBundleShortVersionString", "Unknown")) for app in apps)
        max_bundle_id_length = max(len(app.get("CFBundleIdentifier", "Unknown")) for app in apps)
        max_app_path_length = max(len(app.get("Path", "Unknown")) for app in apps)
        max_container_path_length = max(len(app.get("Path", "Unknown")) for app in apps)

        print(f"{'Display Name':<{max_display_name_length}} {'Bundle ID':<{max_bundle_id_length}} {'Version':<{max_version_length}} {'App Path':<{max_app_path_length}} {'Container Path':<{max_container_path_length}}")
        print("=" * (max_display_name_length + max_version_length + max_bundle_id_length + max_app_path_length + max_container_path_length - 5))

        for app in apps:
            bundle_id = app.get("CFBundleIdentifier", "Unknown")
            display_name = app.get("CFBundleDisplayName", "Unknown")
            app_version = app.get("CFBundleShortVersionString", "Unknown")
            app_path = app.get("Path", "Unknown")
            container_path = app.get("Container", "Unknown")

            print(f"{display_name:<{max_display_name_length}} {bundle_id:<{max_bundle_id_length}} {app_version:<{max_version_length}} {app_path:<{max_app_path_length}} {container_path}")

