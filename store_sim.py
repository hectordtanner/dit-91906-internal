import tkinter as tk

class Product:
    def __init__(self, name: str, base_price: int):
        self.name = name
        self.base_price = base_price
        self.stock = 0

class StoreGUI:
    def __init__(self, parent):
        self.products: list[Product] = []

        self.stock_level_frame = tk.Frame(parent)
        self.sell_restock_frame = tk.Frame(parent)
        self.create_product_frame = tk.Frame(parent)

        self.create_to_stock_button = tk.Button(self.create_product_frame, text="Stocks")
        self.create_to_restock_button = tk.Button(self.create_product_frame, text="Sell & Restock")

if __name__ == "__main__":
    root = tk.Tk()
    store_gui = StoreGUI(root)
    root.mainloop()