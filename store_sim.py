"""Store simulator, with product creation, selling and restocking, money and profits, and external save files."""

import tkinter as tk
from tkinter import messagebox

DEFAULT_PROFIT_MARGIN = 1.2
STARTING_MONEY = 1100
PRODUCT_CREATION_PRICE = 1000
PRODUCTION_PRICE = 10000
STOCK_WARNING_LEVEL = 10
TICK_TIME = 1000
RECENT_PURCHASE_FACTOR = 0.1
RECENT_PURCHASE_CONST = 0.1
PROFIT_MARGIN_FACTOR = 0.01

class Product:
    """Store the information of a single product."""
    def __init__(self, name: str, base_price: int):
        """Add the product's data to the object."""
        self.name = name
        self.base_price = base_price
        self.stock = 0
        self.total_sold = 0
        self.profit_margin = DEFAULT_PROFIT_MARGIN
        self.production = 0
        self.recent_purchases = 0.0
    
    def save_file_str(self):
        return f"{self.name}|{self.base_price}|{self.stock}|{self.total_sold}|{self.profit_margin}|{self.production}|{self.recent_purchases}"

class StoreGUI:
    """Create and display program GUI."""

    def __init__(self, parent):
        """Create GUI elements with tkinter."""
        self.products: list[Product] = []
        self.product_names: list[str] = []
        self.selected_product = tk.StringVar()
        self.selected_product.set("--Choose an option--")
        self.selected_save = tk.StringVar()
        self.selected_save.set("save_1.txt")
        self.sell_or_restock = tk.BooleanVar()
        self.sell_or_restock.set(True)
        self.total_sales = 0
        self.money = STARTING_MONEY
        self.saves: list[str] = ["save_1.txt", "save_2.txt", "save_3.txt", "save_4.txt"]

        self.stock_level_frame = tk.Frame(parent)
        self.sell_restock_frame = tk.Frame(parent)
        self.production_frame = tk.Frame(parent)
        self.create_product_frame = tk.Frame(parent)
        self.saves_frame = tk.Frame(parent)
        self.nav_bar = tk.Frame(parent)
        self.frames = [self.stock_level_frame, self.sell_restock_frame, self.production_frame, self.create_product_frame, self.saves_frame]

        self.nav_bar.grid(row=0, column=0)
        self.create_product_frame.grid(row=1, column=0)

        self.to_stock_button = tk.Button(self.nav_bar, text="Stocks", command=lambda: self.move_to_frame(self.stock_level_frame))
        self.to_restock_button = tk.Button(self.nav_bar, text="Sell & Restock", command=lambda: self.move_to_frame(self.sell_restock_frame))
        self.to_production_button = tk.Button(self.nav_bar, text="Production", command=lambda: self.move_to_frame(self.production_frame))
        self.to_create_button = tk.Button(self.nav_bar, text="Create product", command=lambda: self.move_to_frame(self.create_product_frame))
        self.to_saves_button = tk.Button(self.nav_bar, text="Saves", command=lambda: self.move_to_frame(self.saves_frame))

        self.to_stock_button.grid(row=0, column=0)
        self.to_restock_button.grid(row=0, column=1)
        self.to_production_button.grid(row=0, column=2)
        self.to_create_button.grid(row=0, column=3)
        self.to_saves_button.grid(row=0, column=4)

        self.product_name_label = tk.Label(self.create_product_frame, text="Name")
        self.product_name_entry = tk.Entry(self.create_product_frame)
        self.base_price_label = tk.Label(self.create_product_frame, text="Base Price:")
        self.base_price_entry = tk.Entry(self.create_product_frame)
        self.confirm_product_button = tk.Button(self.create_product_frame, text=f"Confirm (${PRODUCT_CREATION_PRICE})", command=lambda: self.create_product(self.product_name_entry.get(), self.base_price_entry.get()))

        self.product_name_label.grid(row=0, column=0)
        self.product_name_entry.grid(row=0, column=1)
        self.base_price_label.grid(row=1, column=0)
        self.base_price_entry.grid(row=1, column=1)
        self.confirm_product_button.grid(row=2, column=0, columnspan=2)

        self.money_label = tk.Label(self.stock_level_frame, text="")
        self.low_stock_warning_label = tk.Label(self.stock_level_frame, text="")
        self.stock_levels_label = tk.Label(self.stock_level_frame, text="")
        self.total_sales_label = tk.Label(self.stock_level_frame, text="")

        self.money_label.grid(row=0, column=0)
        self.low_stock_warning_label.grid(row=1, column=0)
        self.stock_levels_label.grid(row=2, column=0)
        self.total_sales_label.grid(row=3, column=0)

        self.sell_radiobutton = tk.Radiobutton(self.sell_restock_frame, text="Sell ", variable=self.sell_or_restock, value=True, command=lambda: self.update_profit_label(0))
        self.restock_radiobutton = tk.Radiobutton(self.sell_restock_frame, text="Restock ", variable=self.sell_or_restock, value=False, command=lambda: self.update_profit_label(0))
        self.sell_num_entry = tk.Entry(self.sell_restock_frame)
        self.sell_num_entry.bind("<KeyRelease>", self.update_profit_label)
        self.of_label = tk.Label(self.sell_restock_frame, text=" of ")
        self.sell_of_dropdown = tk.OptionMenu(self.sell_restock_frame, self.selected_product, "--Choose an option--", *self.product_names, command=self.update_profit_label)
        self.confirm_sell_button = tk.Button(self.sell_restock_frame, text="Confirm", command=lambda: self.sell_restock(self.sell_num_entry.get(), self.selected_product.get(), self.sell_or_restock.get()))

        self.sell_radiobutton.grid(row=0, column=0)
        self.restock_radiobutton.grid(row=1, column=0)
        self.sell_num_entry.grid(row=0, column=1, rowspan=2)
        self.of_label.grid(row=0, column=2, rowspan=2)
        self.sell_of_dropdown.grid(row=0, column=3, rowspan=2)
        self.confirm_sell_button.grid(row=2, column=0, columnspan=4)

        self.save_select_label = tk.Label(self.saves_frame, text="Save: ")
        self.save_select = tk.OptionMenu(self.saves_frame, self.selected_save, *self.saves)
        self.save_load_button = tk.Button(self.saves_frame, text="Load", command=lambda: self.load_save(self.selected_save.get()))
        self.save_overwrite_button = tk.Button(self.saves_frame, text="Overwrite", command=lambda: self.overwrite_save(self.selected_save.get()))

        self.save_select_label.grid(row=0, column=0)
        self.save_select.grid(row=0, column=1)
        self.save_load_button.grid(row=1, column=0)
        self.save_overwrite_button.grid(row=1, column=1)

        self.buy_production_label = tk.Label(self.production_frame, text="Buy ")
        self.production_num_entry = tk.Entry(self.production_frame)
        self.production_num_entry.bind("<KeyRelease>", self.update_production_label)
        self.per_s_label = tk.Label(self.production_frame, text="/s production of ")
        self.production_of_dropdown = tk.OptionMenu(self.production_frame, self.selected_product, "--Choose an option--", *self.product_names, command=self.update_production_label)
        self.confirm_production_button = tk.Button(self.production_frame, text="Confirm", command=lambda: self.buy_production(self.selected_product.get(), self.production_num_entry.get()))

        self.buy_production_label.grid(row=0, column=0)
        self.production_num_entry.grid(row=0, column=1)
        self.per_s_label.grid(row=0, column=2)
        self.production_of_dropdown.grid(row=0, column=3)
        self.confirm_production_button.grid(row=1, column=0, columnspan=4)

        messagebox.showinfo(title="Welcome!", message="Create your first product to begin")

    def reset_screen(self):
        """Reset display by using grid_forget on all frames."""
        for frame in self.frames:
            frame.grid_forget()

    def move_to_frame(self, frame: tk.Frame):
        """Change to and update the specified frame, and checks that a product exists."""
        if len(self.products) > 0:
            self.update_stock_level()
            self.reset_screen()
            frame.grid(row=1, column=0)
            
            if frame == self.sell_restock_frame:
                self.sell_of_dropdown.destroy()
                self.sell_of_dropdown = tk.OptionMenu(self.sell_restock_frame, self.selected_product, *self.product_names, command=self.update_profit_label)
                self.sell_of_dropdown.grid(row=0, column=3, rowspan=2)
            if frame == self.production_frame:
                self.production_of_dropdown.destroy()
                self.production_of_dropdown = tk.OptionMenu(self.production_frame, self.selected_product, *self.product_names, command=self.update_production_label)
                self.production_of_dropdown.grid(row=0, column=3)
        else:
            messagebox.showerror(title="No Products", message="Please create your first product")

    def create_product(self, product_name: str, price: str):
        """Create a new product."""
        if len(product_name.strip()) >= 3:
            if not ("|" in product_name or "\n" in product_name):
                if not (product_name.strip() in self.product_names):
                        if int_validation("Please enter a valid price", True, price):
                            if int(price) > 0:
                                if self.money >= PRODUCT_CREATION_PRICE:
                                    self.products.append(Product(product_name, int(price)))
                                    self.product_names.append(product_name)
                                    self.product_name_entry.delete(0, tk.END)
                                    self.base_price_entry.delete(0, tk.END)
                                    self.product_name_entry.focus()
                                    self.money -= round(PRODUCT_CREATION_PRICE, 2)
                                else:
                                    messagebox.showerror(title="No Money", message="You do not have enough money")
                            else:
                                messagebox.showerror(title="Invalid Price", message= "Please enter a valid price")
                        else:
                            self.base_price_entry.delete(0, tk.END)
                            self.base_price_entry.focus()
                else:
                    messagebox.showerror(title="Invalid Name", message="Product name already exists")
                    self.product_name_entry.delete(0, tk.END)
                    self.product_name_entry.focus()
            else:
                messagebox.showerror(title="Invalid Name", message="Product names cannot contain '|'")
                self.product_name_entry.delete(0, tk.END)
                self.product_name_entry.focus()
        else:
            messagebox.showerror(title="Invalid Name", message="Product names must be at least 3 characters")
            self.product_name_entry.delete(0, tk.END)
            self.product_name_entry.focus()

    def sell_restock(self, amount: str, product_name: str, is_selling: bool):
        """Sell and restock products."""
        can_int = int_validation("Please enter a valid amount", True, amount)

        if can_int:
            if product_name == "--Choose an option--":
                messagebox.showerror(title="No Product Selected", message="Please select a product")
            else:
                selling_product = self.identify_product(product_name)

                if is_selling:
                    if selling_product.stock - int(amount) >= 0:
                        selling_product.stock -= int(amount)
                        selling_product.total_sold += int(amount)
                        self.total_sales += int(amount)
                        self.money += round(int(amount) * selling_product.base_price * selling_product.profit_margin, 2)
                        selling_product.recent_purchases += int(amount)
                    else:
                        messagebox.showerror(title="No Stock", message=f"You do not have {amount} of {product_name}")   
  
                else:
                    if self.money - (int(amount) * selling_product.base_price) >= 0:
                        self.money -= round(int(amount) * selling_product.base_price, 2)
                        selling_product.stock += int(amount)
                    else:
                        messagebox.showerror(title="No Money", message="You do not have enough money")

        self.sell_num_entry.delete(0, tk.END)
        self.sell_num_entry.focus()
    
    def identify_product(self, name: str):
        """Identify and return the product in self.products with a specified name, returning an empty product if it does not exist."""
        identified_product = Product("", 0)
        for product in self.products:
            if product.name == name:
                identified_product = product
        return identified_product

    def load_save(self, save: str):
        """Load an external save file from a specified file in the save_files folder."""
        if messagebox.askokcancel(title="Load Save", message="Are you sure you want to load this save? It will delete the save currently open if it has not been saved"):
            try:
                try:
                    with open("save_files/" + save, "r") as save_file:
                        save_data = save_file.read().splitlines()
                    self.money = round(float(save_data[0].split("|")[0]), 2)
                    self.total_sales = int(save_data[0].split("|")[1])
                    save_data.pop(0)

                    self.product_names = []
                    self.products = []
                    for product_data in save_data:
                        product_data = product_data.split("|")
                        self.product_names.append(product_data[0])
                        new_product = Product(product_data[0], int(product_data[1]))
                        new_product.stock = int(product_data[2])
                        new_product.total_sold = int(product_data[3])
                        new_product.profit_margin = round(float(product_data[4]), 3)
                        new_product.production = int(product_data[5])
                        new_product.recent_purchases = float(product_data[6])
                        self.products.append(new_product)
                except ValueError:
                    messagebox.showerror(title="Save Error", message="File corrupted")

            except FileNotFoundError:
                messagebox.showerror(title="Save Error", message="File does not exist.")

    def overwrite_save(self, save: str):
        """Overwrite an external save file from a specified file in the save_files folder."""
        if messagebox.askokcancel(title="Overwrite Save", message="Are you sure you want to overwrite this save? It will delete the save currently stored there."):
            full_save_str = f"{self.money}|{self.total_sales}"
            for product in self.products:
                full_save_str += "\n" + product.save_file_str()

            with open("save_files/" + save, "w") as save_file:
                save_file.write(full_save_str)
        
    def tick_update(self):
        """Runs game ticks with .after"""
        for product in self.products:
            product.stock += product.production
            product.recent_purchases = round(product.recent_purchases - abs(product.recent_purchases * RECENT_PURCHASE_FACTOR) - RECENT_PURCHASE_CONST, 3)
            product.profit_margin -= round(product.recent_purchases * PROFIT_MARGIN_FACTOR, 3)
        self.update_profit_label(0)
        self.update_stock_level()
        root.after(TICK_TIME, self.tick_update)
    
    def update_stock_level(self):
        """Update the stock level labels"""
        stock_label_str = ""
        warning_label_str = ""
        for product in self.products:
            stock_label_str += f"{product.name}: {product.stock}. Total sold: {product.total_sold}\n"
            if product.stock < STOCK_WARNING_LEVEL:
                warning_label_str += f"WARNING: {product.name} has low stock ({product.stock})\n"
        self.money_label.configure(text=f"You have ${self.money}")
        self.low_stock_warning_label.configure(text=warning_label_str)
        self.stock_levels_label.configure(text=stock_label_str)
        self.total_sales_label.configure(text=f"Total Sales: {self.total_sales}")
    
    def update_profit_label(self, arb):
        """Update the profit label."""
        displayed_product = self.identify_product(self.selected_product.get())
        amount = self.sell_num_entry.get()

        if int_validation("", False, amount):
            if self.sell_or_restock.get():
                sale_amount = int(amount) * displayed_product.base_price * displayed_product.profit_margin
            else:
                sale_amount = int(amount) * displayed_product.base_price
            self.confirm_sell_button.configure(text=f"Confirm (for ${round(sale_amount, 2)})")
        else:
            self.confirm_sell_button.configure(text=f"Confirm")

    def update_production_label(self, arb):
        """Update the profit label."""
        displayed_product = self.identify_product(self.selected_product.get())
        amount = self.production_num_entry.get()

        if int_validation("", False, amount):
            sale_amount = displayed_product.base_price * PRODUCTION_PRICE
            self.confirm_production_button.configure(text=f"Confirm (for ${round(sale_amount, 2)})")
        else:
            self.confirm_production_button.configure(text=f"Confirm")
    
    def buy_production(self, product_name: str, num: str):
        """Purchase production"""
        product = self.identify_product(product_name)
        if int_validation("", False, num):
            if self.money - product.base_price * PRODUCTION_PRICE > 0:
                product.production += int(num)
                self.money -= round(product.base_price * PRODUCTION_PRICE, 2)
            else:
                messagebox.showerror(title="No Money", message="You do not have enough money")


def int_validation(error_text: str, display_error: bool, value):
    """Return True if value is able to be turned into an int, False if not."""
    try:
        value = int(value)
        return True

    except ValueError:
        if display_error:
            messagebox.showerror(title="Invalid Value", message=error_text) 
        return False


if __name__ == "__main__":
    root = tk.Tk()
    store_gui = StoreGUI(root)
    root.focus_force()
    store_gui.tick_update()
    root.mainloop()
