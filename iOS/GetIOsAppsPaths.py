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
        print(f"Found {len(apps)} installed apps:\n")

        for i, app in enumerate(apps, 1):
            bundle_id = app.get("CFBundleIdentifier", "Unknown")
            display_name = app.get("CFBundleDisplayName", "Unknown")
            app_version = app.get("CFBundleShortVersionString", "Unknown")
            app_path = app.get("Path", "Unknown")
            container_path = app.get("Container", "Unknown")

            print(f"[{i}] {display_name}")
            print(f"    Bundle ID:      {bundle_id}")
            print(f"    Version:        {app_version}")
            print(f"    App Path:       {app_path}")
            print(f"    Container Path: {container_path}")
            print()

