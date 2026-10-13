import smbus


class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"Принятые данные: {data}, "
                  f"Старший байт: {upper_data_byte:x}, "
                  f"Младший байт: {lower_data_byte:x}, "
                  f"Число: {number}")
        return number

    def get_voltage(self):
        number = self.get_number()
        max_number = 2 ** 10 - 1          # MCP3021 — 10-битный АЦП
        voltage = self.dynamic_range * number / max_number
        return voltage


if __name__ == "__main__":
    try:
        adc = MCP3021(dynamic_range=5.0, verbose=False)
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(1)
    finally:
        adc.deinit()
