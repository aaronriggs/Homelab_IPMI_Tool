import subprocess
from threading import Thread
import tkinter as tk
from tkinter import Text, Radiobutton, Menu, IntVar, Toplevel, CENTER, NORMAL, Tk, ttk

#tkinter setup
root = tk.Tk()
root.title("Homelab IPMI Server Management Tool")
frm = ttk.Frame(root, padding=20)
frm.grid()
textbox_bg_color = "white"
text_font_color = "black"

#functions
def power_on():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
                             "-P", user_credentials[2], "power", "on"], capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stdout.decode()))
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def power_off():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
                             "-P", user_credentials[2], "power", "off"], capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stdout.decode()))
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def power_status():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "power", "status"], capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stdout.decode()))
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def default_pci_fans_off():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0xce", "0x00", "0x16", "0x05", "0x00",
            "0x00", "0x00", "0x05", "0x00", "0x01", "0x00", "0x00"],
            capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stdout.decode()))
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def default_pci_fans_on():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0xce", "0x00", "0x16", "0x05", "0x00",
            "0x00", "0x00", "0x05", "0x00", "0x00", "0x00", "0x00"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stdout.decode()))
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def manual_fan_control_on():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x01", "0x00"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stdout.decode()))
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def manual_fan_control_off():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x01", "0x01"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stdout.decode()))
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def fans_2160():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x02", "0xff", "0x00"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", "Fans commanded to 2160rpm")
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def fans_3840():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x02", "0xff", "0x0a"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", "Fans commanded to 3840rpm")
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def fans_5880():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x02", "0xff", "0x19"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", "Fans commanded to 5880rpm")
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def fans_8520():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x02", "0xff", "0x29"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", "Fans commanded to 8520rpm")
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def fans_10920():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x02", "0xff", "0x39"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", "Fans commanded to 10920rpm")
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def fans_13000():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x02", "0xff", "0x49"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", "Fans commanded to 13000rpm")
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def fans_15600():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x02", "0xff", "0x59"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", "Fans commanded to 15600rpm")
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def fans_17640():
    pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", user_credentials[0], "-U", user_credentials[1],
            "-P", user_credentials[2], "raw", "0x30", "0x30", "0x02", "0xff", "0x64"],
                          capture_output=True)
    if pipe.returncode == 0:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", "Fans commanded to 17640rpm")
    else:
        ew.delete("1.0", tk.END)
        ew.insert("1.0", str(pipe.stderr.decode()))

def get_stats_thread():
    t1=Thread(target=get_stats)
    t1.daemon = True
    t1.start()

cpu_temp1 = ['  '] # used in auto fan control, initialized as if pipe output is not present(system off, comms error, etc)
def get_stats():
    try:
        pipe = subprocess.run(["ipmi-sensors", "-h", user_credentials[0], "-u", user_credentials[1],
                "-p",user_credentials[2], "-l", "user", "-D", "LAN_2_0", "--record-ids=14,15,16,17,18,19,20,25,26,27,98"],
                              capture_output=True)
        output = pipe.stdout.decode().strip() #decode standard output of pipe
        cpu_temp1[0] = '  ' #output format if desired value not present
        cpu_temp1[0] = output[605:607]
        if pipe.returncode == 0:
            gs.delete("1.0", tk.END)
            gs.insert(tk.END, output)  # can also use "end"
        else:
            gs.delete("1.0", tk.END)
            gs.insert("1.0", str(pipe.stderr.decode()))
    finally:
        root.after(4000, get_stats_thread)
        return cpu_temp1

def auto_fan_control_config():
    # disable user selectable fan speeds if auto fan control is selected
    b10.config(state='disabled')
    b11.config(state='disabled')
    b12.config(state='disabled')
    b13.config(state='disabled')
    b14.config(state='disabled')
    b15.config(state='disabled')
    b16.config(state='disabled')
    b17.config(state='disabled')
    # ensures secondary text widget is started (if not done so by power status or error previously)
    # message may appear for extended periods if cpu_temp is between configured fan speed values
    ew.delete("1.0", tk.END)
    ew.insert("1.0", "Auto Fan Control Enabled")
    auto_fan_control_thread()

def auto_fan_control_thread():
    t2=Thread(target=auto_fan_control)
    t2.daemon = True
    t2.start()

fan_state = [0] # stores previously used fan state
def auto_fan_control():
    try:
        print(cpu_temp1)
        print(type(cpu_temp1))
        if cpu_temp1[0] == '  ':
            return
        else:
            cpu_temp = (int(cpu_temp1[0]))
            # fan temperature curve here
            if cpu_temp < 30:
                if fan_state[0] == 2160:
                    return
                else:
                    t3 = Thread(target=fans_2160)
                    t3.daemon = True
                    t3.start()
                    fan_state[0] = 2160

            elif 31 <= cpu_temp < 39:
                if fan_state[0] == 3840:
                    return
                else:
                    t3 = Thread(target=fans_3840)
                    t3.daemon = True
                    t3.start()
                    fan_state[0] = 3840

            elif 40 <= cpu_temp < 44:
                if fan_state[0] == 5880:
                    return
                else:
                    t3 = Thread(target=fans_5880)
                    t3.daemon = True
                    t3.start()
                    fan_state[0] = 5880

            elif 45 <= cpu_temp < 49:
                if fan_state[0] == 8520:
                    return
                else:
                    t3 = Thread(target=fans_8520)
                    t3.daemon = True
                    t3.start()
                    fan_state[0] = 8520

            elif 50 <= cpu_temp < 54:
                if fan_state[0] == 10920:
                    return
                else:
                    t3 = Thread(target=fans_10920)
                    t3.daemon = True
                    t3.start()
                    fan_state[0] = 10920

            elif 55 <= cpu_temp < 59:
                if fan_state[0] == 13000:
                    return
                else:
                    t3 = Thread(target=fans_13000)
                    t3.daemon = True
                    t3.start()
                    fan_state[0] = 13000

            elif 60 <= cpu_temp < 64:
                if fan_state[0] == 15600:
                    return
                else:
                    t3 = Thread(target=fans_15600)
                    t3.daemon = True
                    t3.start()
                    fan_state[0] = 15600

            elif cpu_temp >= 65:
                if fan_state[0] == 17640:
                    return
                else:
                    t = Text(root, width=65, height=5, bg="red", fg="white")
                    t.grid(column=0, row=12, pady=20)
                    t.insert("1.0", "TEMP WARNING - FANS COMMANDED TO MAX")
                    t3 = Thread(target=fans_17640)
                    t3.daemon = True
                    t3.start()
                    fan_state[0] = 17640
            else:
                pass
    finally:
        root.after(4000, auto_fan_control_thread)

def fans_to_manual():
    ew.delete("1.0", tk.END)
    ew.insert("1.0", "Manual fan control selected. Please select a fan speed.")
    b10.config(state='NORMAL')
    b11.config(state='NORMAL')
    b12.config(state='NORMAL')
    b13.config(state='NORMAL')
    b14.config(state='NORMAL')
    b15.config(state='NORMAL')
    b16.config(state='NORMAL')
    b17.config(state='NORMAL')
    fan_state[0] = 0 #delete fan_state data here
    return

user_credentials = []
def submit_entry_fields():
    user_credentials.insert(0, e1.get())
    user_credentials.insert(1, e2.get())
    user_credentials.insert(2, e3.get())
    switch_button_state_on()
    return user_credentials

#changes buttons to working after user credentials submitted
def switch_button_state_on():
    b3.config(state=NORMAL)
    b4.config(state=NORMAL)
    b5.config(state=NORMAL)
    b6.config(state=NORMAL)
    b7.config(state=NORMAL)
    b8.config(state=NORMAL)
    b9.config(state=NORMAL)
    b10.config(state=NORMAL)
    b11.config(state=NORMAL)
    b12.config(state=NORMAL)
    b13.config(state=NORMAL)
    b14.config(state=NORMAL)
    b15.config(state=NORMAL)
    b16.config(state=NORMAL)
    b17.config(state=NORMAL)
    b18.config(state=NORMAL)
    rb1.config(state="normal")
    rb2.config(state="normal")

def about():
    file_window = Toplevel(root)
    file_window.title("About")
    file_window.geometry('300x50')
    ttk.Label(file_window, text="Version 1.08", anchor=CENTER).grid(column=2, row=0)
    ttk.Label(file_window, text="Created by Aaron Riggs", anchor=CENTER).grid(column=2, row=1)

def end():
    root.withdraw()
    root.update_idletasks()
    root.quit()
    root.destroy()

#user credentials
ttk.Label(frm, text="IP Address").grid(row=0, column=0, padx=15)
ttk.Label(frm, text="Username").grid(row=1, column=0)
ttk.Label(frm, text="Password").grid(row=2, column=0)
e1 = ttk.Entry(frm)
e2 = ttk.Entry(frm)
e3 = ttk.Entry(frm, show="*")
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
b1 = ttk.Button(frm, text='Submit', width=11, command=submit_entry_fields)
b1.grid(row=3,column=1)

"""all other buttons, .grid must be placed AFTER button creation to
allow switch_button_state to work (nonetype error otherwise)"""
b3 = ttk.Button(frm, text="Power On ", width=11, state="disabled", command=power_on)
b3.grid(column=2, row=0, padx=10)
b4 = ttk.Button(frm, text="Power Off", width=11, command=power_off, state="disabled")
b4.grid(column=2, row=1)
b5 = ttk.Button(frm, text="System Stats", width=11, command=get_stats_thread, state="disabled")
b5.grid(column=0, row=6)
b6 = ttk.Button(frm, text="Default Dell PCI-E Cooling On", width=30, command=default_pci_fans_on, state="disabled")
b6.grid(column=3, row=0, padx=5)
b7 = ttk.Button(frm, text="Default Dell PCI-E Cooling Off", width=30, command=default_pci_fans_off, state="disabled")
b7.grid(column=3, row=1)
b8 = ttk.Button(frm, text="User Fan Control On", width=22, command=manual_fan_control_on, state="disabled")
b8.grid(column=4, row=0, padx=5)
b9 = ttk.Button(frm, text="Dell Fan Control On", width=22, command=manual_fan_control_off, state="disabled")
b9.grid(column=4, row=1)
b10 = ttk.Button(frm, text="Fans at 2160 ", command=fans_2160, state="disabled")
b10.grid(column=5, row=0, padx=5)
b11 = ttk.Button(frm, text="Fans at 3840 ", command=fans_3840, state="disabled")
b11.grid(column=5, row=1)
b12 = ttk.Button(frm, text="Fans at 5880 ", command=fans_5880, state="disabled")
b12.grid(column=5, row=2)
b13 = ttk.Button(frm, text="Fans at 8520 ", command=fans_8520, state="disabled")
b13.grid(column=5, row=3)
b14 = ttk.Button(frm, text="Fans at 10920", command=fans_10920, state="disabled")
b14.grid(column=6, row=0, padx=5)
b15 = ttk.Button(frm, text="Fans at 13000", command=fans_13000, state="disabled")
b15.grid(column=6, row=1)
b16 = ttk.Button(frm, text="Fans at 15600", command=fans_15600, state="disabled")
b16.grid(column=6, row=2)
b17 = ttk.Button(frm, text="Fans at 17640", command=fans_17640, state="disabled")
b17.grid(column=6, row=3)
b18 = ttk.Button(frm, text="Power Status", width=11, command=power_status, state="disabled")
b18.grid(column=2, row=2)

#radio buttons for user defined fan control
user_selected_fan_curve = IntVar() # remove, why was this created
rb1 = Radiobutton(frm, text='Manual Fans', width=11,  variable=user_selected_fan_curve,
                  value=1, state="disabled", command=fans_to_manual)
rb1.grid(column=5, row=4)
rb2 = Radiobutton(frm, text='Auto Fans', width=11, variable=user_selected_fan_curve,
                  value=2, state="disabled", command=auto_fan_control_config)
rb2.grid(column=6, row=4)

#get stats "window"
ttk.Label(text="System stats update every 4 seconds...", anchor=CENTER).grid(column=0, row=1)
gs = Text(root, width=65, height=12, bg=textbox_bg_color, fg=text_font_color)
gs.grid(column=0, row=8, pady=20)
gs.insert("1.0", "Please log in and select System Stats to view...")

#informational or error "window"
ew = Text(root, width=65, height=5, bg=textbox_bg_color, fg=text_font_color)
ew.grid(column=0, row=12, pady=20)
ew.insert("1.0", "Please log in to see informational messages...")

#menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=end) # made function to quit and destroy
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About...", command=about)


if __name__ == '__main__':
    root.mainloop()
