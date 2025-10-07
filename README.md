# Homelab_IPMI_Tool

I believe this is now a Beta release of the software. 

This is a simple GUI tool that allows for IPMI based management of a Dell R730XD in a homelab. 

Rather than being required to copy and paste IPMI commands to the terminal, you can control the server with a button press.

This utility may work for other Dell server models. 

![Image](https://github.com/user-attachments/assets/1aab9510-3c8d-4770-acc5-3228ecf5c5cb)

#

Verified to work with Ubuntu 24.04LTS and Mac OS 15.3.2 - 15.6.1

#

Test system: R730XD with BIOS version 2.19.0 and iDRAC version 2.86.86 (Build 6) and contains an "un-approved" Gigabyte RTX2070 GPU (relevant below)

Should be compatible with all 13th gen Dell servers (and possibly 12th and 11th gen) so R730, R720, R710, etc.

#

Requires the following dependancies:

- Python 3.12.3
- Python3-tk
- tkinter-tooltip
- IPMItool - Version 1.8.19 found [here.](https://github.com/ipmitool/ipmitool)
- FreeIPMI - Version 1.6.13 found [here.](https://www.gnu.org/software/freeipmi/)
- IDRAC Credentials
- IP Address of your server



# 

Now for some "light" reading. 

First and foremost, please be secure.

Please follow security conventions and place your BMC on a management VLAN that is not internet accessible. A managed switch is $40. Please help combat botnets and spam by securing your equipment. IPMI does NOT give robust protections to credentials. Please see this [CVE](https://www.cvedetails.com/cve/CVE-2013-4786/) . 

I created this application as a standalone tool for this reason. If you are airgapped, this is perfect. I am also not a fan of web based tools(at this time). Memory footprint is 16.5mb on my system. 

#

All commands issued by this utility are reversible. I have also included a text file with all commands that I have found through posts, forums, ones I have used, found in documentation or experimented with. I have also included real outputs, except where serial numbers or PII may exist. 

The commands in this tool are in that document, as well as in the code. Previous versions of this tool contain, essentially, plain text versions of the commands prior to going OOP and condensing things. 

By default, fan control is not able to be controlled by the user. 

If an "un-approved" GPU is added to the system, fan speed is also defaulted to 100% as a protection measure to provide the server max cooling. Noise and power draw are not really concerns in a data center, but they certainly are in your home.

#


# Instructions:

Enter credentials. No safety checks for credentials have been programmed (yet), so incorrect values will be entered for use and return an error when commands are issued. If you mistype, that is okay. New credentials can be "saved" without ending the program. No passwords or information persists between uses in this application, nor will I ever program that. Maybe nicknames and IP's at some point, but never credentials. 

On first use, if no IPMI commands or state changes have been previously made to your server, fan control will NOT work. To enable full manual fan control (and then my auto fan control and its temp curve, if you desire), please select:

- Power On - (if system is not on)
- System Stats
- Default Dell PCI-E Profile Off - turns off max fan speed for unapproved GPU's 
- User Fan Control On - Allows the tool to issue commands on your behalf
- Select Manual Fans and a fan speed or Auto Fans for automatic temperature control


After first use:
- Query Power Status or just issue Power On
- Select System Stats
- Select Auto Fans

Done. 



# More important information:

Default Dell PCI-E Profile Off - this state persists, even after a shutdown. It does not need to be re-issued each time the tool is used. State does not persist after power is removed. 

User Fan Control On - this state persists, even after a shutdown. It does not need to be re-issued each time the tool is used. State does not persist after power is removed. 

If you close the application or if it crashes while in use and the server is still on:

The last issued fan speed is what the system will remain at. Please ensure iDRAC is configured correctly for a max temp power down. 


#

Current Development:


Please bear with me as I upload additional documentation, features and bug fixes. 

Ultimate project goal: Allow user defined profiles for any server managed via IPMI. I know some have far more than just 1 server. 


#

# DISCLAIMER

This software NOT officially licensed and you are accepting any responsibility for damage that may be caused through its use. Please monitor your equipment.

Also, I am not affiliated with, do not work for, or have any contact with Dell in ANY capacity. 

Names, trademarks, copyrights, and anything else that may be owned by someone who is not myself are property of their respective owners. 
