#銀行名・残高を管理するクラスを作成
class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.total_balance = None   #計算結果を入れる変数を用意
        
    def deposit(self, deposit_price):
        self.total_balance = self.balance + deposit_price
        print(f"￥{deposit_price:,}入金されました")
        
    def payment(self, payment_price):
        self.total_balance = self.total_balance - payment_price
        print(f"￥{payment_price:,}出金されました")
        
    def show_balance(self):
        print(f"残高は ￥{self.total_balance:,}です")
        
bank = BankAccount("Python銀行", 0)
print(f"{bank.name} ￥{bank.balance:,}")
bank.deposit(2000)
bank.payment(1000)
bank.show_balance()