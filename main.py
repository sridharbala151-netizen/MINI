#!/usr/bin/env python3
"""
Bill Generator App - Kivy Mobile Version
Can be converted to APK using Buildozer
"""
import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Set window size for desktop testing (mobile will auto-resize)
Window.size = (400, 700)


class BillItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.total = quantity * price


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
        self.load_store_items()
        self.build_ui()

    def load_store_items(self):
        """Load store items from JSON file"""
        self.store_items = {}
        if os.path.exists("store_items.json"):
            try:
                with open("store_items.json", 'r') as f:
                    self.store_items = json.load(f)
            except:
                self.store_items = {}
        else:
            self.store_items = {}

    def build_ui(self):
        """Build the main UI"""
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header
        header = BoxLayout(size_hint_y=None, height=50)
        header.add_widget(Label(
            text='[b]BILL GENERATOR[/b]',
            markup=True,
            font_size='20sp',
            halign='center',
            valign='middle',
            color=get_color_from_hex('#2c3e50')
        ))

        # Customer Name
        customer_layout = BoxLayout(size_hint_y=None, height=40, padding=5)
        customer_layout.add_widget(Label(text='Customer:', font_size='14sp', size_hint_x=0.3))
        self.customer_input = TextInput(hint_text='Customer Name', multiline=False, font_size='14sp')
        customer_layout.add_widget(self.customer_input)

        # Product List (Scrollable)
        list_label = Label(text='[b]TAP PRODUCT TO ADD[/b]', markup=True, font_size='14sp',
                          size_hint_y=None, height=30, color=get_color_from_hex('#3498db'))

        self.product_list = GridLayout(cols=2, size_hint_y=None, spacing=5, padding=5)
        self.product_list.bind(minimum_height=self.product_list.setter('height'))
        self.refresh_product_list()

        scroll_view = ScrollView(size_hint_y=0.5, do_scroll_y=True)
        scroll_view.add_widget(self.product_list)

        # Quantity Input
        qty_layout = BoxLayout(size_hint_y=None, height=40, padding=5)
        qty_layout.add_widget(Label(text='Qty:', font_size='14sp', size_hint_x=0.3))
        self.qty_input = TextInput(text='1', hint_text='Quantity', multiline=False,
                                   font_size='14sp', input_filter='float')
        qty_layout.add_widget(self.qty_input)

        add_btn = Button(text='[b]+ ADD TO BILL[/b]', markup=True, size_hint_y=None, height=50,
                        background_color=get_color_from_hex('#27ae60'), font_size='16sp')
        add_btn.bind(on_press=self.add_to_bill)
        self.add_btn_ref = add_btn

        # Bill Preview Section
        bill_label = Label(text='[b]BILL PREVIEW[/b]', markup=True, font_size='14sp',
                          size_hint_y=None, height=30, color=get_color_from_hex('#3498db'))

        self.bill_preview = GridLayout(cols=4, size_hint_y=None, height=40, padding=5)
        self.bill_preview.add_widget(Label(text='Item', font_size='12sp'))
        self.bill_preview.add_widget(Label(text='Qty', font_size='12sp'))
        self.bill_preview.add_widget(Label(text='Price', font_size='12sp'))
        self.bill_preview.add_widget(Label(text='Total', font_size='12sp'))

        self.bill_items_container = GridLayout(cols=4, size_hint_y=None, padding=5)
        self.bill_items_container.bind(minimum_height=self.bill_items_container.setter('height'))

        bill_scroll = ScrollView(size_hint_y=0.25, do_scroll_y=True)
        bill_scroll.add_widget(self.bill_items_container)

        # Total Label
        self.total_label = Label(text='Total: 0.00', font_size='18sp', size_hint_y=None,
                                height=40, color=get_color_from_hex('#27ae60'))

        # Action Buttons
        btn_layout = GridLayout(cols=3, size_hint_y=None, height=50, spacing=5)
        save_btn = Button(text='SAVE', background_color=get_color_from_hex('#27ae60'), font_size='14sp')
        save_btn.bind(on_press=self.save_bill)
        btn_layout.add_widget(save_btn)

        clear_btn = Button(text='CLEAR', background_color=get_color_from_hex('#e74c3c'), font_size='14sp')
        clear_btn.bind(on_press=self.clear_bill)
        btn_layout.add_widget(clear_btn)

        show_btn = Button(text='SHOW ALL', background_color=get_color_from_hex('#3498db'), font_size='14sp')
        show_btn.bind(on_press=self.show_all_items)
        btn_layout.add_widget(show_btn)

        # Add all widgets
        layout.add_widget(header)
        layout.add_widget(customer_layout)
        layout.add_widget(list_label)
        layout.add_widget(scroll_view)
        layout.add_widget(qty_layout)
        layout.add_widget(add_btn)
        layout.add_widget(bill_label)
        layout.add_widget(self.bill_preview)
        layout.add_widget(bill_scroll)
        layout.add_widget(self.total_label)
        layout.add_widget(btn_layout)

        self.add_widget(layout)

    def refresh_product_list(self):
        """Refresh the product list"""
        self.product_list.clear_widgets()
        for item_name, price in sorted(self.store_items.items()):
            btn = Button(
                text=f'{item_name}\n{price:.2f}',
                font_size='12sp',
                size_hint_y=None,
                height=60,
                background_color=get_color_from_hex('#3498db'),
                on_press=lambda x, name=item_name, p=price: self.select_product(name, p)
            )
            self.product_list.add_widget(btn)

    def select_product(self, name, price):
        """Handle product selection"""
        self.selected_product = name
        self.selected_price = price

        # Highlight selected button (visual feedback)
        for child in self.product_list.children:
            if child.text.startswith(name):
                child.background_color = get_color_from_hex('#27ae60')
            else:
                child.background_color = get_color_from_hex('#3498db')

    def add_to_bill(self, instance):
        """Add selected product to bill"""
        if not hasattr(self, 'selected_product'):
            self.show_popup('Error', 'Please tap a product first!')
            return

        try:
            qty = float(self.qty_input.text)
            if qty <= 0:
                self.show_popup('Error', 'Quantity must be greater than 0!')
                return
        except ValueError:
            self.show_popup('Error', 'Invalid quantity!')
            return

        item = BillItem(self.selected_product, qty, self.selected_price)
        self.items.append(item)
        self.refresh_bill_preview()
        self.qty_input.text = '1'

        # Reset button colors
        for child in self.product_list.children:
            child.background_color = get_color_from_hex('#3498db')

        self.show_popup('Success', f'{self.selected_product} added to bill!')

    def refresh_bill_preview(self):
        """Refresh the bill preview"""
        self.bill_items_container.clear_widgets()
        total = 0
        for item in self.items:
            self.bill_items_container.add_widget(Label(text=item.name[:10], font_size='10sp', size_hint_x=0.3))
            self.bill_items_container.add_widget(Label(text=str(item.quantity), font_size='10sp', size_hint_x=0.2))
            self.bill_items_container.add_widget(Label(text=f'{item.price:.2f}', font_size='10sp', size_hint_x=0.25))
            self.bill_items_container.add_widget(Label(text=f'{item.total:.2f}', font_size='10sp', size_hint_x=0.25))
            total += item.total
        self.total_label.text = f'Total: {total:.2f}'

    def clear_bill(self, instance):
        """Clear all items from bill"""
        if not self.items:
            self.show_popup('Warning', 'Bill is already empty!')
            return
        self.items = []
        self.refresh_bill_preview()
        self.customer_input.text = ''
        self.show_popup('Success', 'Bill cleared!')

    def save_bill(self, instance):
        """Save bill to file"""
        if not self.items:
            self.show_popup('Error', 'No items in bill!')
            return

        bill_number = f"B-{datetime.now().strftime('%d%m%y%H%M')}"
        customer = self.customer_input.text or 'N/A'

        # Create bills directory
        if not os.path.exists('bills'):
            os.makedirs('bills')

        # Generate bill text
        bill_text = "=" * 50 + "\n"
        bill_text += "         INVOICE BILL\n"
        bill_text += "=" * 50 + "\n\n"
        bill_text += f"Bill Number: {bill_number}\n"
        bill_text += f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
        bill_text += f"Customer: {customer}\n\n"
        bill_text += "-" * 50 + "\n"
        bill_text += f"{'No':<4} {'Item':<15} {'Qty':>5} {'Price':>8} {'Total':>8}\n"
        bill_text += "-" * 50 + "\n"

        total = 0
        for idx, item in enumerate(self.items, 1):
            bill_text += f"{idx:<4} {item.name:<15} {item.quantity:>5.1f} {item.price:>6.2f} {item.total:>6.2f}\n"
            total += item.total

        bill_text += "=" * 50 + "\n"
        bill_text += f"{'TOTAL':>36} {total:.2f}\n"
        bill_text += "=" * 50 + "\n"
        bill_text += "\n     Thank You for Your Business!\n"
        bill_text += "=" * 50 + "\n"

        # Save to file
        filename = f'bills/{bill_number}.txt'
        with open(filename, 'w') as f:
            f.write(bill_text)

        self.show_popup('Success', f'Bill saved!\n{filename}')

    def show_all_items(self, instance):
        """Show all items in bill"""
        if not self.items:
            self.show_popup('Warning', 'No items in bill!')
            return

        msg = "ITEMS IN BILL\n" + "-" * 30 + "\n"
        total = 0
        for idx, item in enumerate(self.items, 1):
            msg += f"{idx}. {item.name} x{self.qty_input.text} = {item.total:.2f}\n"
            total += item.total
        msg += "-" * 30 + f"\nTOTAL: {total:.2f}"

        self.show_popup('All Items', msg)

    def show_popup(self, title, message):
        """Show a popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message, font_size='14sp'),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class BillGeneratorApp(App):
    def build(self):
        """Build the app"""
        return MainScreen()


if __name__ == '__main__':
    BillGeneratorApp().run()
