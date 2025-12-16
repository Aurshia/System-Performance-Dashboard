import psutil
import os
import time

def bytes_to_readable(num):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024

def Get_CPU_INFO():
    freq = psutil.cpu_freq()
    return {
        "CPU Usage (%)": psutil.cpu_percent(interval=0.5),
        "CPU Cores": psutil.cpu_count(logical=True),
        "CPU Frequency": f"{freq.current:.2f} MHz"
    }

def Get_MEMORY_INFO():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "Total Memory": bytes_to_readable(mem.total),
        "Used Memory": bytes_to_readable(mem.used),
        "Free Memory": bytes_to_readable(mem.available),
        "Swap Total": bytes_to_readable(swap.total),
        "Swap Used": bytes_to_readable(swap.used),
    }

def Get_DISK_INFO():
    usage = psutil.disk_usage("C:\\")
    return {
        "Total Disk": bytes_to_readable(usage.total),
        "Used Disk": bytes_to_readable(usage.used),
        "Free Disk": bytes_to_readable(usage.free),
    }

def Get_NETWORK_INFO():
    net = psutil.net_io_counters()
    return {
        "Bytes Sent": bytes_to_readable(net.bytes_sent),
        "Bytes Received": bytes_to_readable(net.bytes_recv),
    }

def Get_BATTERY_INFO():
    battery = psutil.sensors_battery()
    if battery is None:
        return {"Battery": "No battery detected"}

    return {
        "Battery Percentage": f"{battery.percent}%",
        "Plugged In": "Yes" if battery.power_plugged else "No",
    }

def print_dash(title, info):
    print(f"\n===== {title} =====")
    for key, value in info.items():
        print(f"{key}: {value}")

while True:
    os.system("cls")

    print("======= SYSTEM PERFORMANCE DASHBOARD =======")

    print_dash("CPU INFO", Get_CPU_INFO())
    print_dash("MEMORY INFO", Get_MEMORY_INFO())
    print_dash("DISK INFO", Get_DISK_INFO())
    print_dash("NETWORK INFO", Get_NETWORK_INFO())
    print_dash("BATTERY INFO", Get_BATTERY_INFO())

    print("\nRefreshing every 1 second... (Press Ctrl + C to stop)")

    time.sleep(1)
