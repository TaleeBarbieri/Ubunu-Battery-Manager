import os
import time
import psutil
import subprocess

def battery_info():
    battery = psutil.sensors_battery()

    print("\n--- BATTERY INFORMATION ---\n")

    if battery is not None:
        percent = int(battery.percent)
        is_plugged = battery.power_plugged
        time_left = battery.secsleft

        print(f"Battery Percentage: {percent}%")
        print(f"Charging: {'Yes' if is_plugged else 'No'}")

        if percent == 100:
            print("Battery fully charged.")
        else:
            print("Battery not fully charged")

        if time_left == psutil.POWER_TIME_UNKNOWN:
            print("Power time unknown.")

        elif time_left < 0:
            print("Time left: Charging, time estimation not available.")

        else:
            hours, minutes = divmod(time_left // 60, 60)
            print(f"Time left: {hours} hours and {minutes} minutes")
    else:
        print("Battery information is not available.")

def change_power_mode():
    battery = psutil.sensors_battery()

    if battery is None:
        print("No battery detected.")
        return

    if battery.power_plugged:
        print("Laptop is plugged in. Switching to PERFORMANCE mode.")
        subprocess.run(['powerprofilesctl', 'set', 'performance'], check=True)
    else:
        print("Laptop is running on battery. Switching to POWER-SAVER mode.")
        subprocess.run(['powerprofilesctl', 'set', 'power-saver'], check=True)

def monitor_power_status():
    previous_status = None

    while True:
        battery_info()  # Display battery info
        battery = psutil.sensors_battery()

        if battery is None:
            print("No battery detected. Exiting.")
            break

        current_status = battery.power_plugged

        if current_status != previous_status:
            change_power_mode()
            previous_status = current_status

        # Sleep for 30 seconds before checking again
        time.sleep(10)

if __name__ == "__main__":
    # Start monitoring the power status in the background
    print(f"Starting background process with PID: {os.getpid()}")
    monitor_power_status()
