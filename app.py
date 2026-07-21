import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pymysql
import pymysql.cursors

def connect_to_db():
    return pymysql.connect(
        host='127.0.0.1',
        port=8889,
        user='root',
        password='root',
        database='inventorystocks',
        cursorclass=pymysql.cursors.DictCursor
    )
def get_suppliers():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Supplier_ID, Supplier_Name FROM supplier")
    data = cursor.fetchall()
    conn.close()
    return {row['Supplier_Name']: row['Supplier_ID'] for row in data}
def get_all_supply_names():
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT Supply_ID, Supply_Name FROM molecular_supply")
            return cursor.fetchall()
    finally:
        conn.close()
def get_all_supplier_names():
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT Supplier_ID, Supplier_Name FROM supplier")
            return cursor.fetchall()
    finally:
        conn.close()


root = tk.Tk()
root.title("Molecular Biology Lab Inventory System")
root.geometry("700x500")

tab_control = ttk.Notebook(root)

# --- TAB 1: Manage Supplies --- #
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Inventory Management")

tk.Label(tab1, text="Supply Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
supply_name = tk.Entry(tab1)
supply_name.grid(row=0, column=1, padx=10)

tk.Label(tab1, text="Supply Type:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
supply_type = tk.Entry(tab1)
supply_type.grid(row=1, column=1)

tk.Label(tab1, text="Brand:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
brand = tk.Entry(tab1)
brand.grid(row=2, column=1)

tk.Label(tab1, text="Quantity Available:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
quantity = tk.Entry(tab1)
quantity.grid(row=3, column=1)

tk.Label(tab1, text="Unit:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
unit = tk.Entry(tab1)
unit.grid(row=4, column=1)

tk.Label(tab1, text="Unit Price:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
unit_price = tk.Entry(tab1)
unit_price.grid(row=5, column=1)

tk.Label(tab1, text="Expiration Date (YYYY-MM-DD):").grid(row=6, column=0, padx=10, pady=5, sticky="e")
expiration = tk.Entry(tab1)
expiration.grid(row=6, column=1)

tk.Label(tab1, text="Threshold Quantity:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
threshold = tk.Entry(tab1)
threshold.grid(row=7, column=1)

supplier_dict = get_suppliers()
supplier_names = list(supplier_dict.keys())

tk.Label(tab1, text="Select Supplier:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
supplier_combo = ttk.Combobox(tab1, values=supplier_names, state="readonly")
supplier_combo.grid(row=8, column=1)
supplier_combo.set("Select Supplier")


def add_supply():
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            selected_supplier = supplier_combo.get()
            if selected_supplier not in supplier_dict:
                messagebox.showerror("Input Error", "Please select a valid supplier.")
                return
            supplier_id = supplier_dict[selected_supplier]
            sql_supply = """
                INSERT INTO molecular_supply (
                    Supply_Type, Supply_Name, Brand, Quantity_Available, Unit,
                    Unit_Price, Expiration_Date, Threshold_Quantity, Supplier_ID
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            supply_data = (supply_type.get(),
                supply_name.get(),
                brand.get(),
                int(quantity.get()),
                unit.get(),
                float(unit_price.get()),
                expiration.get(),
                int(threshold.get()),
                supplier_id)
            cursor.execute(sql_supply, supply_data)
            supply_id =cursor.lastrowid
            sql_inventory = """
                            INSERT INTO inventory (Quantity_Available, Last_Updated, Supply_ID)
                            VALUES (%s, %s, %s)
                        """
            today = datetime.today().strftime('%Y-%m-%d')
            inventory_data = (int(quantity.get()), today, supply_id)
            cursor.execute(sql_inventory, inventory_data)
        conn.commit()
        messagebox.showinfo("Supply Added", f'{supply_name.get()} added to inventory.')
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

tk.Button(tab1, text="Add Supply", command=add_supply).grid(row=9, column=1, pady=10)

tk.Label(tab1, text="Delete Supply:").grid(row=10, column=0, padx=10, pady=5, sticky="e")
delete_supply_combo = ttk.Combobox(tab1, state="readonly")
delete_supply_combo.grid(row=10, column=1, pady=5)

def refresh_supply_combo():
    supply_data = get_all_supply_names()
    supply_names = [f"{s['Supply_ID']} - {s['Supply_Name']}" for s in supply_data]
    delete_supply_combo['values'] = supply_names
refresh_supply_combo()

def delete_supply():
    selected_supply = delete_supply_combo.get()
    if not selected_supply:
        messagebox.showwarning("Input Error", "Please select a supply to delete.")
        return
    supply_id_to_delete = selected_supply.split(" - ")[0]
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM molecular_supply WHERE Supply_ID = %s", (supply_id_to_delete,))
            supply = cursor.fetchone()
            if supply:
                cursor.execute("DELETE FROM molecular_supply WHERE Supply_ID = %s", (supply_id_to_delete,))
                conn.commit()
                messagebox.showinfo("Supply Deleted", f"The supply '{supply['Supply_Name']}' has been deleted.")
                refresh_supply_combo()  # Refresh ComboBox after deletion
            else:
                messagebox.showerror("Delete Error", "Supply not found.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()
tk.Button(tab1, text="Delete Supply", command=delete_supply).grid(row=11, column=1, pady=5)


# --- TAB 2: Manage Suppliers --- #
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text="Manage Suppliers")

tk.Label(tab2, text="Supplier Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
supplier_name = tk.Entry(tab2)
supplier_name.grid(row=0, column=1)

tk.Label(tab2, text="Contact Info:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
contact_info = tk.Entry(tab2)
contact_info.grid(row=1, column=1)

tk.Label(tab2, text="Address:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
address = tk.Entry(tab2)
address.grid(row=2, column=1)

def add_supplier():
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO supplier (Supplier_Name, Contact_information, Supplier_Address)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (
                supplier_name.get(), contact_info.get(), address.get()
            ))
        conn.commit()
        messagebox.showinfo("Supplier Added", f"Supplier {supplier_name.get()} added!")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

tk.Button(tab2, text="Add Supplier", command=add_supplier).grid(row=3, column=1, pady=10)
tk.Label(tab2, text="Delete Supplier:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
delete_supplier_combo = ttk.Combobox(tab2, state="readonly")
delete_supplier_combo.grid(row=4, column=1)

def refresh_supplier_combo():
    supplier_data = get_all_supplier_names()
    supplier_names = [f"{s['Supplier_ID']} - {s['Supplier_Name']}" for s in supplier_data]
    delete_supplier_combo['values'] = supplier_names
refresh_supplier_combo()

def delete_supplier():
    selected_supplier = delete_supplier_combo.get()
    if not selected_supplier:
        messagebox.showwarning("Input Error", "Please select a supplier to delete.")
        return
    supplier_id_to_delete = selected_supplier.split(" - ")[0]
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM supplier WHERE Supplier_ID = %s", (supplier_id_to_delete,))
            supplier = cursor.fetchone()
            if supplier:
                cursor.execute("DELETE FROM supplier WHERE Supplier_ID = %s", (supplier_id_to_delete,))
                conn.commit()
                messagebox.showinfo("Supplier Deleted", f"The supplier '{supplier['Supplier_Name']}' has been deleted.")
                refresh_supplier_combo()
            else:
                messagebox.showerror("Delete Error", "Supplier not found.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()
tk.Button(tab2, text="Delete Supplier", command=delete_supplier).grid(row=5, column=1, pady=5)


# --- TAB 3: Search Inventory --- #
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text="Search Inventory")

tk.Label(tab3, text="Search by Supply Name:").grid(row=0, column=0, padx=10, pady=5)
search_input = tk.Entry(tab3)
search_input.grid(row=0, column=1)

tk.Checkbutton(tab3, text="Only show low inventory").grid(row=1, column=1, sticky="w")

def search_inventory():
    query = search_input.get()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a supply name to search for.")
        return
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM molecular_supply 
                WHERE Supply_Name LIKE %s
            """
            cursor.execute(sql, ("%" + query + "%",))  # allows for partial matches
            results = cursor.fetchall()
            if results:
                result_text = "Search Results:\n"
                for result in results:
                    result_text += f'Name: {result["Supply_Name"]}, Type: {result["Supply_Type"]}, Quantity: {result["Quantity_Available"]}\n'
                messagebox.showinfo("Search Results", result_text)
            else:
                messagebox.showinfo("No Results", f'No supplies found for "{query}".')
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()
tk.Button(tab3, text="Search", command=search_inventory).grid(row=2, column=1, pady=10)


# --- TAB 4: Restocking Alerts --- #
tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text="Restocking Alerts")

tk.Label(tab4, text="Check Restocking Alerts").grid(row=0, column=0, padx=10, pady=5)
def simulate_alert():
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT ms.Supply_ID, ms.Supply_Name, ms.Quantity_Available, ms.Threshold_Quantity
                FROM molecular_supply ms
                WHERE ms.Quantity_Available < ms.Threshold_Quantity
            """)
            results = cursor.fetchall()
            if results:
                result_text = "Low Stock Alerts:\n"
                for result in results:
                    supply_name = result['Supply_Name']
                    quantity_available = result['Quantity_Available']
                    threshold_quantity = result['Threshold_Quantity']
                    alert_date = datetime.today().strftime('%Y-%m-%d')
                    restock_quantity = threshold_quantity - quantity_available
                    alert_status = 'Pending'
                    cursor.execute("""
                        INSERT INTO restocking_alert (Alert_Date, Quantity_Below_Threshold, Restock_Quantity, Alert_Status, Supply_ID)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (alert_date, quantity_available - threshold_quantity, restock_quantity, alert_status,
                          result['Supply_ID']))
                    result_text += f"Supply: {supply_name}, Available: {quantity_available}, Threshold: {threshold_quantity}, Restock Quantity: {restock_quantity}\n"
                conn.commit()
                messagebox.showinfo("Restocking Alerts", result_text)
            else:
                messagebox.showinfo("No Alerts", "All supplies are above their threshold quantities.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()
tk.Button(tab4, text="Check for Alerts", command=simulate_alert).grid(row=1, column=0, pady=10)

# --- Tab 5 ---
tab5 = ttk.Frame(tab_control)
tab_control.add(tab5, text="Ordering")

tk.Label(tab5, text="Select Supply:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
supply_list = []
def load_supply_options():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT Supply_ID, Supply_Name FROM molecular_supply")
        result = cursor.fetchall()
        for r in result:
            supply_list.append(f"{r['Supply_ID']} - {r['Supply_Name']}")
    conn.close()

load_supply_options()
supply_combo_order = ttk.Combobox(tab5, values=supply_list, state="readonly")
supply_combo_order.grid(row=0, column=1)

tk.Label(tab5, text="Quantity to Order:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
quantity_order = tk.Entry(tab5)
quantity_order.grid(row=1, column=1)

tk.Label(tab5, text="Unit Price:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
unit_price_entry = tk.Entry(tab5)
unit_price_entry.grid(row=2, column=1)

def place_order():
    try:
        selected = supply_combo_order.get()
        if not selected:
            messagebox.showerror("Input Error", "Please select a supply.")
            return
        supply_id = int(selected.split(" - ")[0])
        qty = int(quantity_order.get())
        price = float(unit_price_entry.get())
        total = qty * price
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT Supplier_ID FROM molecular_supply WHERE Supply_ID = %s", (supply_id,))
            supplier = cursor.fetchone()
            if not supplier:
                messagebox.showerror("Error", "Supplier not found for this supply.")
                return
            supplier_id = supplier['Supplier_ID']
            order_sql = """
                INSERT INTO ordering (Order_Date, Total_Amount, Order_Status, Supplier_ID, Supply_ID)
                VALUES (%s, %s, %s, %s, %s)
            """
            today = datetime.today().strftime('%Y-%m-%d')
            cursor.execute(order_sql, (today, total, 'Pending', supplier_id, supply_id))
            order_id = cursor.lastrowid
            order_details_sql = """
                INSERT INTO order_details (quantity_ordered, unit_price, total_cost, order_id, supplier_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(order_details_sql, (qty, price, total, order_id, supplier_id))
        conn.commit()
        messagebox.showinfo("Order Placed", f"Order #{order_id} placed successfully.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()
tk.Button(tab5, text="Place Order", command=place_order).grid(row=3, column=1, pady=10)

tk.Label(tab5, text="--- Update Existing Order ---").grid(row=4, column=0, columnspan=2, pady=(20, 5))

tk.Label(tab5, text="Select Order:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
order_list = []
order_combo = ttk.Combobox(tab5, values=order_list, state="readonly")
order_combo.grid(row=5, column=1)

tk.Label(tab5, text="New Status:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
status_combo = ttk.Combobox(tab5, values=["Pending", "Ordered", "Completed", "Cancelled"], state="readonly")
status_combo.grid(row=6, column=1)

def load_orders():
    order_list.clear()
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT Order_ID, Order_Date, Order_Status FROM ordering")
        result = cursor.fetchall()
        for row in result:
            display = f"{row['Order_ID']} - {row['Order_Date']} ({row['Order_Status']})"
            order_list.append(display)
    conn.close()
    order_combo['values'] = order_list
load_orders()


def update_order_status():
    selected = order_combo.get()
    new_status = status_combo.get()

    if not selected or not new_status:
        messagebox.showwarning("Input Error", "Please select an order and a new status.")
        return
    order_id = int(selected.split(" - ")[0])
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE ordering SET Order_Status = %s WHERE Order_ID = %s", (new_status, order_id))
        conn.commit()
        messagebox.showinfo("Order Updated", f"Order #{order_id} updated to '{new_status}'.")
        load_orders()  # Refresh the list
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()
tk.Button(tab5, text="Update Status", command=update_order_status).grid(row=7, column=1, pady=10)


# --- Display Tabs ---
tab_control.pack(expand=1, fill="both")

# --- Run the App ---
root.mainloop()
