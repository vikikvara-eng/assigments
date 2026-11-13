
class BankAccount:
    bank_name = "BOG"
    def __init__(self, card_type, owner, balance):
        self.card_type = card_type
        self.owner = owner
        self.__balance = balance if balance >= 0 else 0
    @property
    def balance(self):
        return self.__balance
    @balance.setter
    def balance(self, amount):
        if amount < 0:
            print("ბალანსი არ შეიძლება იყოს უარყოფითი")
        else:
            self.__balance = amount
    @balance.deleter
    def balance(self):
        del self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.balance = self.balance + amount
        else:
            print("თანხის შეტანა შეუძლებელია")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance = self.balance - amount
        else:
            print("თანხის გამოტანა შეუძლებელია")

    @classmethod
    def get_bank_name(cls):
        return cls.bank_name

    @staticmethod
    def calculate_tax(amount):
        tax_rate = 0.15
        return amount * tax_rate


class SavingsAccount(BankAccount):

    def __init__(self, card_type, owner, balance, interest_rate):
        super().__init__(card_type, owner, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        return self.balance * self.interest_rate / 100

    def apply_interest(self):
        interest = self.calculate_interest()
        self.deposit(interest)

    def withdraw(self, amount):
        total_amount = amount + 2

        if amount > 0 and total_amount <= self.balance:
            self.balance = self.balance - total_amount
        else:
            print("თანხის გამოტანა შეუძლებელია")


class CreditAccount(BankAccount):

    def __init__(self, card_type, owner, balance, credit_limit):
        super().__init__(card_type, owner, balance)
        self.credit_limit = credit_limit

    @BankAccount.balance.setter
    def balance(self, amount):
        if amount < -self.credit_limit:
            print("საკრედიტო ლიმიტი გადაჭარბებულია")
        else:
            self._BankAccount__balance = amount

    def withdraw(self, amount):
        if amount > 0 and (self.balance - amount) >= -self.credit_limit:
            self.balance = self.balance - amount
        else:
            print("თანხის გამოტანა შეუძლებელია")
