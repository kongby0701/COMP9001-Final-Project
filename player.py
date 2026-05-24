class Player:
    def __init__(self, name, color, symbol, money=1500):
        self.name = name
        self.color = color
        self.symbol = symbol
        self.money = money
        self.position = 0
        self.in_jail = False
        self.jail_turns = 0
        self.properties = []
        self.get_out_of_jail_cards = 0
    
    def move(self, steps):
        self.position = (self.position + steps) % 40
    
    def add_money(self, amount):
        self.money += amount
    
    def remove_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def go_to_jail(self):
        self.in_jail = True
        self.jail_turns = 0
        self.position = 30  # 监狱位置
    
    def get_out_of_jail(self):
        self.in_jail = False
        self.jail_turns = 0
    
    def buy_property(self, property):
        if self.money >= property.price:
            self.money -= property.price
            self.properties.append(property)
            property.owner = self
            return True
        return False
    
    def __str__(self):
        return f"Player: {self.name} ({self.color}, {self.symbol})\nMoney: ${self.money}\nPosition: {self.position}\nIn Jail: {self.in_jail}\nProperties: {len(self.properties)}"
