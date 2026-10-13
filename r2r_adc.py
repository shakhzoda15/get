import RPi.GPIO as GPIO
import time


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def __del__(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        bits = [(number >> i) & 1 for i in range(len(self.bits_gpio) - 1, -1, -1)]
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_adc(self):
        max_number = 2 ** len(self.bits_gpio) - 1
        for number in range(max_number + 1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio):
                return number
        return max_number

    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        max_number = 2 ** len(self.bits_gpio) - 1
        return self.dynamic_range * number / max_number

    def successive_approximation_adc(self):
        max_number = 2 ** len(self.bits_gpio) - 1
        result = 0
        for bit in range(len(self.bits_gpio) - 1, -1, -1):
            trial = result | (1 << bit)
            self.number_to_dac(trial)
            time.sleep(self.compare_time)
            if not GPIO.input(self.comp_gpio):
                result = trial
            if self.verbose:
                print(f"bit={bit}  trial={trial:3d}  result={result:3d}")
        if result < max_number:
            result += 1
        return result

    def get_sar_voltage(self):
        number = self.successive_approximation_adc()
        max_number = 2 ** len(self.bits_gpio) - 1
        return self.dynamic_range * number / max_number
