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
        self.create_product_frame.pack()

        self.create_to_stock_button = tk.Button(self.create_product_frame, text="Stocks")
        self.create_to_restock_button = tk.Button(self.create_product_frame, text="Sell & Restock")
        self.create_to_stock_button.grid(row=0, column=0)
        self.create_to_restock_button.grid(row=0, column=1)

        self.product_name_label = tk.Label(self.create_product_frame, text="Name")
        self.product_name_entry = tk.Entry(self.create_product_frame)
        self.base_price_label = tk.Label(self.create_product_frame, text="Base Price:")
        self.base_price_entry = tk.Entry(self.create_product_frame)
        self.product_name_label.grid(row=1, column=0)
        self.product_name_entry.grid(row=1, column=1)
        self.base_price_label.grid(row=2, column=0)
        self.base_price_entry.grid(row=2, column=1)

        self.confirm_product_button = tk.Button(self.create_product_frame, text="Confirm")
        self.confirm_product_button.grid(row=3, column=0, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    store_gui = StoreGUI(root)
    root.mainloop()