from tkinter import *
from tkinter import ttk, Tk , Label, Entry, ttk 
import time
import sqlite3
import random
import tempfile
import win32api
import win32print
import tkinter as tk
from PIL import Image, ImageTk

f=''
flag=''
flags=''


login=sqlite3.connect("admin.db")
l=login.cursor()

c=sqlite3.connect("medicine.db")
cur=c.cursor()

columns=('Sl No', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')


def open_win():
    global apt, flag
    flag = 'apt'
    apt = tk.Tk()
    apt.title("Health Haven Pharmacy")
    apt.configure(bg="#f0f0f0")
    apt.geometry('1000x600')

    # Load and resize the background image using Pillow
    image_path = r"X:\New folder\Pharmacy Software u\background 1.jpg"  # Correct path to your JPEG file
    original_image = Image.open(image_path)
    resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize to match the window size
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = tk.Label(apt, image=background_image)  # Ensure the label uses the resized image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image  # Keep a reference to avoid garbage collection

    # Define style for buttons
    style = ttk.Style()
    style.configure('TButton', padding=5, relief="raised", font=('Arial', 10))

    title_label = Label(apt, text="Health Haven Pharmacy", font=("Arial", 18, "bold"), bg="#f0f0f0")
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    separator_top = Frame(apt, height=2, bd=1, relief=SUNKEN, bg="black")
    separator_top.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)


    # Stock Maintenance Frame
    stock_frame = LabelFrame(apt, text="Stock Maintenance", padx=10, pady=10, bg="#f0f0f0")
    stock_frame.grid(row=2, column=0, padx=10, pady=10)
    ttk.Button(stock_frame, text="Add product to Stock", width=25, command=stock).grid(row=0, column=0, pady=5)
    ttk.Button(stock_frame, text="Delete product from Stock", width=25, command=delete_stock).grid(row=1, column=0, pady=5)

    # Access Database Frame
    access_db_frame = LabelFrame(apt, text="Access Database", padx=10, pady=10, bg="#f0f0f0")
    access_db_frame.grid(row=2, column=1, padx=10, pady=10)
    ttk.Button(access_db_frame, text="Modify", width=15, command=modify).grid(row=0, column=0, pady=5)
    ttk.Button(access_db_frame, text="Search", width=15, command=search).grid(row=1, column=0, pady=5)
    ttk.Button(access_db_frame, text="Check Expiry", width=15, command=exp_date).grid(row=2, column=0, pady=5)

    # Handle Cash Flows Frame
    cash_flows_frame = LabelFrame(apt, text="Handle Cash Flows", padx=10, pady=10, bg="#f0f0f0")
    cash_flows_frame.grid(row=2, column=2, padx=10, pady=10)
    ttk.Button(cash_flows_frame, text="Revenue Record", width=20, command=show_rev).grid(row=1, column=0, pady=5)
    ttk.Button(cash_flows_frame, text="Generate Bill", width=20, command=billing).grid(row=0, column=0, pady=5)

    separator_bottom = Frame(apt, height=2, bd=1, relief=SUNKEN, bg="black")
    separator_bottom.grid(row=3, column=0, columnspan=3, sticky="ew", pady=5)

    # Logout Button
    ttk.Button(apt, text="Logout", command=again).grid(row=4, column=2, pady=10)

    apt.mainloop()

def again():
    global apt
    apt.destroy()
    open_win()



def delete_stock():
    global cur, c, flag, lb1, d
    apt.destroy()
    flag = 'd'
    d = Tk()
    d.title("Delete a product from Stock")
    d.configure(bg="#f0f0f0")
    d.geometry('1000x600')
    # -------------------------background-------------------------
    # Load the background image using Pillow
    image_path = r"X:\New folder\Pharmacy Software u\background 1.jpg"  # Correct path to your JPEG file
    
    original_image = Image.open(image_path)
    resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize to match the window size, using updated resampling method
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = tk.Label(image=background_image)  # Ensure the label uses the resized image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image  

    # ----------------------------------------------------------------------------

    # Styling for buttons
    style = ttk.Style()
    style.configure('TButton', padding=5, relief="raised", font=('Arial', 10))

    Label(d, text='Enter Product to delete:').grid(row=0, column=0)
    Label(d, text='', width=30, bg='white').grid(row=0, column=1)
    Label(d, text='Product').grid(row=2, column=0)
    Label(d, text='Qty.  Exp.dt.     Cost                           ').grid(row=2, column=1)
    ren()

    list_box = Listbox(d, width=40)

    list_box.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    # Delete and Main Menu buttons with styled ttk buttons
    ttk.Button(d, width=20, text='Delete', command=delt).grid(row=0, column=3, padx=5, pady=5)
    ttk.Button(d, width=20, text='Main Menu', command=main_menu).grid(row=5, column=3, padx=5, pady=5)

    d.mainloop()

    # b=Button(d,width=20,text='Delete',command=delt).grid(row=0,column=3)
    # b=Button(d,width=20,text='Main Menu',command=main_menu).grid(row=5,column=3) 
    


def ren():
    global lb1, d, cur, c
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
    def onmousewheel(event):
        lb1.yview('scroll', event.delta, 'units')
        lb2.yview('scroll', event.delta, 'units')
        return 'break'

    d.configure(bg="#f0f0f0")
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(d, width=25, yscrollcommand=vsb.set)
    lb2 = Listbox(d, width=30, yscrollcommand=vsb.set)
    vsb.grid(row=3, column=2, sticky=N+S)
    lb1.grid(row=3, column=0)
    lb2.grid(row=3, column=1)
    lb1.bind('<MouseWheel>', onmousewheel)
    lb2.bind('<MouseWheel>', onmousewheel)
    cur.execute("SELECT * FROM med")
    for i in cur:
        s1 = [str(i[0]), str(i[1])]
        s2 = [str(i[3]), str(i[6]), str(i[4])]
        lb1.insert(END, '. '.join(s1))
        lb2.insert(END, '   '.join(s2))
    c.commit()
    lb1.bind('<<ListboxSelect>>', sel_del)

def sel_del(e):
    global lb1, d, cur, c, p, sl2
    p = lb1.curselection()
    x = 0
    sl2 = ''
    cur.execute("SELECT * FROM med")
    for i in cur:
        if x == int(p[0]):
            sl2 = i[0]
            break
        x += 1
    c.commit()
    Label(d, text=' ', bg='white', width=20).grid(row=0, column=1)
    cur.execute('SELECT * FROM med')
    for i in cur:
        if i[0] == sl2:
            Label(d, text=i[0] + '. ' + i[1], bg='white').grid(row=0, column=1)
    c.commit()

def delt():
    global p, c, cur, d
    cur.execute("DELETE FROM med WHERE sl_no=?", (sl2,))
    c.commit()
    ren()  # Re-populate list after deletion

# Sample placeholder functions to demonstrate the structure
def main():
    global cur, c
    c = None  
    cur = c.cursor()  
    ren()  




def modify(): # For modification---------MODIFY
    global cur, c, accept, flag, att, up, n, name_, apt, st, col, col_n
    col = ('', '', 'type', 'qty_left', 'cost', 'purpose', 'expdt', 'loc', 'mfg')
    col_n = ('', '', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')
    flag = 'st'
    name_ = ''
    apt.destroy()
    n = []
    cur.execute("SELECT * FROM med")
    for i in cur:
        n.append(i[1])
    c.commit()
    st = Tk()
    st.title('MODIFY')
    st.configure(bg="#f0f0f0")
    st.geometry('1000x600')
    # -------------------------background-------------------------
    # Load the background image using Pillow
    image_path = r"X:\New folder\Pharmacy Software u\background 1.jpg"  # Correct path to your JPEG file
    original_image = Image.open(image_path)
    resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize to match the window size, using updated resampling method
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = tk.Label(image=background_image)  # Ensure the label uses the resized image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image  

    # ----------------------------------------------------------------------------

    # Define style for buttons
    style = ttk.Style()
    style.configure('TButton', padding=5, relief="raised", font=('Arial', 10))

    def onvsb(*args):
        name_.yview(*args)

    def onmousewheel(event):
        name_.yview('scroll', event.delta, 'units')
        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    vsb.grid(row=1, column=3, sticky=N+S)
    name_ = Listbox(st, width=43, yscrollcommand=vsb.set, bg="#ffffff", fg="#000000", font=("Arial", 10))
    cur.execute("SELECT * FROM med")
    for i in cur:
        cx += 1
        name_.insert(cx, (str(i[0]) + '.  ' + str(i[1])))
        name_.grid(row=1, column=1, columnspan=2)
    c.commit()
    name_.bind('<MouseWheel>', onmousewheel)
    name_.bind('<<ListboxSelect>>', sel_mn)

    def on_enter(e):
        e.widget.config(bg="#0077cc", fg="#ffffff")

    def on_leave(e):
        e.widget.config(bg="#008CBA", fg="#ffffff")

    Label(st, text='Enter Medicine Name: ', bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0)
    Label(st, text='Enter changed Value of: ', bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0)
    att = Spinbox(st, values=col_n, bg="#ffffff", fg="#000000", font=("Arial", 10))
    att.grid(row=2, column=1)
    up = Entry(st, bg="#ffffff", fg="#000000", font=("Arial", 10))
    up.grid(row=2, column=2)
    
    submit_button = ttk.Button(st, width=10, text='Submit', command=save_mod)
    submit_button.grid(row=2, column=4)
    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)
    
    reset_button = ttk.Button(st, width=10, text='Reset', command=res)
    reset_button.grid(row=2, column=5)
    reset_button.bind("<Enter>", on_enter)
    reset_button.bind("<Leave>", on_leave)

    show_button = ttk.Button(st, width=10, text='Show data', command=show_val)
    show_button.grid(row=1, column=4)
    show_button.bind("<Enter>", on_enter)
    show_button.bind("<Leave>", on_leave)

    Label(st, text='-' * 120, bg="#f0f0f0").grid(row=3, column=0, columnspan=6)

    main_menu_button = ttk.Button(st, width=10, text='Main Menu', command=main_menu)
    main_menu_button.grid(row=5, column=5)
    main_menu_button.bind("<Enter>", on_enter)
    main_menu_button.bind("<Leave>", on_leave)

    st.mainloop()

def res():
    global st, up,i
    up=Entry(st)
    up.grid(row=2, column=2)
    Label(st,width=20, text='                         ').grid(row=5,column=i)

def sel_mn(e):
    global n,name_, name_mn, sl, c, cur
    name_mn=''
    p=name_.curselection()
    print (p)
    x=0
    sl=''
    cur.execute("select * from med")
    for i in cur:
        print (x, p[0])
        if x==int(p[0]):
            sl=i[0]
            break
        x+=1
    c.commit()
    print (sl)
    name_nm=n[int(sl)]
    print (name_nm)
    
def show_val():
    global st, name_mn, att, cur, c, col, col_n, sl
    for i in range(3):
        Label(st,width=20, text='                         ').grid(row=5,column=i)
    cur.execute("select * from med")
    for i in cur:
        for j in range(9):
            if att.get()==col_n[j] and sl==i[0]:
                Label(st, text=str(i[0])).grid(row=5,column=0)
                Label(st, text=str(i[1])).grid(row=5,column=1)
                Label(st, text=str(i[j])).grid(row=5,column=2)
    c.commit()

def save_mod(): #save modified data
    global cur, c, att, name_mn, st, up, col_n, sl
    for i in range(9):
        if att.get()==col_n[i]:
            a=col[i]
    sql="update med set '%s' = '%s' where sl_no = '%s'" % (a,up.get(),sl)
    cur.execute(sql)
    c.commit()
    Label(st, text='Updated!').grid(row=5,column=4)
    

def submit():
    global accept, data_records

    # Get the product name from the entry field
    product_name = accept[1].get()  # Assuming product name is entered in the first entry field

    if product_name in data_records:
        # Product name already exists
        print(f"Product name '{product_name}' already exists. Please enter a unique name.")
    else:
        # Assuming accept[2], accept[3], etc., correspond to other data fields (modify as needed)
        # Gather other product data
        product_data = [accept[i].get() for i in range(2, len(accept))]

        # Add data to the records
        data_records[product_name] = product_data

        # Optional: Print added data for demonstration
        print("Added data:", product_name, product_data)

        # Optionally, clear the entry fields after successful submission
        for entry in accept[1:]:
            entry.delete(0, 'end')  # Clear the text in each Entry field

# ------------------------Factory Pattern---------------------
class ButtonFactory:
    def create_button(self, button_type, master, text, command, row, column):
        button = ttk.Button(master, text=text, command=command)
        button.grid(row=row, column=column)
        # Set hover effects using bindings
        button.bind("<Enter>", lambda e, b=button: b.config(bg="#0077cc", fg="#ffffff"))
        button.bind("<Leave>", lambda e, b=button: b.config(bg="#008CBA", fg="#ffffff"))
        return button

def stock():       # add to stock window----------------ADD TO STOCK
    global accept, cur, c, columns, accept, flag, sto, apt
    apt.destroy()
    flag = 'sto'
    accept = [''] * 10
    sto = Tk()
    sto.title('STOCK ENTRY')
    sto.configure(bg="#f0f0f0")
    sto.geometry('1000x600')

    # -------------------------background-------------------------
    # Load the background image using Pillow
    image_path = r"X:\New folder\Pharmacy Software u\background 1.jpg"  # Correct path to your JPEG file
    original_image = Image.open(image_path)
    resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize to match the window size, using updated resampling method
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = tk.Label(image=background_image)  # Ensure the label uses the resized image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image  

    # ----------------------------------------------------------------------------

    Label(sto, text='ENTER NEW PRODUCT DATA TO THE STOCK', bg="#f0f0f0", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)
    Label(sto, text='-' * 50, bg="#f0f0f0").grid(row=1, column=0, columnspan=2)

    for i in range(1, len(columns)):
        Label(sto, width=15, text=' ' * (14 - len(str(columns[i]))) + str(columns[i]) + ':', bg="#f0f0f0").grid(row=i + 2, column=0)
        accept[i] = Entry(sto, bg="#ffffff", fg="#000000", font=("Arial", 10))
        accept[i].grid(row=i + 2, column=1)

    # Using factory to create buttons
    button_factory = ButtonFactory()
    submit_button = button_factory.create_button('submit', sto, 'Submit', submit, 12, 1)
    reset_button = button_factory.create_button('reset', sto, 'Reset', reset, 12, 0)
    refresh_button = button_factory.create_button('refresh', sto, 'Refresh stock', ref, 12, 4)
    main_menu_button = button_factory.create_button('main_menu', sto, 'Main Menu', main_menu, 12, 5)

    Label(sto, text='-' * 165, bg="#f0f0f0").grid(row=13, column=0, columnspan=7)

    for i in range(1, 6):
        Label(sto, text=columns[i], bg="#f0f0f0").grid(row=14, column=i - 1)
    Label(sto, text='Exp           Rack   Manufacturer                      ', bg="#f0f0f0").grid(row=14, column=5)

    ref()
    sto.mainloop()




def ref(): # creates a multi-listbox manually to show the whole database 
    global sto, c, cur
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)

    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        lb3.ywiew=('scroll',event.delta,'units')
        lb4.ywiew=('scroll',event.delta,'units')
        lb5.ywiew=('scroll',event.delta,'units')
        lb6.ywiew=('scroll',event.delta,'units')
        
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(sto,yscrollcommand=vsb.set)
    lb2=Listbox(sto,yscrollcommand=vsb.set)
    lb3=Listbox(sto,yscrollcommand=vsb.set,width=10)
    lb4=Listbox(sto,yscrollcommand=vsb.set,width=7)
    lb5=Listbox(sto,yscrollcommand=vsb.set,width=25)
    lb6=Listbox(sto,yscrollcommand=vsb.set,width=37)
    vsb.grid(row=15,column=6,sticky=N+S)
    lb1.grid(row=15,column=0)
    lb2.grid(row=15,column=1)
    lb3.grid(row=15,column=2)
    lb4.grid(row=15,column=3)
    lb5.grid(row=15,column=4)
    lb6.grid(row=15,column=5)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    lb3.bind('<MouseWheel>',onmousewheel)
    lb4.bind('<MouseWheel>',onmousewheel)
    lb5.bind('<MouseWheel>',onmousewheel)
    lb6.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        seq=(str(i[0]),str(i[1]))
        lb1.insert(cx,'. '.join(seq))
        lb2.insert(cx,i[2])
        lb3.insert(cx,i[3])
        lb4.insert(cx,i[4])
        lb5.insert(cx,i[5])
        lb6.insert(cx,i[6]+'    '+i[7]+'    '+i[8])
    c.commit()

def reset():
    global sto, accept
    for i in range(1,len(columns)):
        Label(sto,width=15,text=' '*(14-len(str(columns[i])))+str(columns[i])+':').grid(row=i+2,column=0)
        accept[i]=Entry(sto)
        accept[i].grid(row=i+2, column=1)
    
def submit(): #for new stock submission
    global accept, c, cur, columns, sto
    prev = time.perf_counter()
    x=['']*10
    cur.execute("select * from med")
    for i in cur:
        y=int(i[0])
    for i in range(1,9):
        x[i]=accept[i].get()
    cur.execute("select * from med WHERE name = '%s'" % (x[1]))
    if cur.fetchone():
        top = Tk()
        label = Label(top, width=40, height=10 , bg="#db3972", text="Error: Medicine name already exists.")
        label.pack()
        top.mainloop()
        return  

    sql="insert into med values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (y+1,x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8])
    cur.execute(sql)
    cur.execute("select * from med")
    c.commit()
    now = time.perf_counter()
    print (now-prev)
    top=Tk()
    Label(top,width=20, text='Success!').pack()
    top.mainloop()
    main_menu()

def chk(): #checks if the medicine is already present so that can be modified
    global cur, c, accept, sto
    cur.execute("select * from med")
    for i in cur:
        if accept[6].get()==i[6] and i[1]==accept[1].get():
            sql="update med set qty_left = '%s' where name = '%s'" % (str(int(i[3])+int(accept[3].get())),accept[1].get())
            cur.execute(sql)
            c.commit()
            top=Tk()
            Label(top,width=20, text='Modified!').pack()
            top.mainloop()
            main_menu()
        else:
            submit()
    c.commit()
    


def exp_date(): # expiry window open-----------EXPIRY
    global exp, s, c, cur, flag, apt, flags
    apt.destroy()
    flag = 'exp'
    from datetime import date
    now = time.localtime()
    n = []
    cur.execute("select * from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    
    
    exp = Tk()
    exp.title('EXPIRY CHECK')
    exp.configure(bg="#f0f0f0")
    exp.geometry('1000x600')
    # -------------------------background-------------------------
    # Load the background image using Pillow
    image_path = r"X:\New folder\Pharmacy Software u\background 1.jpg"  # Correct path to your JPEG file
    original_image = Image.open(image_path)
    resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize to match the window size, using updated resampling method
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = tk.Label(image=background_image)  # Ensure the label uses the resized image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image  

    # ----------------------------------------------------------------------------

    Label(exp, text='Today : ' + str(now[2]) + '/' + str(now[1]) + '/' + str(now[0]), bg="#f0f0f0").grid(row=0, column=0, columnspan=3)
    Label(exp, text='Selling Expired Medicines and Drugs is Illegal', bg="#f0f0f0").grid(row=1, column=0, columnspan=3)
    Label(exp, text='-' * 80, bg="#f0f0f0").grid(row=2, column=0, columnspan=3)
    
    s = Spinbox(exp, values=n)
    s.grid(row=3, column=0)
    
    check_expiry_button = ttk.Button(exp, text='Check Expiry date', command=s_exp)
    check_expiry_button.grid(row=3, column=1)
    check_expiry_button.bind("<Enter>", lambda e: check_expiry_button.config(style='TButton', cursor='hand2'))
    check_expiry_button.bind("<Leave>", lambda e: check_expiry_button.config(style='TButton'))
    
    Label(exp, text='-' * 80, bg="#f0f0f0").grid(row=4, column=0, columnspan=3)
    
    if flags == 'apt1':
        main_menu_button = ttk.Button(exp, text='Main Menu', command=main_cus)
    else:
        main_menu_button = ttk.Button(exp, text='Main Menu', command=main_menu)
    main_menu_button.grid(row=5, column=2)
    main_menu_button.bind("<Enter>", lambda e: main_menu_button.config(style='TButton', cursor='hand2'))
    main_menu_button.bind("<Leave>", lambda e: main_menu_button.config(style='TButton'))
    
    if flags != 'apt1':
        check_products_button = ttk.Button(exp, width=20, text='Check Products expiring', command=exp_dt)
        check_products_button.grid(row=5, column=0)
        check_products_button.bind("<Enter>", lambda e: check_products_button.config(style='TButton', cursor='hand2'))
        check_products_button.bind("<Leave>", lambda e: check_products_button.config(style='TButton'))

    exp.mainloop()

def s_exp():    # shows the expiry date of the medicine entered
    global c, cur, s, exp, top
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    cur.execute("select * from med")
    for i in cur:
        if(i[1]==s.get()):
            q=i[6]
            d2=date(int('20'+q[8:10]),int(q[3:5]),int(q[0:2]))
            if d1>d2:
                Label(exp, text='EXPIRED! on '+i[6]).grid(row=3, column=2)
                top=Tk()
                Label(top, text='EXPIRED!').pack()
            else:
                Label(exp, text=i[6]).grid(row=3, column=2)
    c.commit()

def exp_dt(): # shows medicine to expire in the coming week
    global c, cur, exp, top
    x=0
    z=1
    from datetime import datetime, timedelta 
    N = 7
    dt = datetime.now() + timedelta(days=N)
    d=str(dt)
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    d3 = date(int(d[0:4]),int(d[5:7]),int(d[8:10]))
    Label(exp,text='S.No'+'   '+'Name'+'     Qty.    '+'Exp_date').grid(row=6,column=0,columnspan=2)
    cur.execute("select * from med")
    for i in cur:
        s=i[6]
        d2=date(int('20'+s[8:10]),int(s[3:5]),int(s[0:2]))
        
        if d1<d2<d3:
            Label(exp,text=str(z)+'.      '+str(i[1])+'    '+str(i[3])+'    '+str(i[6])).grid(row=x+7,column=0,columnspan=2)
            x+=1
            z+=1
        elif d1>d2:
            top=Tk()
            Label(top,width=20, text=str(i[1])+' is EXPIRED!').pack()
    c.commit()


def billing(): # BILLING system
    global c, cur, apt, flag, t, name, name1, add, st, names, qty, sl, qtys, vc_id, n, namee, lb1
    t = 0
    vc_id = ''
    names = []
    qty = []
    sl = []
    n = []
    qtys = [''] * 10
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    if flag == 'st':
        st.destroy()
    else:
        apt.destroy()
    flag = 'st'

    st = Tk()
    st.title('BILLING SYSTEM')
    st.configure(bg="#f0f0f0")
    st.geometry('1000x600')
    # -------------------------background-------------------------
    # Load the background image using Pillow
    image_path = r"X:\New folder\Pharmacy Software u\background 1.jpg"  # Correct path to your JPEG file
    original_image = Image.open(image_path)
    resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize to match the window size, using updated resampling method
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = tk.Label(image=background_image)  # Ensure the label uses the resized image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image  

    # ----------------------------------------------------------------------------

    style = ttk.Style()
    style.configure('TButton', padding=5, relief="raised", font=('Arial', 10))

    Label(st, text='-' * 48 + 'BILLING SYSTEM' + '-' * 49, bg="#f0f0f0").grid(row=0, column=0, columnspan=7)
    Label(st, text='Enter Name: ', bg="#f0f0f0").grid(row=1, column=0)
    name1 = Entry(st)
    name1.grid(row=1, column=1)
    Label(st, text='Enter Cashier: ', bg="#f0f0f0").grid(row=2, column=0)
    add = Entry(st)
    add.grid(row=2, column=1)
    vc_id = Entry(st)
    vc_id.grid(row=3, column=1)
    # ttk.Button(st, text='Check V.C.', command=blue).grid(row=4, column=0)
    Label(st, text='-' * 115, bg="#f0f0f0").grid(row=6, column=0, columnspan=7)
    Label(st, text='SELECT PRODUCT', width=25, relief='ridge', bg="#f0f0f0").grid(row=7, column=0)
    Label(st, text=' RACK  QTY LEFT     COST          ', width=25, relief='ridge', bg="#f0f0f0").grid(row=7, column=1)
    ttk.Button(st, text='Add to bill', width=15, command=append2bill).grid(row=8, column=6)
    Label(st, text='QUANTITY', width=20, relief='ridge', bg="#f0f0f0").grid(row=7, column=5)
    qtys = Entry(st)
    qtys.grid(row=8, column=5)
    refresh()
    ttk.Button(st, width=15, text='Main Menu', command=main_menu).grid(row=1, column=6)
    ttk.Button(st, width=15, text='Refresh Stock', command=refresh).grid(row=3, column=6)
    ttk.Button(st, width=15, text='Reset Bill', command=billing).grid(row=4, column=6)
    ttk.Button(st, width=15, text='Print Bill', command=print_bill).grid(row=5, column=6)
    ttk.Button(st, width=15, text='Save Bill', command=make_bill).grid(row=7, column=6)

    st.mainloop()

def refresh():
    global cur, c, st, lb1, lb2, vsb
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(st,width=25, yscrollcommand=vsb.set)
    lb2=Listbox(st ,width=25,yscrollcommand=vsb.set)
    vsb.grid(row=8,column=2,sticky=N+S)
    lb1.grid(row=8,column=0)
    lb2.grid(row=8,column=1)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        lb1.insert(cx,str(i[0])+'. '+str(i[1]))
        lb2.insert(cx,' '+str(i[7])+'        '+str(i[3])+'             Rs '+str(i[4]))
    c.commit()
    lb1.bind('<<ListboxSelect>>', select_mn)

def select_mn(e): #store the selected medicine from listbox
    global st, lb1, n ,p, nm, sl1
    p=lb1.curselection()
    x=0
    sl1=''
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    cur.execute("select * from med")
    for i in cur:
        if x==int(p[0]):
            sl1=int(i[0])
            break
        x+=1    
    c.commit()
    print (sl1)
    nm=n[x]
    print (nm)
    
def append2bill(): # append to the bill
    global st, names, nm , qty, sl,cur, c, sl1
    sl.append(sl1)
    names.append(nm)
    qty.append(qtys.get())
    print (qty)
    print (sl[len(sl)-1],names[len(names)-1],qty[len(qty)-1])
    
def blue(): # check if valued customer
    global st ,c, cur, named, addd, t, vc_id
    cur.execute("select * from cus")
    for i in cur:
        if vc_id.get()!='' and int(vc_id.get())==i[2]:
            named=i[0]
            addd=i[1]
            Label(st,text=named,width=20).grid(row=1, column=1)
            Label(st,text=addd,width=20).grid(row=2, column=1)
            Label(st,text=i[2],width=20).grid(row=3, column=1)
            Label(st, text='Valued Customer!').grid(row=4, column=1)
            t=1
            break
    c.commit()

def make_bill(): # makes bill
    global t, c, B, cur, st, names, qty, sl , named, addd, name1, add,det, vc_id
    price=[0.0]*10
    q=0
    det=['','','','','','','','']
    det[2]=str(sl)
    for i in range(len(sl)):
        print (sl[i],' ',qty[i],' ',names[i])
    for k in range(len(sl)):
        cur.execute("select * from med where sl_no=?",(sl[k],))
        for i in cur:
            price[k]=int(qty[k])*float(i[4])
            print (qty[k],price[k])
            cur.execute("update med set qty_left=? where sl_no=?",(int(i[3])-int(qty[k]),sl[k]))
        c.commit()
    det[5]=str(random.randint(100,999))
    B='bill_'+str(det[5])+'.txt'
    total=0.00
    for i in range(10):
        if price[i] != '':
            total+=price[i] #totalling
    m='\n\n\n'
    m+="===============================================\n"
    m+="                                  No :%s\n\n" % det[5]
    m+="         Health Haven Pharmacy\n"
    m+="  10-B, Block E, Main Boulevard, Gulberg III, Lahore-Pakistan\n\n"
    m+="-----------------------------------------------\n"
    if t==1:
        m+="Name: %s\n" % named
        m+="Phone Number: %s\n" % addd
        det[0]=named
        det[1]=addd
        cur.execute('select * from cus')
        for i in cur:
            if i[0]==named:
                det[7]=i[2]
    else:
        m+="Name: %s\n" % name1.get()
        m+="Cashier name: %s\n" % add.get()
        det[0]=name1.get()
        det[1]=add.get()
    m+="-----------------------------------------------\n"
    m+="Product                      Qty.       Price\n"
    m+="-----------------------------------------------\n"#47, qty=27, price=8 after 2
    for i in range(len(sl)):
        if names[i] != 'nil':
            s1=' '
            s1=(names[i]) + (s1 * (27-len(names[i]))) + s1*(3-len(qty[i])) +qty[i]+ s1*(15-len(str(price[i])))+str(price[i]) + '\n'
            m+=s1
    m+="\n-----------------------------------------------\n"
    if t==1:
        ntotal=total*0.8
        m+='Total'+(' '*25)+(' '*(15-len(str(total)))) + str(total)+'\n'
        m+="Valued customer Discount"+ (' '*(20-len(str(total-ntotal))))+'-'+str(total-ntotal)+'\n'
        m+="-----------------------------------------------\n"
        m+='Total'+(' '*25)+(' '*(12-len(str(ntotal)))) +'Rs '+ str(ntotal)+'\n'
        det[3]=str(ntotal)
    else:
        m+='Total'+(' '*25)+(' '*(12-len(str(total)))) +'Rs '+ str(total)+'\n'
        det[3]=str(total)
        
    m+="-----------------------------------------------\n\n"
    m+="***Thank you for choosing Health Haven Pharmacy!***\n"
    m+="**Returns accepted within 2 days with original\n receipt.**\n"
    m+="===============================================\n"
    print (m)
    p=time.localtime()
    det[4]=str(p[2])+'/'+str(p[1])+'/'+str(p[0])
    det[6]=m
    bill=open(B,'w')
    bill.write(m)
    bill.close()
    cb=('cus_name','cus_add','items','Total_cost','bill_dt','bill_no','bill','val_id')
    cur.execute('insert into bills values(?,?,?,?,?,?,?,?)',(det[0],det[1],det[2],det[3],det[4],det[5],det[6],det[7]))
    c.commit()
    
def print_bill():
    global B
    win32api.ShellExecute (0,"print",B,'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
    


def show_rev():
    global c, cur, flag, rev
    apt.destroy()
    cb = ('cus_name', 'cus_add', 'items', 'Total_cost', 'bill_dt', 'bill_no', 'bill', 'val_id')
    flag = 'rev'
    rev = Tk()
    rev.title('TOTAL REVENUE')
    rev.configure(bg="#f0f0f0")
    rev.geometry('1000x600')
    # -------------------------background-------------------------
    # Load the background image using Pillow
    image_path = r"X:\New folder\Pharmacy Software u\background 1.jpg"  # Correct path to your JPEG file
    original_image = Image.open(image_path)
    resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize to match the window size, using updated resampling method
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = tk.Label(image=background_image)  # Ensure the label uses the resized image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image  

    # ----------------------------------------------------------------------------

    total = 0.0
    today = str(time.localtime()[2])+'/'+str(time.localtime()[1])+'/'+str(time.localtime()[0])

    Label(rev, text='Today: '+today, bg="#f0f0f0", font=("Arial", 14)).grid(row=0, column=0, pady=10)

    cur.execute('select * from bills')
    for i in cur:
        if i[4] == today:
            total += float(i[3])

    total_label = Label(rev, width=22, text='Total revenue: Rs '+str(total), bg='black', fg='white', font=("Arial", 18))
    total_label.grid(row=1, column=0, pady=10)

    cx = 0
    vsb = Scrollbar(rev, orient='vertical')
    lb1 = Listbox(rev, width=35, yscrollcommand=vsb.set, font=("Arial", 12))
    vsb.grid(row=2, column=1, sticky=N+S)
    lb1.grid(row=2, column=0)
    vsb.config(command=lb1.yview)

    cur.execute("select * from bills")
    for i in cur:
        if i[4] == today:
            cx += 1
            lb1.insert(cx, 'Bill No.: '+str(i[5])+'    : Rs '+str(i[3]))
    c.commit()

    ttk.Button(rev, text='Main Menu', command=main_menu).grid(row=15, column=0)

    rev.mainloop()


def search():   #search window medicine and symptom details
    global c, cur, flag, st, mn, sym, flags
    flag='st'
    apt.destroy()
    cur.execute("Select * from med")
    symp = ['nil']
    med_name = ['nil']
    for i in cur:
        symp.append(i[5])
        med_name.append(i[1])
    st = Tk()
    st.title('SEARCH ')
    st.configure(bg="#f0f0f0")
    st.geometry('1000x600')
    # -------------------------background-------------------------
    # Load the background image using Pillow
    image_path = r"X:\New folder\Pharmacy Software u\background 1.jpg"  # Correct path to your JPEG file
    original_image = Image.open(image_path)
    resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize to match the window size, using updated resampling method
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = tk.Label(image=background_image)  # Ensure the label uses the resized image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image  

    # ----------------------------------------------------------------------------
    
    Label(st, text=' SEARCH FOR MEDICINE ', bg="#f0f0f0").grid(row=0, column=0, columnspan=3)
    Label(st, text='~'*40, bg="#f0f0f0").grid(row=1, column=0, columnspan=3)
    Label(st, text='Symptom Name', bg="#f0f0f0").grid(row=3, column=0)
    sym = Spinbox(st, values=symp)
    sym.grid(row=3, column=1)
    ttk.Button(st, width=15, text='Search', command=search_med).grid(row=3, column=2)
    Label(st, text='-'*70, bg="#f0f0f0").grid(row=4, column=0, columnspan=3)
    
    if flags == 'apt1':
        ttk.Button(st, width=15, text='Main Menu', command=main_cus).grid(row=6, column=2)
    else:
        ttk.Button(st, width=15, text='Main Menu', command=main_menu).grid(row=6, column=2)
    
    st.mainloop()

def search_med():
    global c, cur, st, sym, columns
    cur.execute("select * from med")
    y=[]
    x=0
    for i in cur:
        if i[5]==sym.get():
            y.append(str(i[0])+'. '+str(i[1])+'  Rs '+str(i[4])+'    Rack : '+str(i[7])+'    Mfg : '+str(i[8]))
            x=x+1
    top=Tk()
    for i in range(len(y)):
        Label(top,text=y[i]).grid(row=i, column=0)
    Button(top,text='OK',command=top.destroy).grid(row=5, column=0)
    c.commit()
    top.mainloop()
    

def again():    # for login window
    global un, pwd, flag, root, apt
    if flag == 'apt':
        apt.destroy()

    
    root = Tk()
    root.title('LogicMinds SOFTWARE SOLUTIONS')
    root.configure(bg="#f0f0f0")
    root.geometry('1000x600')  # Adjust the size of the window

    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 12), bg="#f0f0f0")
    style.configure('TButton', padding=5, relief="raised", font=('Arial', 10))
    # -------------------------background-------------------------
    # Load the background image using Pillow
    image_path = r"X:\New folder\Pharmacy Software u\background 1.jpg"  # Correct path to your JPEG file
    original_image = Image.open(image_path)
    resized_image = original_image.resize((1000, 600), Image.Resampling.LANCZOS)  # Resize to match the window size, using updated resampling method
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = tk.Label(image=background_image)  # Ensure the label uses the resized image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image  

    # ----------------------------------------------------------------------------


    Label(root, text='Health Haven Pharmacy', font=('Arial', 18, 'bold'), bg="#f0f0f0").grid(row=0, column=0, columnspan=5)
    Label(root, text="10-B, Block E, Main Boulevard, Gulberg III, Lahore-Pakistan", bg="#f0f0f0").grid(row=1, column=0, columnspan=5)
    separator = Frame(root, height=2, bd=1, relief=SUNKEN, bg="black")
    separator.grid(row=2, column=0, columnspan=5, sticky="ew", pady=5)
    
    Label(root, text='Username', bg="#f0f0f0").grid(row=3, column=0)
    un = Entry(root, width=15)
    un.grid(row=3, column=1)
    
    Label(root, text='Password', bg="#f0f0f0").grid(row=4, column=0)
    pwd = Entry(root, width=15, show='*')
    pwd.grid(row=4, column=1)
    
    ttk.Button(root, width=8, text='Enter', command=check).grid(row=5, column=0)
    ttk.Button(root, width=8, text='Close', command=root.destroy).grid(row=5, column=1)

    root.mainloop()
   

# ------------------------FOR LOGIN--------------------------------
# ------------------------Singleton Pattern------------------------
class Admin():
    def handle(self, context):
        root.destroy()
        open_win()  

class User():
    def handle(self, context):
        root.destroy()
        open_cus()  

class LoginContext:
    _instance = None  # Class variable to hold the single instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if LoginContext._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.state = None
            self.initialize_global_variables()
            LoginContext._instance = self

    def initialize_global_variables(self):
        # Initialize all global variables used in main_menu
        self.sto = None
        self.rev = None
        self.st = None
        self.st1 = None
        self.val = None
        self.exp = None
        self.d = None
        self.flag = None

    def set_state(self, state):
        self.state = state

    def execute(self):
        if self.state:
            self.state.handle(self)

def check():
    global un, pwd, l, root
    u = un.get()
    p = pwd.get()
    context = LoginContext.get_instance()

    l.execute("SELECT * FROM log")
    for i in l:
        if i[0] == u and i[1] == p:
            if u == 'admin':
                context.set_state(Admin())
            else:
                context.set_state(User())
            context.execute()
            return
    login.commit()
    print("Invalid credentials.")  # Notify about failed login

def main_menu():
    context = LoginContext.get_instance()
    context.set_state(MainMenuState())
    context.execute()




def main_menu(): #controls open and close of main menu window----------------------------------------RETURN TO MAIN MENU
    global sto, apt, flag, root, st, val, exp, st1,rev
    if flag=='sto':
        sto.destroy()
    if flag=='rev':
        rev.destroy()
    elif flag=='st':
        st.destroy()
    elif flag=='st1':
        st1.destroy()
    elif flag=='val':
        val.destroy()
    elif flag=='exp':
        exp.destroy()
    elif flag=='d':
        d.destroy()
    open_win()    

def main_cus():
    global st, flag, exp
    if flag=='exp':
        exp.destroy()
    elif flag=='st':
        st.destroy()
    open_cus()
    
def open_cus(): #OPENS MAIN MENU-------------MAIN MENU
    global apt, flag, flags
    flags='apt1'
    apt=Tk()
    apt.title("Interface")
    Label(apt, text="MEDPLUS CHEMIST AND DRUGGIST").grid(row=0,column=0)
    Label(apt, text='*'*40).grid(row=1,column=0)
    Label(apt, text='*  WELCOME  *').grid(row=2,column=0)
    Label(apt, text='-'*40).grid(row=3,column=0)
    Label(apt, text="Customer Services").grid(row=4,column=0)
    Label(apt, text='-'*40).grid(row=5,column=0)
    Button(apt,text='Search', width=15, command=search).grid(row=6,column=0)
    Button(apt,text='Expiry Check', width=15, command=exp_date).grid(row=7,column=0)
    
    Label(apt, text='-'*40).grid(row=8,column=0)    
    Button(apt,text='Logout',command=again1).grid(row=9, column=0)
    apt.mainloop()

# def again1():
#     global flags
#     apt.destroy()
#     flags=''
#     again()

# -------------------------------STATE PATTERN-----------------------------
class AppState:
    def handle(self, context):
        raise NotImplementedError("Handle method must be defined in subclass.")

class DefaultState(AppState):
    def handle(self, context):
        global flags, apt
        apt.destroy()
        flags = ''
        context.transition_to(LoginState())

class LoginState(AppState):
    def handle(self, context):
        # Possibly handle reinitialization or redirection to a login screen
        print("Redirecting to login screen.")
        again()

class ApplicationContext:
    def __init__(self):
        self.state = DefaultState()  # Initial state

    def transition_to(self, state):
        self.state = state

    def request(self):
        self.state.handle(self)

def again1():
    global context  # Assuming `context` is globally available and initialized
    context.request()

again()

