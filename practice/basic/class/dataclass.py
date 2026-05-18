from dataclasses import dataclass

@dataclass
class Car:
    name : str
    type : str
    price : int
    maker : str
    

c1 = Car(
    name="ラパン", 
    type="軽自動車", 
    price=2000000, 
    maker="スズキ"
)

print(c1)
print(c1.name)
print(c1.type)
print(f"{c1.price:,}")
print(c1.maker)

c2 = Car(
    name="アルファード",
    type="普通車",
    price=100000000,
    maker="トヨタ"
)

print(c2)
print(c2.name)
print(c2.type)
print(f"{c2.price:,}")
print(c2.maker)