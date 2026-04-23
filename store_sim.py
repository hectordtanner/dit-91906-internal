import tkinter as tk

class Product:
    """Store the information of a single product"""
    def __init__(self, name: str, base_price: int):
        self.name = name
        self.base_price = base_price
        self.stock = 0

class StoreGUI:
    """Create and display program GUI"""

    def __init__(self, parent):
        """Create GUI elements"""
        self.products: list[Product] = []
        self.product_names: list[str] = []
        self.selected_product = tk.StringVar()
        self.selected_product.set("--Choose an option--")
        self.sell_or_restock = tk.BooleanVar()
        self.sell_or_restock.set(True)

        self.stock_level_frame = tk.Frame(parent)
        self.sell_restock_frame = tk.Frame(parent)
        self.create_product_frame = tk.Frame(parent)
        self.nav_bar = tk.Frame(parent)
        self.nav_bar.grid(row=0, column=0)
        self.sell_restock_frame.grid(row=1, column=0)

        self.to_stock_button = tk.Button(self.nav_bar, text="Stocks")
        self.to_restock_button = tk.Button(self.nav_bar, text="Sell & Restock")
        self.to_create_button = tk.Button(self.nav_bar, text="Create product")
        self.to_stock_button.grid(row=0, column=0)
        self.to_restock_button.grid(row=0, column=1)
        self.to_create_button.grid(row=0, column=2)

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

        self.stock_to_restock_button = tk.Button(self.stock_level_frame, text="Sell & Restock")
        

        self.restock_to_stock_button = tk.Button(self.sell_restock_frame, text="Stocks")
        self.restock_to_create_button = tk.Button(self.sell_restock_frame, text="Create Product")
        self.restock_to_stock_button.grid(row=0, column=0, columnspan=2)
        self.restock_to_create_button.grid(row=0, column=2, columnspan=2)
        
        self.sell_radiobutton = tk.Radiobutton(self.sell_restock_frame, text="Sell ", variable=self.sell_or_restock, value=True)
        self.restock_radiobutton = tk.Radiobutton(self.sell_restock_frame, text="Restock ", variable=self.sell_or_restock, value=False)
        self.sell_num_entry = tk.Entry(self.sell_restock_frame)
        self.of_label = tk.Label(self.sell_restock_frame, text=" of ")
        self.sell_of_dropdown = tk.OptionMenu(self.sell_restock_frame, self.selected_product, "--Choose an option--", *self.product_names)
        self.sell_radiobutton.grid(row=1, column=0)
        self.restock_radiobutton.grid(row=2, column=0)
        self.sell_num_entry.grid(row=1, column=1, rowspan=2)
        self.of_label.grid(row=1, column=2, rowspan=2)
        self.sell_of_dropdown.grid(row=1, column=3, rowspan=2)


if __name__ == "__main__":
    root = tk.Tk()
    store_gui = StoreGUI(root)
    root.mainloop()