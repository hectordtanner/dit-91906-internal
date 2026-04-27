import tkinter as tk
from tkinter import messagebox

class Product:
    """Store the information of a single product"""
    def __init__(self, name: str, base_price: int):
        """Add the product's data to the object"""
        self.name = name
        self.base_price = base_price
        self.stock = 1

class StoreGUI:
    """Create and display program GUI"""

    def __init__(self, parent):
        """Create GUI elements"""
        self.products: list[Product] = []
        self.product_names: list[str] = []
        self.selected_product = tk.StringVar()
        self.selected_product.set("--Choose an option--")
        self.sell_or_restock = tk.IntVar()
        self.sell_or_restock.set(-1)

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
        self.product_name_label.grid(row=0, column=0)
        self.product_name_entry.grid(row=0, column=1)
        self.base_price_label.grid(row=1, column=0)
        self.base_price_entry.grid(row=1, column=1)

        self.confirm_product_button = tk.Button(self.create_product_frame, text="Confirm", command=lambda: self.create_product(self.product_name_entry.get(), self.base_price_entry.get()))
        self.confirm_product_button.grid(row=2, column=0, columnspan=2)
        
        self.stock_levels_label = tk.Label(self.stock_level_frame, text="")
        self.stock_levels_label.grid(row=0, column=0)

        self.sell_radiobutton = tk.Radiobutton(self.sell_restock_frame, text="Sell ", variable=self.sell_or_restock, value=-1)
        self.restock_radiobutton = tk.Radiobutton(self.sell_restock_frame, text="Restock ", variable=self.sell_or_restock, value=1)
        self.sell_num_entry = tk.Entry(self.sell_restock_frame)
        self.of_label = tk.Label(self.sell_restock_frame, text=" of ")
        self.sell_of_dropdown = tk.OptionMenu(self.sell_restock_frame, self.selected_product, "--Choose an option--", *self.product_names)
        self.confirm_sell_button = tk.Button(self.sell_restock_frame, text="Confirm", command=lambda: self.sell_restock(self.sell_num_entry.get(), self.selected_product.get(), self.sell_or_restock.get()))
        self.sell_radiobutton.grid(row=0, column=0)
        self.restock_radiobutton.grid(row=1, column=0)
        self.sell_num_entry.grid(row=0, column=1, rowspan=2)
        self.of_label.grid(row=0, column=2, rowspan=2)
        self.sell_of_dropdown.grid(row=0, column=3, rowspan=2)
        self.confirm_sell_button.grid(row=2, column=0, columnspan=4)
        
    def reset_screen(self):
        """Reset display"""
        self.stock_level_frame.grid_forget()
        self.sell_restock_frame.grid_forget()
        self.create_product_frame.grid_forget()

    def move_to_stock(self):
        """Change to stock level screen"""
        if len(self.products) > 0:
            self.reset_screen()
            self.stock_level_frame.grid(row=1, column=0)
            label_str = ""
            for product in self.products:
                label_str += f"{product.name}: {product.stock}\n"
            self.stock_levels_label.configure(text=label_str)
        else:
            messagebox.showerror(title="No Products", message="Please create your first product")
    
    def move_to_sell_restock(self):
        """Change to sell & restock level screen"""
        if len(self.products) > 0:
            self.reset_screen()
            self.sell_restock_frame.grid(row=1, column=0)
            self.sell_of_dropdown.destroy()
            self.sell_of_dropdown = tk.OptionMenu(self.sell_restock_frame, self.selected_product, *self.product_names)
            self.sell_of_dropdown.grid(row=0, column=3, rowspan=2)
        else:
            messagebox.showerror(title="No Products", message="Please create your first product")
    
    def move_to_create(self):
        """Change to product creation screen"""
        self.reset_screen()
        self.create_product_frame.grid(row=1, column=0)
    
    def create_product(self, product_name: str, price: str):
        """Create a new product"""
        if len(product_name.strip()) >= 3:
            can_int = int_validation("Please enter a valid price", price)
            if can_int:
                self.products.append(Product(product_name, int(price)))
                self.product_names.append(product_name)
                self.product_name_entry.delete(0, tk.END)
                self.base_price_entry.delete(0, tk.END)
                self.product_name_entry.focus()
            else:
                self.base_price_entry.delete(0, tk.END)
                self.base_price_entry.focus()
        else:
            messagebox.showerror(title="Invalid Name", message="Product names must be at least 3 non-space characters")
            self.product_name_entry.delete(0, tk.END)
            self.product_name_entry.focus()
    
    def sell_restock(self, amount: str, product_name: str, is_selling: int):
        can_int = int_validation("Please enter a valid amount", amount)
        if can_int:
            if product_name == "--Choose an option--":
                messagebox.showerror(title="No Product Selected", message="Please select a product")
            else:
                selling_product = Product("", 0)
                for product in self.products:
                    if product.name == product_name:
                        selling_product = product

                if selling_product.stock + (int(amount) * is_selling) >= 0:
                    selling_product.stock += int(amount) * is_selling
                else:
                    messagebox.showerror(title="No Stock", message=f"You do not have {amount} of {product_name}")
                
                self.sell_num_entry.delete(0, tk.END)
                self.sell_num_entry.focus()
        else:
            self.sell_num_entry.delete(0, tk.END)
            self.sell_num_entry.focus()
    
def int_validation(error_text: str, value):
    try:
        value = int(value)
        return True
    except ValueError:
        messagebox.showerror(title="Invalid Value", message=error_text) 
        return False


if __name__ == "__main__":
    root = tk.Tk()
    store_gui = StoreGUI(root)
    root.mainloop()