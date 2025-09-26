class Product:
    def __init__(self, price, stock):
        self.price = price
        self.stock = stock
    
    def sellOne(self):
        self.stock -= 1
    
    def addStock(self, n=1):
        self.stock += n
    
    def changePrice(self, price):
        self.price = price
        
class Car(Product):
    def __init__(self, name, price, stock, sale_ratio):
        super().__init__(price, stock)
        self.name = name
        self.sale_ratio = sale_ratio
        
class Furniture(Product):
    def __init__(self, name, price, stock, sale_ratio):
        super().__init__(price, stock)
        self.name = name
        self.sale_ratio = sale_ratio
        
class addProduct:
    pass # 팩토리 패턴을 자연스럽게 습득