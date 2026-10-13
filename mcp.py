import time
from mcp3021 import MCP3021
from adc_plot import plot_voltage_vs_time


adc = MCP3021(dynamic_range=5.0)

voltage_values = []
time_values = []
duration = 3.0

try:
    start_time = time.time()
    while time.time() - start_time < duration:
        voltage_values.append(adc.get_voltage())
        time_values.append(time.time() - start_time)

    plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
finally:
    adc.deinit()
