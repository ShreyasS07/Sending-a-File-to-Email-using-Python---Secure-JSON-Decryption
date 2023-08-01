import os
import json
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import subprocess
import loadME as me


selected_file = ""
generated_otp = ""
email_ids = []



def browse_file():
    global selected_file
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        selected_file = file_path
        file_status_var.set("Selected file: " + file_path)
    else:
        file_status_var.set("No file selected")


def generate_otp():
    letters = random.choices(string.ascii_uppercase, k=3)
    numbers = random.choices(string.digits, k=3)
    otp = ''.join(random.sample(letters + numbers, len(letters + numbers)))
    return otp

def send_otp():
    global generated_otp, email_ids
    email_ids = ["shreyas07.in@gmail.com", "roshanbhitkar18@gmail.com"]

    # Create OTP
    generated_otp = generate_otp()
    print("OTP", generated_otp)

    # Email configuration
    sender_email = "shreyas07.in@gmail.com"
    sender_password = "tktubtoynnuilkhy"

    # Gmail SMTP server and port
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        # Connecting to SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        for email_id in email_ids:
            # Creating email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email_id
            msg['Subject'] = "OTP for Decryption"

            # OTP msg
            body = f"Your OTP to Decrypt the selected file is: {generated_otp}"
            msg.attach(MIMEText(body, 'plain'))
            # Send Mail
            server.sendmail(sender_email, email_id, msg.as_string())
        # Close connection
        server.quit()

        print("OTP sent successfully!")
        otp_status_var.set("OTP sent successfully! Check your Inbox.")
    except Exception as e:
        print("Failed to send OTP:", e)
        otp_status_var.set("Failed to send OTP")





def enter_OTP(event):
    entered_otp = otp_entry.get()
    if entered_otp == "Enter OTP":
        otp_entry.delete(0, 'end')  # Clear the default text

def leave_OTP(event):
    entered_otp = otp_entry.get()
    if not entered_otp:
        otp_entry.insert(0, "Enter OTP")


def View_file():
    global selected_file
    if selected_file:
        try:
            with open(selected_file, 'r') as file:
                json_content = json.load(file)

            # with open(selected_file, 'r') as file:
            #     json_content = json.load(file)
            # status, decrypted_data = me.runME('decrypt', json_content)

            view_window = tk.Toplevel(root)
            view_window.title("JSON File")

            # Text box to display the JSON
            content_text = tk.Text(view_window, width=80, height=20, wrap='none', state='disabled')
            content_text.pack(padx=10, pady=10)
            content_text.config(state='normal')
            content_text.insert('end', json.dumps(json_content, indent=4))
            # content_text.insert('end', json.dumps(decrypted_data, indent=4))
            content_text.config(state='disabled')

            view_window.mainloop()
            file_status_var.set("File selected: " + selected_file)
        except Exception as e:
            file_status_var.set("Error while reading JSON file")
    else:
        file_status_var.set("No file selected")



def decrypt_send():
    global selected_file, generated_otp, email_ids
    entered_otp = otp_entry.get()
    print("Sent OTP", generated_otp)
    print("Received OTP", entered_otp)

    if generated_otp == entered_otp:
        print("OTP matched")
        if selected_file:
            try:
                # JSON data from the selected file
                with open(selected_file, 'r') as file:
                    encrypted_data = json.load(file)

                # Decrypt the JSON content using the decryption logic
                status, decrypted_data = me.runME('decrypt', encrypted_data)

                if status == 'success':
                    # Email configuration
                    print("Decrypted JSON")
                    # print(decrypted_data)
                    print(json.dumps(decrypted_data, indent=4))
                    sender_email = "shreyas07.in@gmail.com"
                    sender_password = "tktubtoynnuilkhy"

                    # Gmail server
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587

                    # Connect to the SMTP server
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(sender_email, sender_password)

                    for email_id in email_ids:
                        # Create the email message
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = email_id
                        msg['Subject'] = "Decrypted JSON file"

                        # JSON message
                        # body = json.dumps(decrypted_data, indent=4)      # JSON as text msg
                        body = "Please find the decrypted JSON file attached."
                        msg.attach(MIMEText(body, 'plain'))

                        # Attach the final JSON file
                        decrypted_file_name = os.path.splitext(os.path.basename(selected_file))[0] + ".json"
                        attachment = MIMEApplication(json.dumps(decrypted_data, indent=4))
                        attachment.add_header('Content-Disposition', 'attachment', filename=decrypted_file_name)
                        msg.attach(attachment)

                        # Send the email
                        server.sendmail(sender_email, email_id, msg.as_string())

                    # Close connection
                    server.quit()

                    print("Decrypted JSON file successfully!")
                    otp_status_var.set("Decrypted JSON sent successfully!")
                else:
                    print("Decryption failed.")
                    otp_status_var.set("Decryption failed.")
            except Exception as e:
                print("Error while reading or decrypting JSON file:", e)
                otp_status_var.set("Error while reading or decrypting JSON file.")
        else:
            print("No file selected.")
            otp_status_var.set("No file selected.")
    else:
        print("Entered OTP does not match the generated OTP.")
        otp_status_var.set("Entered OTP does not match the generated OTP.")





root = tk.Tk()
root.title("Mindful Automation Pvt Ltd")
root.geometry("645x220")
root['bg'] = 'white'
current_path = os.path.dirname(os.path.realpath(__file__))
root.wm_iconbitmap(f"{current_path}/icons/mindful_logo.ico")

file_status_var = tk.StringVar()
otp_status_var = tk.StringVar()

# label = tk.Label(root, text="DECRYPTER", width=40, height=3, fg="#03001C", font=('Arial', 10, 'bold'))
# label.grid(column=2, row=1  columnspan=3)
label = tk.Label(root, text="DECRYPTER", width=40, height=3, fg="#03001C", font=('Arial', 10, 'bold'))
label.grid(column=1, row=1, columnspan=3, sticky='news')
style = ttk.Style()
style.configure('TLabel', background=root['bg'])

file_status_label = tk.Label(root, textvariable=file_status_var, fg="#006400")
file_status_label.grid(column=1, row=2, columnspan=3, pady=0, sticky='news')
otp_status_label = tk.Label(root, textvariable=otp_status_var, fg="#006400")
otp_status_label.grid(column=1, row=3, columnspan=3, pady=0, sticky='news')

browse = tk.Button(root, text="BROWSE FILE", command=browse_file, height=1, width=30)
browse.grid(column=1, row=4, pady=10)
otp = tk.Button(root, text="SEND OTP", command=send_otp, height=1, width=30)
otp.grid(column=2, row=4, pady=10)

# Entry widget for entering OTP
otp_entry = tk.Entry(root, width=33)
otp_entry.insert(0, "Enter OTP")
otp_entry.grid(column=3, row=4, pady=10)
otp_entry.bind("<FocusIn>", enter_OTP)
otp_entry.bind("<FocusOut>", leave_OTP)

view = tk.Button(root, text="VIEW", command=View_file, height=1, width=30)
view.grid(column=1, row=5, pady=10)
send = tk.Button(root, text="DECRYPT & SEND", command=decrypt_send, height=1, width=30)
send.grid(column=2, row=5, pady=10)
root.mainloop()

