class Product:
    total_products=0
    store_name = "TechShop Georgia"
    currency = "GEL"
    def __init__(self,name,price,stock,category,discount=0):
        self.name=name
        self.price=price
        self.stock=stock
        self.category=category
        self.discount=discount
        Product.total_products += 1
    def get_info(self):
        return f"პროდუქტის სახელი: {self.name}\nფასი: {self.currency}{self.price}\nმარაგი: {self.stock} ერთეული\nკატეგორია: {self.category}\nფასდაკლება: {self.discount}%"
    def apply_discount(self, percent):
        self.discount = percent
        print(f"{self.name} , {self.discount}")
    def update_stock(self, amount):
         if self.stock + amount < 0:
            print(f"ყურადღება! {self.name} მარაგი არასაკმარისია")
         else:
            self.stock += amount
            print(f"{self.name} მარაგი განახლდა: {self.stock} ერთეული")
    def calculate_final_price(self):
        discounted_price = self.price * (1 - self.discount / 100)
        return discounted_price
    @classmethod
    def get_total_products_count(cls):
        return cls.total_products
product1 = Product("laptop", 2500, 10,"electronics")
print(product1.get_info()) 
product2 = Product("mouse",80,25,"accessories")
print(product2.get_info())
product3 = Product("keyboard", 150, 15, "accessories", 5)
print(product3.get_info())
print(Product.get_total_products_count())
product1.apply_discount(20)
print(product1.calculate_final_price())
product1.update_stock(5)
product1.update_stock(-20)
print(product1.get_info())