import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

def get_triangle_wave_amplitude(freq, time_):
phase = (freq * time_) % 1.0
return 1.0 - 2.0 * abs(phase - 0.5)

try:
dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, False)
t = 0.0
dt = 1.0 / sampling_frequency
while True:
normalized = get_triangle_wave_amplitude(signal_frequency, t)
voltage = normalized * amplitude
dac.set_voltage(voltage)
sg.wait_for_sampling_period(sampling_frequency)
t += dt
finally:
dac. deinit ()
