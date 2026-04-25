#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

class BillGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Generator App")
        self.root.geometry("900x700")
        self.root.configure(bg="#ecf0f1")

        self.bills_folder = "bills"
        if not os.path.exists(self.bills_folder):
            os.makedirs(self.bills_folder)

        self.items = []
        self.store_items_file = "store_items.json"
        self.store_items = {}
        self.load_store_items()
        self.create_ui()

    def load_store_items(self):
        """Load store items from JSON file"""
        if os.path.exists(self.store_items_file):
            try:
                with open(self.store_items_file, 'r') as f:
                    self.store_items = json.load(f)
            except:
                self.store_items = {}
        else:
            self.store_items = {}

    def save_store_items(self):
        """Save store items to JSON file"""
        try:
            with open(self.store_items_file, 'w') as f:
                json.dump(self.store_items, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save items: {e}")

    def create_ui(self):
        """Create the main UI"""
        # Header
        header = tk.Label(self.root, text="BILL GENERATOR APP",
                         font=("Helvetica", 24, "bold"), bg="#ecf0f1", fg="#2c3e50")
        header.pack(pady=15)

        # Main frame
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left section - Bill Details
        left_frame = tk.Frame(main_frame, bg="#ecf0f1")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Customer Info
        tk.Label(left_frame, text="CUSTOMER DETAILS", font=("Helvetica", 12, "bold"),
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", pady=(0, 10))

        tk.Label(left_frame, text="Customer Name:", font=("Helvetica", 10), bg="#ecf0f1").pack(anchor="w")
        self.customer_name = tk.Entry(left_frame, font=("Helvetica", 11), width=40)
        self.customer_name.pack(pady=5)

        tk.Label(left_frame, text="Bill Number:", font=("Helvetica", 10), bg="#ecf0f1").pack(anchor="w", pady=(10, 0))
        self.bill_number = tk.Entry(left_frame, font=("Helvetica", 11), width=40)
        self.bill_number.pack(pady=5)
        self.bill_number.insert(0, f"B-{datetime.now().strftime('%d%m%y%H%M')}")

        # Add Item Section
        tk.Label(left_frame, text="ADD ITEMS FROM STORE", font=("Helvetica", 12, "bold"),
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", pady=(20, 10))

        tk.Label(left_frame, text="Select Item:", font=("Helvetica", 10), bg="#ecf0f1").pack(anchor="w")
        self.store_item_var = tk.StringVar()
        self.store_dropdown = tk.OptionMenu(left_frame, self.store_item_var, "-- No Items --", *self.store_items.keys())
        self.store_dropdown.config(font=("Helvetica", 11), width=37, bg="white")
        self.store_dropdown.pack(pady=5)

        tk.Label(left_frame, text="Quantity:", font=("Helvetica", 10), bg="#ecf0f1").pack(anchor="w")
        self.store_quantity = tk.Entry(left_frame, font=("Helvetica", 11), width=40)
        self.store_quantity.pack(pady=5)
        self.store_quantity.insert(0, "1")

        add_store_btn = tk.Button(left_frame, text="ADD TO BILL", command=self.add_from_store,
                                 font=("Helvetica", 11, "bold"), bg="#3498db", fg="white",
                                 width=40, height=2)
        add_store_btn.pack(pady=10)

        # Manage Store Items Section
        tk.Label(left_frame, text="MANAGE STORE ITEMS", font=("Helvetica", 12, "bold"),
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", pady=(15, 10))

        # Store items listbox with scrollbar
        list_frame = tk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.store_listbox = tk.Listbox(list_frame, font=("Helvetica", 10), height=8,
                                       yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
        self.store_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.store_listbox.yview)

        # Bind click event
        self.store_listbox.bind("<ButtonRelease-1>", self.on_store_item_click)

        # Load items into listbox
        self.update_store_listbox()

        # Buttons frame for store items
        store_btn_frame = tk.Frame(left_frame, bg="#ecf0f1")
        store_btn_frame.pack(pady=5)

        add_selected_btn = tk.Button(store_btn_frame, text="ADD TO BILL", command=self.add_selected_to_bill,
                                    font=("Helvetica", 10, "bold"), bg="#27ae60", fg="white",
                                    width=15, height=2)
        add_selected_btn.pack(side=tk.LEFT, padx=2)

        show_store_btn = tk.Button(store_btn_frame, text="REFRESH", command=self.update_store_listbox,
                                   font=("Helvetica", 10, "bold"), bg="#3498db", fg="white",
                                   width=15, height=2)
        show_store_btn.pack(side=tk.LEFT, padx=2)

        # Right section - Bill Preview
        right_frame = tk.Frame(main_frame, bg="white", relief=tk.SUNKEN, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(right_frame, text="BILL PREVIEW", font=("Helvetica", 12, "bold"),
                bg="white", fg="#2c3e50").pack(pady=10)

        # Bill text area
        self.bill_text = tk.Text(right_frame, font=("Courier", 10), height=30, width=45,
                                state=tk.DISABLED, bg="white", fg="#2c3e50")
        self.bill_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        # Delete Item Button
        del_btn = tk.Button(button_frame, text="DELETE LAST ITEM", command=self.delete_last_item,
                           font=("Helvetica", 10, "bold"), bg="#e74c3c", fg="white",
                           width=20, height=2)
        del_btn.pack(side=tk.LEFT, padx=5)

        # Show All Items Button
        show_btn = tk.Button(button_frame, text="SHOW ALL ITEMS", command=self.show_all_items,
                            font=("Helvetica", 10, "bold"), bg="#16a085", fg="white",
                            width=18, height=2)
        show_btn.pack(side=tk.LEFT, padx=5)

        # Show Store Items Button
        show_store_btn = tk.Button(button_frame, text="SHOW STORE", command=self.show_store_items,
                                  font=("Helvetica", 10, "bold"), bg="#8e44ad", fg="white",
                                  width=18, height=2)
        show_store_btn.pack(side=tk.LEFT, padx=5)

        # Clear All Button
        clear_btn = tk.Button(button_frame, text="CLEAR ALL", command=self.clear_all,
                             font=("Helvetica", 10, "bold"), bg="#f39c12", fg="white",
                             width=20, height=2)
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Save Bill Button
        save_btn = tk.Button(button_frame, text="SAVE BILL", command=self.save_bill,
                            font=("Helvetica", 10, "bold"), bg="#27ae60", fg="white",
                            width=20, height=2)
        save_btn.pack(side=tk.LEFT, padx=5)

        # Print Bill Button
        print_btn = tk.Button(button_frame, text="PRINT BILL", command=self.print_bill,
                             font=("Helvetica", 10, "bold"), bg="#9b59b6", fg="white",
                             width=20, height=2)
        print_btn.pack(side=tk.LEFT, padx=5)

    def add_to_store(self):
        """Add item to store inventory"""
        item_name = self.store_item_name.get().strip()
        try:
            price = float(self.store_item_price.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number!")
            return

        if not item_name or price <= 0:
            messagebox.showerror("Error", "Please fill all fields with valid values!")
            return

        self.store_items[item_name] = price
        self.save_store_items()

        # Clear fields
        self.store_item_name.delete(0, tk.END)
        self.store_item_price.delete(0, tk.END)

        # Update dropdown
        self.update_store_dropdown()
        messagebox.showinfo("Success", f"'{item_name}' added to store!")

    def update_store_listbox(self):
        """Update the store items listbox"""
        self.store_listbox.delete(0, tk.END)
        for item_name, price in self.store_items.items():
            self.store_listbox.insert(tk.END, f"{item_name} - ${price:.2f}")

    def on_store_item_click(self, event):
        """Handle click on store item listbox"""
        selection = self.store_listbox.curselection()
        if selection:
            self.selected_store_item = self.store_listbox.get(selection[0]).split(" - $")[0]

    def add_selected_to_bill(self):
        """Add selected item from listbox to bill"""
        selection = self.store_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please click on an item to select it!")
            return

        item_name = self.store_listbox.get(selection[0]).split(" - $")[0]

        try:
            quantity = float(self.store_quantity.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number!")
            return

        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than 0!")
            return

        price = self.store_items[item_name]
        item_total = quantity * price

        self.items.append({
            "name": item_name,
            "quantity": quantity,
            "price": price,
            "total": item_total
        })

        self.update_bill_preview()
        messagebox.showinfo("Success", f"'{item_name}' added to bill!")

    def add_from_store(self):
        """Add item from store to bill"""
        item_name = self.store_item_var.get().strip()

        if not item_name or item_name == "-- No Items --":
            messagebox.showerror("Error", "Please select an item from store!")
            return

        try:
            quantity = float(self.store_quantity.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number!")
            return

        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than 0!")
            return

        price = self.store_items[item_name]
        item_total = quantity * price

        self.items.append({
            "name": item_name,
            "quantity": quantity,
            "price": price,
            "total": item_total
        })

        # Clear fields
        self.store_quantity.delete(0, tk.END)
        self.store_quantity.insert(0, "1")
        self.store_item_var.set("-- No Items --")

        self.update_bill_preview()
        messagebox.showinfo("Success", "Item added to bill!")

    def add_item(self):
        """Add item to the bill (manual entry)"""
        # This is now handled by add_from_store, keeping for backwards compatibility
        pass

    def delete_last_item(self):
        """Delete the last item from the bill"""
        if not self.items:
            messagebox.showwarning("Warning", "No items to delete!")
            return

        self.items.pop()
        self.update_bill_preview()
        messagebox.showinfo("Success", "Last item deleted!")

    def show_all_items(self):
        """Show all items in a formatted list"""
        if not self.items:
            messagebox.showwarning("Warning", "No items added yet!")
            return

        items_list = "=" * 60 + "\n"
        items_list += "           ALL ITEMS IN BILL\n"
        items_list += "=" * 60 + "\n\n"

        items_list += f"{'No':<4} {'Item Name':<25} {'Qty':>8} {'Price':>10} {'Total':>10}\n"
        items_list += "-" * 60 + "\n"

        total_amount = 0
        for idx, item in enumerate(self.items, 1):
            items_list += f"{idx:<4} {item['name']:<25} {item['quantity']:>8.1f} {item['price']:>10.2f} {item['total']:>10.2f}\n"
            total_amount += item['total']

        items_list += "-" * 60 + "\n"
        items_list += f"{'TOTAL ITEMS':<30} {' ':>8} {' ':>10} {total_amount:>10.2f}\n"
        items_list += "=" * 60 + "\n"

        messagebox.showinfo("All Items", items_list)

    def show_store_items(self):
        """Show all store items in inventory"""
        if not self.store_items:
            messagebox.showwarning("Warning", "No items in store inventory!")
            return

        store_list = "=" * 50 + "\n"
        store_list += "       STORE INVENTORY\n"
        store_list += "=" * 50 + "\n\n"

        store_list += f"{'No':<4} {'Item Name':<30} {'Price':>10}\n"
        store_list += "-" * 50 + "\n"

        for idx, (item_name, price) in enumerate(self.store_items.items(), 1):
            store_list += f"{idx:<4} {item_name:<30} {price:>10.2f}\n"

        store_list += "=" * 50 + "\n"
        store_list += f"Total Items in Store: {len(self.store_items)}\n"
        store_list += "=" * 50 + "\n"

        messagebox.showinfo("Store Inventory", store_list)

    def clear_all(self):
        """Clear all items and reset form"""
        if not self.items:
            messagebox.showwarning("Warning", "Bill is already empty!")
            return

        if messagebox.askyesno("Confirm", "Clear all items?"):
            self.items = []
            self.customer_name.delete(0, tk.END)
            self.bill_number.delete(0, tk.END)
            self.bill_number.insert(0, f"B-{datetime.now().strftime('%d%m%y%H%M')}")
            self.store_quantity.delete(0, tk.END)
            self.store_quantity.insert(0, "1")
            self.store_item_var.set("-- No Items --")
            self.store_item_name.delete(0, tk.END)
            self.store_item_price.delete(0, tk.END)
            self.update_bill_preview()

    def generate_bill_text(self):
        """Generate the bill text"""
        bill = ""
        bill += "=" * 65 + "\n"
        bill += "                      INVOICE BILL\n"
        bill += "=" * 65 + "\n\n"

        bill += f"Bill Number: {self.bill_number.get()}\n"
        bill += f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        bill += f"Customer: {self.customer_name.get() or 'N/A'}\n"
        bill += "\n" + "-" * 65 + "\n"

        bill += f"{'No':<4} {'Item Name':<25} {'Qty':>8} {'Price':>10} {'Total':>10}\n"
        bill += "-" * 65 + "\n"

        subtotal = 0
        for idx, item in enumerate(self.items, 1):
            bill += f"{idx:<4} {item['name']:<25} {item['quantity']:>8.1f} {item['price']:>10.2f} {item['total']:>10.2f}\n"
            subtotal += item['total']

        bill += "=" * 65 + "\n"
        bill += f"{'TOTAL':<4} {' ':<25} {' ':>8} {' ':>10} {subtotal:>10.2f}\n"
        bill += "=" * 65 + "\n"

        bill += "\n              Thank You for Your Business!\n"
        bill += "=" * 65 + "\n"

        return bill, subtotal

    def update_bill_preview(self):
        """Update the bill preview in the text box"""
        if not self.items:
            self.bill_text.config(state=tk.NORMAL)
            self.bill_text.delete(1.0, tk.END)
            self.bill_text.insert(1.0, "Add items to generate bill...")
            self.bill_text.config(state=tk.DISABLED)
            return

        bill_text, subtotal = self.generate_bill_text()

        self.bill_text.config(state=tk.NORMAL)
        self.bill_text.delete(1.0, tk.END)
        self.bill_text.insert(1.0, bill_text)
        self.bill_text.config(state=tk.DISABLED)

    def save_bill(self):
        """Save bill to a text file"""
        if not self.items:
            messagebox.showerror("Error", "No items in bill!")
            return

        bill_text, subtotal = self.generate_bill_text()

        bill_number = self.bill_number.get()
        filename = os.path.join(self.bills_folder, f"{bill_number}.txt")

        try:
            with open(filename, 'w') as f:
                f.write(bill_text)
            messagebox.showinfo("Success", f"Bill saved as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save bill: {e}")

    def print_bill(self):
        """Print bill (display in message box)"""
        if not self.items:
            messagebox.showerror("Error", "No items in bill!")
            return

        bill_text, subtotal = self.generate_bill_text()
        messagebox.showinfo("Bill Preview", bill_text)


def main():
    root = tk.Tk()
    app = BillGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
