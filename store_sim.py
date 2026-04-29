import tkinter as tk
from tkinter import messagebox

DEFAULT_PROFIT_MARGIN = 1.2
STARTING_MONEY = 110000000
PRODUCT_CREATION_PRICE = 1000
STOCK_WARNING_LEVEL = 10

class Product:
    """Store the information of a single product."""
    def __init__(self, name: str, base_price: int):
        """Add the product's data to the object."""
        self.name = name
        self.base_price = base_price
        self.stock = 0
        self.total_sold = 0
        self.profit_margin = DEFAULT_PROFIT_MARGIN

class StoreGUI:
    """Create and display program GUI."""

    def __init__(self, parent):
        """Create GUI elements with tkinter."""
        self.products: list[Product] = []
        self.product_names: list[str] = []
        self.selected_product = tk.StringVar()
        self.selected_product.set("--Choose an option--")
        self.sell_or_restock = tk.BooleanVar()
        self.sell_or_restock.set(True)
        self.total_sales = 0
        self.money = STARTING_MONEY

        self.stock_level_frame = tk.Frame(parent)
        self.sell_restock_frame = tk.Frame(parent)
        self.create_product_frame = tk.Frame(parent)
        
        self.nav_bar = tk.Frame(parent)
        self.nav_bar.grid(row=0, column=0)
        self.create_product_frame.grid(row=1, column=0)

        self.to_stock_button = tk.Button(self.nav_bar, text="Stocks", command=self.move_to_stock)
        self.to_restock_button = tk.Button(self.nav_bar, text="Sell & Restock", command=self.move_to_sell_restock)
        self.to_create_button = tk.Button(self.nav_bar, text="Create product", command=self.move_to_create)
        
        self.to_stock_button.grid(row=0, column=0)
        self.to_restock_button.grid(row=0, column=1)
        self.to_create_button.grid(row=0, column=2)

        self.product_name_label = tk.Label(self.create_product_frame, text="Name")
        self.product_name_entry = tk.Entry(self.create_product_frame)
        self.base_price_label = tk.Label(self.create_product_frame, text="Base Price:")
        self.base_price_entry = tk.Entry(self.create_product_frame)
        self.confirm_product_button = tk.Button(self.create_product_frame, text="Confirm ($1000)", command=lambda: self.create_product(self.product_name_entry.get(), self.base_price_entry.get()))
        
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
        self.confirm_sell_button = tk.Button(self.sell_restock_frame, text="Confirm (for $X)", command=lambda: self.sell_restock(self.sell_num_entry.get(), self.selected_product.get(), self.sell_or_restock.get()))
        
        self.sell_radiobutton.grid(row=0, column=0)
        self.restock_radiobutton.grid(row=1, column=0)
        self.sell_num_entry.grid(row=0, column=1, rowspan=2)
        self.of_label.grid(row=0, column=2, rowspan=2)
        self.sell_of_dropdown.grid(row=0, column=3, rowspan=2)
        self.confirm_sell_button.grid(row=2, column=0, columnspan=4)

    def reset_screen(self):
        """Reset display by using grid_forget on all frames"""
        self.stock_level_frame.grid_forget()
        self.sell_restock_frame.grid_forget()
        self.create_product_frame.grid_forget()

    def move_to_stock(self):
        """Change to and update the stock level screen, and checks that a product exists."""
        if len(self.products) > 0:
            self.reset_screen()
            self.stock_level_frame.grid(row=1, column=0)
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
        else:
            messagebox.showerror(title="No Products", message="Please create your first product")

    def move_to_sell_restock(self):
        """Change to and update the sell & restock level screen, and checks that a product exists."""
        if len(self.products) > 0:
            self.reset_screen()
            self.sell_restock_frame.grid(row=1, column=0)
            self.sell_of_dropdown.destroy()
            self.sell_of_dropdown = tk.OptionMenu(self.sell_restock_frame, self.selected_product, *self.product_names, command=self.update_profit_label)
            self.sell_of_dropdown.grid(row=0, column=3, rowspan=2)
            self.update_profit_label(0)
        else:
            messagebox.showerror(title="No Products", message="Please create your first product")

    def move_to_create(self):
        """Change to product creation screen, and checks that a product exists.."""
        self.reset_screen()
        self.create_product_frame.grid(row=1, column=0)

    def create_product(self, product_name: str, price: str):
        """Create a new product."""
        if len(product_name.strip()) >= 3:
            can_int = int_validation("Please enter a valid price", True, price)
            if can_int:
                if self.money >= PRODUCT_CREATION_PRICE:
                    self.products.append(Product(product_name, int(price)))
                    self.product_names.append(product_name)
                    self.product_name_entry.delete(0, tk.END)
                    self.base_price_entry.delete(0, tk.END)
                    self.product_name_entry.focus()
                    self.money -= PRODUCT_CREATION_PRICE
                else:
                    messagebox.showerror(title="No Money", message="You do not have enough money")
            else:
                self.base_price_entry.delete(0, tk.END)
                self.base_price_entry.focus()
        else:
            messagebox.showerror(title="Invalid Name", message="Product names must be at least 3 non-space characters")
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
                        self.money += int(amount) * selling_product.base_price * selling_product.profit_margin
                    else:
                        messagebox.showerror(title="No Stock", message=f"You do not have {amount} of {product_name}")   
  
                else:
                    if self.money - (int(amount) * selling_product.base_price) >= 0:
                        self.money -= int(amount) * selling_product.base_price
                        selling_product.stock += int(amount)
                    else:
                        messagebox.showerror(title="No Money", message="You do not have enough money")

        self.sell_num_entry.delete(0, tk.END)
        self.sell_num_entry.focus()
        self.update_profit_label(0)
    
    def update_profit_label(self, arb):
        """Update the profit label, with an arbitrary parameter as some tkinter widgets require commands to have exaclty one parameter"""
        print("a")
        displayed_product = self.identify_product(self.selected_product.get())
        amount = self.sell_num_entry.get()

        if int_validation("", False, amount):
            
            if self.sell_or_restock.get():
                sale_amount = int(amount) * displayed_product.base_price * displayed_product.profit_margin
            else:
                sale_amount = int(amount) * displayed_product.base_price
            self.confirm_sell_button.configure(text=f"Confirm (for ${sale_amount})")
        else:
            self.confirm_sell_button.configure(text=f"Confirm")

    def identify_product(self, name: str):
        identified_product = Product("", 0)
        for product in self.products:
            if product.name == name:
                identified_product = product
        return identified_product

        
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
    root.mainloop()