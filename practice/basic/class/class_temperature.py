class Temperature:
    def __init__(self,temperature, unit):
        self.temperature = temperature
        self.unit = unit
        self.total_temperature = None
    
    def change_celsius(self):
        self.total_temperature = (self.temperature - 32) * 5 // 9
        print(self.total_temperature,self.unit)
        
    def change_fahrenheit(self):
        self.total_temperature = self.temperature * 9 // 5 + 32
        print(self.total_temperature,self.unit)
        
    def temperature_now(self):
        if self.total_temperature == None:
            self.total_temperature = self.temperature
        print(f"現在の温度: {self.total_temperature} {self.unit}")
        
temp_1 = Temperature(100, "C")
temp_1.change_celsius()

temp_2 = Temperature(32, "F")
temp_2.change_fahrenheit()

temp_1.temperature_now()
temp_2.temperature_now()
