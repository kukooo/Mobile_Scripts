#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

if [ "$#" -eq 1 ]; then
    echo "Trying to dump: $1"
    application="$1"
else
    echo "[+] Retrieving packages..."

    packages=($(adb shell pm list packages | grep -vE "com.google|com.android|com.qualcomm|com.xiaomi|com.miui" | sed 's/package://g'))

    for package in "${!packages[@]}"; do
      echo "    $((package + 1)): ${packages[package]}"
    done

    # Ask the user to select a file
    read -e -p "[?] Enter a number to select the package: " choice

    # Check if the choice is valid
    if [[ "$choice" -ge 1 && "$choice" -le "${#packages[@]}" ]]; then
      # Display the selected file
      echo "[+] You selected: ${packages[$((choice - 1))]}"
      application=${packages[$((choice - 1))]}
    else
      echo "Invalid choice."
      exit 1
    fi
fi

adb shell pm path ${application} 1>/dev/null

if [ $? -eq 1 ]; then
    echo "Package ${application} not found"
    echo "Exiting..."
    exit 1
fi

mkdir ./${application}/
adb shell pm path ${application} | sed 's/package://g' | xargs -I {} adb pull {} ./${application}/
java -jar $SCRIPT_DIR/APKEditor.jar m -i ./${application} -o ${application}.apk
