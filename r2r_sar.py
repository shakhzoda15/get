import time
from R2R_ADC import R2R_ADC
from adc_plot import plot_voltage_vs_time


adc = R2R_ADC(dynamic_range=3.3, compare_time=0.0001)

voltage_values = []
time_values = []
duration = 3.0

try:
    start_time = time.time()
    while time.time() - start_time < duration:
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(time.time() - start_time)

    plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
finally:
    del adc
