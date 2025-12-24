import os
import psutil
import streamlit as st
from streamlit_autorefresh import st_autorefresh


st.set_page_config(page_title="System Performance Dashboard", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("## 💻 System Performance Dashboard")

# 🔁 Auto refresh every 1 second
st_autorefresh(interval=1000, key="refresh")

st.sidebar.header('Dashboard ')

HISTORY_LIMIT = 60 # Store last 60 seconds of data (assuming 1 update per second)


# ---------------- FUNCTIONS ---------------- #

def bytes_to_readable(num):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024

def cpu_info():
    freq = psutil.cpu_freq()
    return psutil.cpu_percent(), psutil.cpu_count(), freq.current

def memory_info():
    mem = psutil.virtual_memory()
    return mem.percent, bytes_to_readable(mem.used), bytes_to_readable(mem.total)

def disk_info():
    path = "C:\\" if os.name == "nt" else "/"
    disk = psutil.disk_usage(path)
    return disk.percent, bytes_to_readable(disk.used), bytes_to_readable(disk.total)

def network_info():
    net = psutil.net_io_counters()
    return bytes_to_readable(net.bytes_sent), bytes_to_readable(net.bytes_recv)

def battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return battery.percent, battery.power_plugged
    return None, None

# ---------------- LAYOUT ---------------- #

col1, col2, col3 = st.columns(3)

cpu_usage, cores, freq = cpu_info()
col1.metric("CPU Usage", f"{cpu_usage} %")
col1.caption(f"Cores: {cores} | {freq:.0f} MHz")

mem_percent, mem_used, mem_total = memory_info()
col2.metric("RAM Usage", f"{mem_percent} %")
col2.caption(f"{mem_used} / {mem_total}")

disk_percent, disk_used, disk_total = disk_info()
col3.metric("Disk Usage", f"{disk_percent} %")
col3.caption(f"{disk_used} / {disk_total}")


if "history" not in st.session_state:
    st.session_state.history = {"cpu": [], "ram": [], "disk": []}

history = st.session_state.history
history["cpu"].append(cpu_usage)
history["ram"].append(mem_percent)
history["disk"].append(disk_percent)

for key in history:
    if len(history[key]) > HISTORY_LIMIT:
        history[key] = history[key][-HISTORY_LIMIT:]

st.subheader("Usage Trends (last 60s)")
chart_col1, chart_col2, chart_col3 = st.columns(3)
chart_col1.line_chart(history["cpu"], height=200)
chart_col1.caption("CPU %")
chart_col2.line_chart(history["ram"], height=200)
chart_col2.caption("RAM %")
chart_col3.line_chart(history["disk"], height=200)
chart_col3.caption("Disk %")

st.divider()

col4, col5 = st.columns(2)

sent, recv = network_info()
col4.metric("Network Sent", sent)
col4.metric("Network Received", recv)

battery_percent, plugged = battery_info()
if battery_percent is not None:
    col5.metric("Battery", f"{battery_percent} %")
    col5.caption("Charging ⚡" if plugged else "On Battery 🔋")
else:
    col5.warning("No battery detected")
