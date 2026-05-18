class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.loans = False #本の状態を確認する変数を用意（真偽値）
        
    def book_lend(self):
        if not self.loans == False:
            print(f"既に本は貸し出し中です")
        else:
            self.loans = True
            print(f"本を貸し出しました")
    
    def book_return(self):
        if not self.loans == True:
            print(f"貸し出し中の本はありません")
        else:
            self.loans = False
            print(f"本を返却しました")
    
    def show_book(self):
        if self.loans == True:
            print(f"タイトル: {self.title}, 著者名: {self.author}, 状態: 貸し出し中")
        else:
            print(f"タイトル: {self.title}, 著者名: {self.author}, 状態: なし")

book = Book("小説 A", "Claude")
book.show_book()
book.book_lend()
book.show_book()
book.book_lend()
book.book_return()