#Version 1.16
import subprocess
from threading import Thread
import tkinter as tk
from tkinter import Text, ttk

def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Homelab IPMI Server Management Tool")
        model = Model("ini")# initializes Model class
        #Initialize the View class with tk.Tk and place in the root window
        root = View(self) # creates root window
        root.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5) #locates window on root and fills it NSEW
        # create a controller, and pass in the Model Class and tk.Tk
        controller = Controller(model, root)
        # set the controller to view
        root.set_controller(controller)


class Model:
    def __init__(self, creds):
        self.creds = creds
        self.fan_state = [0] # stores previously used fan state to stop fan speed changes if not needed
        self.temp_messages = ''

    def save(self):
        return self.creds

    def power_mode(self, power_commanded_status): # controls power on, off, reboot, or power status
        self.power_commanded_status = power_commanded_status
        self.pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", self.creds[0], "-U", self.creds[1],
                            "-P", self.creds[2], "power", self.power_commanded_status], capture_output=True)
        self.pipe_output_from_model = str(self.pipe.stdout.decode())
        self.pipe_output_from_model_error = str(self.pipe.stderr.decode())
        self.pipe_out = ''
        if self.pipe_output_from_model == "":
            self.pipe_out = self.pipe_output_from_model_error
        else:
            self.pipe_out = self.pipe_output_from_model
        return self.pipe_out

    def pci_mode(self, pci_commanded_status): # controls pci-e fan profile (state persists in BMC)
        self.pci_commanded_status = pci_commanded_status
        self.pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", self.creds[0], "-U", self.creds[1],
                               "-P", self.creds[2], "raw", "0x30", "0xce", "0x00", "0x16", "0x05", "0x00",
                               "0x00", "0x00", "0x05", "0x00", self.pci_commanded_status, "0x00", "0x00"],
                              capture_output=True)

    def fan_mode(self, fan_profile_commanded_status): # uses default dell fan curve or user control of fans
        self.fan_profile_commanded_status = fan_profile_commanded_status
        self.pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", self.creds[0], "-U", self.creds[1],
                               "-P", self.creds[2], "raw", "0x30", "0x30", "0x01",
                                self.fan_profile_commanded_status], capture_output=True)

    # controls Fan Speed RPM, whether manually selected OR issued by Model.auto_fan_control
    def fan_speed(self, fan_speed_commanded_status):
        self.fan_speed_commanded_status = fan_speed_commanded_status
        self.pipe = subprocess.run(["ipmitool", "-I", "lanplus", "-H", self.creds[0], "-U", self.creds[1],
            "-P", self.creds[2], "raw", "0x30", "0x30", "0x02", "0xff", self.fan_speed_commanded_status],
                          capture_output=False)

    # Provides System Stats from a selected list of sensors
    def system_stats(self):
        self.cpu_temp1 = ['  ']  # used in auto fan control, initialized as if pipe output is not present
        self.pipe = subprocess.run(["ipmi-sensors", "-h", self.creds[0], "-u", self.creds[1],
                               "-p", self.creds[2], "-l", "user", "-D", "LAN_2_0",
                               "--record-ids=14,15,16,17,18,19,20,25,26,27,98"],
                              capture_output=True)
        self.pipe_output_from_model = ''
        self.pipe_output_from_model = self.pipe.stdout.decode().strip()  # decode standard output of pipe
        self.cpu_temp1[0] = '  '  # output format for auto fan control if desired int value not present
        self.cpu_temp1[0] = self.pipe_output_from_model[605:607]
        return self.cpu_temp1, self.pipe_output_from_model

    # auto fan control logic. use of < and not <= to allow less fan speed changes between temp ranges
    def auto_fan_control(self):
        try:
            if self.cpu_temp1[0] == '  ':
                return
            else:
                cpu_temp = (int(self.cpu_temp1[0]))
                self.temp_messages = ""
                # fan temperature curve here
                if cpu_temp < 30:
                    if self.fan_state[0] == 2160:
                        return
                    else:
                        self.fan_state[0] = 2160
                        self.temp_messages = "Fans commanded to 2160rpm"
                        self.fan_speed("0x00")

                elif 31 <= cpu_temp < 39:
                    if self.fan_state[0] == 3840:
                        return
                    else:
                        self.fan_state[0] = 3840
                        self.temp_messages = "Fans commanded to 3840rpm"
                        self.fan_speed("0x0a")

                elif 40 <= cpu_temp < 44:
                    if self.fan_state[0] == 5880:
                        return
                    else:
                        self.fan_state[0] = 5880
                        self.temp_messages = "Fans commanded to 5880rpm"
                        self.fan_speed("0x19")

                elif 45 <= cpu_temp < 49:
                    if self.fan_state[0] == 8520:
                        return
                    else:
                        self.fan_state[0] = 8520
                        self.temp_messages = "Fans commanded to 8520rpm"
                        self.fan_speed("0x29")

                elif 50 <= cpu_temp < 54:
                    if self.fan_state[0] == 10920:
                        return
                    else:
                        self.fan_state[0] = 10920
                        self.temp_messages = "Fans commanded to 10920rpm"
                        self.fan_speed("0x39")

                elif 55 <= cpu_temp < 59:
                    if self.fan_state[0] == 13000:
                        return
                    else:
                        self.fan_state[0] = 13000
                        self.temp_messages = "Fans commanded to 13000rpm"
                        self.fan_speed("0x49")

                elif 60 <= cpu_temp < 64:
                    if self.fan_state[0] == 15600:
                        return
                    else:
                        self.fan_state[0] = 15600
                        self.temp_messages = "Fans commanded to 15600rpm"
                        self.fan_speed("0x59")

                elif cpu_temp >= 65:
                    if self.fan_state[0] == 17640:
                        return
                    else:
                        self.fan_state[0] = 17640
                        self.temp_messages = "TEMP WARNING - FANS COMMANDED TO MAX"
                        self.fan_speed("0x64")
                else:
                    return
        finally:
            return self.temp_messages, self.fan_state

class Controller:
    def __init__(self, model, root):
        self.model = model
        self.root = root

    def save(self, creds): #credentials from View becomes creds here
        self.model.creds = creds
        self.model.save() # saves credentials in Model
        self.root.display_user_interface() #displays second "View" in View

    def one_thread_to_rule_them_all(self, method_to_call, var_passed_to_method):
        self.method_to_call = method_to_call
        self.var_passed_to_method = var_passed_to_method
        t900 = Thread(target=self.method_to_call(var_passed_to_method))
        t900.daemon = True
        t900.start()
    def power_mode(self, power_commanded_status):
        self.power_commanded_status = power_commanded_status
        self.model.power_mode(self.power_commanded_status) # calls power_mode in Model and gives it status var
        self.root.pipe_message(self.model.pipe_out) # message back to view
    def pci_mode(self, pci_commanded_status):
        self.pci_commanded_status = pci_commanded_status
        self.model.pci_mode(self.pci_commanded_status) # calls pci_mode in Model and gives it status var
    def fan_mode(self, fan_profile_commanded_status):
        self.fan_profile_commanded_status = fan_profile_commanded_status
        self.model.fan_mode(self.fan_profile_commanded_status) # calls fan_mode in Model and gives it status var

    # creates a new thread for System Stats to run on and provides CPU temp for auto fan control in Model
    def system_stats_thread(self):
        t5 = Thread(target=self.system_stats)
        t5.daemon = True
        t5.start()
    def system_stats(self):
        self.model.system_stats() # calls system_stats in Model
        self.root.system_stats_message(self.model.pipe_output_from_model) # sends stats message back to view

    # AUTO fan control that executes fan speed adjustments
    def auto_fan_control_thread(self):
        self.fan_state = [0] # resets fan state var to zero on auto fan selection, clearing old value
        t7 = Thread(target=self.auto_fan_control) # calls auto_fan_control
        t7.daemon = True
        t7.start()
    def auto_fan_control(self):
        self.model.auto_fan_control() # calls auto_fan_control in Model
        self.root.cpu_temp_message(self.model.temp_messages)
    # manual fan speed adjustments
    def fan_speed(self, fan_speed_commanded_status):
        self.fan_speed_commanded_status = fan_speed_commanded_status
        self.model.fan_speed(self.fan_speed_commanded_status) # calls fan_speed in Model and gives it status var

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # set the controller and initialize credentials
        self.credentials = []
        self.radio_button_selected = 0
        self.controller = None
        # create widgets
        self.textbox_bg_color = "white"
        self.text_font_color = "black"
        # labels for user credential fields
        self.ip = ttk.Label(self, text="IP Address")
        self.ip.grid(column=0, row=0, sticky="W", padx=5)
        self.username = ttk.Label(self, text="Username")
        self.username.grid(column=0, row=1, sticky="W", padx=5)
        self.password = ttk.Label(self, text="Password")
        self.password.grid(column=0, row=2, sticky="W", padx=5)
        # credential entry
        self.user_cred_ip, self.user_cred_user, self.user_cred_pass = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.e1 = ttk.Entry(self, textvariable=self.user_cred_ip)
        self.e2 = ttk.Entry(self, textvariable=self.user_cred_user)
        self.e3 = ttk.Entry(self, show="*", textvariable=self.user_cred_pass)
        self.e1.grid(column=1, row=0, sticky="W")
        self.e2.grid(column=1, row=1, sticky="W")
        self.e3.grid(column=1, row=2, sticky="W")
        # save button
        self.save_button = ttk.Button(self, text='Save', command=self.save_button_clicked)
        self.save_button.grid(column=1, row=3, padx=10)
        # labels
        self.label1 = ttk.Label(self, text="System stats update every 4 seconds...")
        self.label2 = ttk.Label(self, text="Select Manual or Auto fans", foreground='green')
        # system power manipulation buttons
        self.b3 = ttk.Button(self, text="Power On ", width=11, command=lambda:
        self.power_mode_button_clicked("on", "Power On"), state="enabled")
        self.b4 = ttk.Button(self, text="Power Off", width=11, command=lambda:
            self.power_mode_button_clicked("off", "Power Off"), state="enabled")
        self.b19 = ttk.Button(self, text="Reboot", width=11, command=lambda:
            self.power_mode_button_clicked("reset", "Warm Reset"), state="enabled")
        self.b18 = ttk.Button(self, text="Power Status", width=11,
            command=lambda: self.power_mode_button_clicked("status", "Power Status"),
            state="enabled")
        # system stats buttons
        self.b5 = ttk.Button(self, text="System Stats", width=11, command=self.system_stats_clicked,
            state="enabled")
        self.sys_stats_label = ttk.Label(self, text="<-- Select System Stats to enable fan control.",
            foreground='green')
        # pci-e cooling profile buttons, state persists
        self.b6 = ttk.Button(self, text="Default Dell PCI-E Profile On", width=30, command=lambda:
            self.pci_button_clicked("0x00", "Default Dell PCI-E Profile On"),
            state="enabled")
        self.b7 = ttk.Button(self, text="Default Dell PCI-E Profile Off", width=30, command=lambda:
            self.pci_button_clicked("0x01", "Default Dell PCI-E Profile Off"),
            state="enabled")
        # buttons allowing default or user fan control, state persists
        self.b8 = ttk.Button(self, text="User Fan Control On", width=20,
            command=lambda: self.system_fan_control_clicked("0x00", "User Fan Control On"),
            state="enabled")
        self.b9 = ttk.Button(self, text="Dell Fan Control On", width=20,
            command=lambda: self.system_fan_control_clicked("0x01", "Dell Fan Control On"),
            state="enabled")
        # fan speed buttons
        self.b10 = ttk.Button(self, text="Fans at 2160", width=11, command=lambda:
            self.manual_fan_speed_clicked("0x00", "2160"),state="enabled")
        self.b11 = ttk.Button(self, text="Fans at 3840", width=11, command=lambda:
            self.manual_fan_speed_clicked("0x0a", "3840"),state="enabled")
        self.b12 = ttk.Button(self, text="Fans at 5880", width=11, command=lambda:
            self.manual_fan_speed_clicked("0x19", "5880"),state="enabled")
        self.b13 = ttk.Button(self, text="Fans at 8520", width=11, command=lambda:
            self.manual_fan_speed_clicked("0x29", "8520"),state="enabled")
        self.b14 = ttk.Button(self, text="Fans at 10920", width=11, command=lambda:
            self.manual_fan_speed_clicked("0x39", "10920"), state="enabled")
        self.b15 = ttk.Button(self, text="Fans at 13000", width=11, command=lambda:
            self.manual_fan_speed_clicked("0x49", "13000"), state="enabled")
        self.b16 = ttk.Button(self, text="Fans at 15600", width=11, command=lambda:
            self.manual_fan_speed_clicked("0x59", "15600"), state="enabled")
        self.b17 = ttk.Button(self, text="Fans at 17640", width=11, command=lambda:
            self.manual_fan_speed_clicked("0x64", "17640"), state="enabled")
        # informational windows
        self.gs = Text(self, width=65, height=12, bg=self.textbox_bg_color, fg=self.text_font_color, undo=False)
        self.ew = Text(self, width=65, height=5, bg=self.textbox_bg_color, fg=self.text_font_color, undo=False)
        # manual fan speed or auto fan control selection (now as buttons)
        self.rb1 = tk.Button(self, text='Manual Fans', width=9, command=self.enable_manual_fan_buttons,
                               state="normal")
        self.rb2 = tk.Button(self, text='Auto Fans', width=9, command=self.enable_auto_fan_control,
                               state="normal")

    def set_controller(self, controller):
        self.controller = controller

    def save_button_clicked(self):
        if self.controller:
            self.credentials = [self.user_cred_ip.get(), self.user_cred_user.get(), self.user_cred_pass.get()]
            self.controller.save(self.credentials) # goes to controller save and passes credentials into creds

    def display_user_interface(self):
        self.label1.grid(column=3, row=5)
        self.label2.grid(column=5, row=5, columnspan=3, sticky="nsew")
        self.b3.grid(column=2, row=0, sticky="W", padx=10)
        self.b4.grid(column=2, row=1, sticky="W", padx=10)
        self.b5.grid(column=0, row=4)
        self.sys_stats_label.grid(column=1, row=4, columnspan=3, sticky="W", padx=10)
        self.b6.grid(column=3, row=0, sticky="W")
        self.b7.grid(column=3, row=1, sticky="W")
        self.b8.grid(column=4, row=0, padx=5, sticky="W")
        self.b9.grid(column=4, row=1)
        self.b18.grid(column=2, row=3, sticky="W", padx=10)
        self.b19.grid(column=2, row=2, sticky="W", padx=10)
        self.rb1.grid(column=5, row=4, sticky="W", padx=5, pady=5)
        self.rb2.grid(column=6, row=4, sticky="W", pady=5)
        self.gs.grid(column=2, row=8, pady=20, columnspan=4, sticky="W")
        self.ew.grid(column=2, row=12, pady=20, columnspan=4, sticky="W")
        # disables auto fan control button until system stats runs
        self.rb1.config(relief="sunken", state="disabled")
        self.rb2.config(relief="sunken", state="disabled")

    # manual fan control buttons enabled from Manual Fans Radio Button
    def enable_manual_fan_buttons(self):
        self.pipe_message("Manual Fan Control selected. Please pick a fan speed...")
        self.label2['text'] = ''
        self.radio_button_selected = 1 # stored selection to check against and end auto fan thread
        # configure selection buttons to prevent multiple clicks (and multiple threads starting)
        self.rb1.config(relief="sunken", state="disabled") # disables manual fan control button
        self.rb2.config(relief="raised", state="normal") # enables auto fan control button
        # calling grid after a grid_forget shows buttons again (or enables them if not forgotten)
        self.rb2.grid(column=6, row=4, sticky="W", pady=3)
        self.b10.grid(column=5, row=0, sticky="W", padx=5)
        self.b11.grid(column=5, row=1, sticky="W", padx=5)
        self.b12.grid(column=5, row=2, sticky="W", padx=5)
        self.b13.grid(column=5, row=3, sticky="W", padx=5)
        self.b14.grid(column=6, row=0, sticky="W")
        self.b15.grid(column=6, row=1, sticky="W")
        self.b16.grid(column=6, row=2, sticky="W")
        self.b17.grid(column=6, row=3, sticky="W")

    def enable_auto_fan_control(self):
        self.radio_button_selected = 2 # stored selection to check against and continue auto fan thread
        self.label2['text'] = ''
        # configure selection buttons to prevent multiple clicks (and multiple threads starting)
        self.rb1.config(relief="raised", state="normal") # enables manual fan control button
        self.rb2.config(relief="sunken", state="disabled") # disables auto fan control button
        # "disable" manual fan speed buttons
        self.b10.grid_forget()
        self.b11.grid_forget()
        self.b12.grid_forget()
        self.b13.grid_forget()
        self.b14.grid_forget()
        self.b15.grid_forget()
        self.b16.grid_forget()
        self.b17.grid_forget()
        self.pipe_message("Auto Fan Control selected. Enabling...")
        self.after(2300, self.controller.auto_fan_control_thread) #added .after to allow above message to appear

    # system stats methods
    def system_stats_clicked(self):
        self.rb1.config(relief="raised", state="normal")
        self.rb2.config(relief="raised", state="normal")
        self.sys_stats_label.grid_forget()
        self.controller.system_stats_thread()
    def system_stats_message(self, message):
        self.gs.delete("1.0", tk.END)
        self.gs.insert("1.0", message)
        self.after(4000, self.controller.system_stats)

    # not condensed with pipe message because I want separate logic here to run the next iteration of auto fan
    def cpu_temp_message(self, message):
        self.ew.delete("1.0", tk.END)
        self.ew.insert(tk.END, message)
        if self.radio_button_selected == 1:
            return # ends auto fan thread here once manual fan control is selected and ~4 seconds have passed
        else:
            self.after(4000, self.controller.auto_fan_control) # run auto fan again on the same thread

    def pipe_message(self, message):
        # used for anything else accessing the error window aka 'ew'
        self.ew.delete("1.0", tk.END)
        self.ew.insert(tk.END, message)

    # system power management (4 buttons route here)
    def power_mode_button_clicked(self, selected_power_mode, human_var):
        self.human_var, self.selected_power_mode = human_var, selected_power_mode
        self.pipe_message(f"Power setting: {self.human_var} selected. Enabling...")
        # call controller thread method and pass in desired controller method and the var used to issue command
        self.controller.one_thread_to_rule_them_all(self.controller.power_mode, self.selected_power_mode)

    # pci-e cooling management (2 buttons route here)
    def pci_button_clicked(self, system_pci_fan_control, human_var):
        self.human_var, self.system_pci_fan_control = human_var, system_pci_fan_control
        self.pipe_message(f"PCI-E settings: {self.human_var} selected. Enabling...")
        self.controller.one_thread_to_rule_them_all(self.controller.pci_mode, self.system_pci_fan_control)

    # default or user fan control (2 buttons route here)
    def system_fan_control_clicked(self, system_manual_fan_control, human_var):
        self.human_var, self.system_manual_fan_control = human_var, system_manual_fan_control
        self.pipe_message(f"System Fan profile: {self.human_var} selected. Enabling...")
        self.controller.one_thread_to_rule_them_all(self.controller.fan_mode, self.system_manual_fan_control)

    # manual fan speed controls (8 buttons route here)
    def manual_fan_speed_clicked(self, fan_speed_var, human_var):
        self.human_var, self.fan_speed_var = human_var, fan_speed_var
        self.pipe_message(f"Fans manually commanded to {self.human_var} rpm.")
        self.controller.one_thread_to_rule_them_all(self.controller.fan_speed, self.fan_speed_var)

if __name__ == "__main__":
    main()
