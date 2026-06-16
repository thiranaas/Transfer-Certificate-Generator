import customtkinter as ctk
from PIL import Image, ImageTk
import csv
from reportlab.pdfgen.canvas import Canvas
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

d = {}
def tc():
    global d

    def collect_input():
        global d
        # Collect data from form entries
        admission_no = d["Admission No"].get()
        promoted_to = d["Promoted to"].get()
        fees_concession = d["Fees concession"].get()
        date_of_application = d["Date of application"].get()
        date_of_issue = d["Date of issue"].get()
        reason_for_leaving = d["Reason for leaving"].get()

        f=open('Data.csv','r')
        r=list(csv.reader(f))
        for i in r[4:]:
            if  i[4]== admission_no:
                found = True
                break
        else:
            found=False
        f.close()

        if not found:
             messagebox.showinfo('Error', 'Admission number doesn\'t match.')
             # Clear all entry fields
             for entry in d.values():
                 entry.delete(0, ctk.END)
        else:
            # Save the request with 'Pending' approval status
            f=open('Pending_TCs.csv','a',newline='')
            wr=csv.writer(f)
            wr.writerow([admission_no, promoted_to, fees_concession, date_of_application, date_of_issue, reason_for_leaving, "Pending"])
            f.close()

            # Inform the user
            messagebox.showinfo("Success", "Transfer Certificate request submitted for approval.")
            w.destroy()
            mainpage1()

    # Create CustomTkinter window
    w = ctk.CTk()
    w.title("TC Generator")
    w.geometry('800x500')
    w.configure(bg='#4CCD99')  # Set a light grey background

    # Title label
    label = ctk.CTkLabel(w, text="TC Generator", font=("Helvetica", 24, "bold"), text_color="#333333")
    label.grid(row=0, column=1, columnspan=2, padx=50, pady=20)

    # Define label and entry pairs in a list
    d = {}.fromkeys(["Admission No", "Promoted to", "Fees concession", "Date of application", "Date of issue", "Reason for leaving"], None)
    i = 1
    for x in d:
        ctk.CTkLabel(w, text=x, font=('Helvetica', 16), text_color="#1E201E").grid(row=i, column=1, padx=10, pady=10, sticky='e')
        d[x] = ctk.CTkEntry(w, border_color="#4A90E2", fg_color="#FFFFFF")
        d[x].grid(row=i, column=2, padx=10, pady=10, sticky='w')
        i += 1

    # Submit button
    ctk.CTkButton(w, text='Submit', command=collect_input, fg_color="#FF6347", hover_color="#FF4500", text_color="#FFFFFF", font=("Helvetica", 16, "bold")).grid(row=i, column=1, columnspan=2, pady=20)

    w.mainloop()

# Principal approves or rejects the TC request
def principal_approve(main_page_callback,mainpage2):
    def load_pending_requests():
        # Load pending TC requests from CSV
        with open('Pending_TCs.csv', 'r') as f:
            pending_requests = list(csv.reader(f))
        return pending_requests

    def save_requests_to_file(requests):
        # Save updated requests back to CSV
        with open('Pending_TCs.csv', 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerows(requests)

    def approve_tc(admission_no, info_label, approve_button, reject_button):
        # Update CSV to mark as approved
        with open('Pending_TCs.csv', 'r') as f:
            requests = list(csv.reader(f))

        # Find the request and mark it as approved
        for i in range(len(requests)):
            if requests[i][0] == admission_no:
                requests[i][-1] = "Approved"  # Update status to "Approved"
                with open('Data.csv', 'r') as f:
                    r = list(csv.reader(f))
                    for j in r[4:]:
                        if j[4] == admission_no:
                            found = True
                            break
                create_pdf(requests[i], j)  # Generate the PDF

        # Remove the approved request from the pending requests
        requests = [req for req in requests if req[0] != admission_no]
        save_requests_to_file(requests)  # Save the updated requests

        with open('Data.csv','r+',newline='') as f1:
            r=list(csv.reader(f1))
            for i in r:
                if i[4]==admission_no:
                    r.remove(i)
                    break
            f1.close()
            
        # Remove the request from the UI
        info_label.pack_forget()
        approve_button.pack_forget()
        reject_button.pack_forget()

        with open('Data.csv','w',newline='') as f1:
            w=csv.writer(f1)
            w.writerows(r)
            f1.close()

        messagebox.showinfo("Success", f"Transfer Certificate for Admission No: {admission_no} approved and generated.")

    def reject_tc(admission_no, info_label, approve_button, reject_button):
        # Update CSV to remove rejected request
        with open('Pending_TCs.csv', 'r') as f:
            requests = list(csv.reader(f))

        # Remove the rejected request
        requests = [req for req in requests if req[0] != admission_no]
        save_requests_to_file(requests)  # Save the updated requests

        # Remove the request from the UI
        info_label.pack_forget()
        approve_button.pack_forget()
        reject_button.pack_forget()

        messagebox.showinfo("Rejected", f"Transfer Certificate for Admission No: {admission_no} rejected.")

    # Create a window for principal approval
    w = ctk.CTk()
    w.title("Principal Approval")
    w.geometry('800x500')

    # Styling similar to the screenshot (gray background, dark fonts)
    w.configure(bg='#E6E6E6')  # Light gray background

    label = ctk.CTkLabel(w, text="Pending TC Requests", font=("Helvetica", 24, "bold"), text_color="#000000")
    label.pack(padx=20, pady=20)

    pending_requests = load_pending_requests()
    if not pending_requests:
        label = ctk.CTkLabel(w, text="No pending requests", font=("Helvetica", 16), text_color="#000000")
        label.pack(padx=10, pady=10)
    else:
        for request in pending_requests:
            admission_no = request[0]
            info_label = ctk.CTkLabel(w, text=f"Admission No: {admission_no}, Status: {request[-1]}", font=("Helvetica", 16), text_color="#000000")
            info_label.pack(padx=10, pady=10)

            # Create buttons (without lambda at first)
            approve_button = ctk.CTkButton(w, text="Approve", fg_color="#5cb85c")
            reject_button = ctk.CTkButton(w, text="Reject", fg_color="#d9534f")

            # Assign the command after the button is created
            approve_button.configure(command=lambda ad_no=admission_no, label=info_label, abtn=approve_button, rbtn=reject_button: approve_tc(ad_no, label, abtn, rbtn))
            reject_button.configure(command=lambda ad_no=admission_no, label=info_label, abtn=approve_button, rbtn=reject_button: reject_tc(ad_no, label, abtn, rbtn))

            # Pack the buttons after configuring their commands
            approve_button.pack(padx=10, pady=10)
            reject_button.pack(padx=10, pady=10)

    # Add a "Return to Main Page" button
    return_button = ctk.CTkButton(w, text="Return to Main Page", fg_color="#f0ad4e", command=lambda: [w.destroy(), mainpage2()])
    return_button.pack(padx=20, pady=20)

    w.mainloop()

def create_pdf(d,data):
    admission_no, promoted_to, fees_concession, date_of_application, date_of_issue, reason_for_leaving, _ = d
    school_info = {"name": "D.A.V. PUBLIC SCHOOL, VELACHERY", "address": "19, Sitaram Nagar, Velachery, Chennai - 42", "code": "123456"}
    
   # Define the PDF file name
    file_name = f"{data[0]}_Transfer_Certificate.pdf"

    # Create the PDF document
    pdf = SimpleDocTemplate(file_name, pagesize=A4)
    elements = []

    # Load the styles
    styles = getSampleStyleSheet()
    
    # Custom style for Times New Roman font
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontName='Times-Roman', fontSize=16, alignment=1)
    sub_title_style = ParagraphStyle('Normal', parent=styles['Normal'], fontName='Times-Roman', fontSize=12, alignment=1)
    normal_style = ParagraphStyle('Normal',parent=styles['Normal'], fontName='Times-Roman', fontSize=12, alignment=4)

     # Add the school logo
    logo_path="images/school logo.jfif"
    logo = Image(logo_path)
    logo.drawHeight=1*inch
    logo.drawWidth=1*inch
    logo.hAlign='CENTRE'
    elements.append(logo)

    # School Header
    elements.append(Paragraph(school_info['name'], title_style))
    elements.append(Paragraph(school_info['address'], sub_title_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("Transfer Certificate", title_style))
    elements.append(Spacer(1, 0.5 * inch))
    
    # Student Information Section
    student_info = [
        ["Name Of Student:", data[0]],
        ["Father/Guardian's Name:", data[1]],
        ["Mother’s Name:", data[2]],
        ["Nationality:", data[3]],
        ["Student Admission No.:", data[4]],
        ["Class in which the student last studied:", data[5]],
        ["Subjects studied:", data[6].replace('\'','')],
        ["To which class is he/she qualified:", promoted_to],
        ["Any fees concession availed (if so nature of concession):", fees_concession],
        ["Date of Application for Certificate:", date_of_application],
        ["Date of issue of Certificate:", date_of_issue],
        ["Reasons for leaving the School:", reason_for_leaving],
    ]

    for item in student_info:
        elements.append(Paragraph(f"{item[0]} {item[1]}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

    # Footer
    footer_data = [
        ["Signature of class teacher", "Signature of Principal", "School Seal"],
        ["_____________________", "_____________________", "_____________________"]
    ]

    footer_table = Table(footer_data, colWidths=[2.5 * inch, 2.5 * inch, 2.5 * inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
    ]))

    elements.append(footer_table)

     # Add the formal border using canvas
    def add_border(c, doc):
        width, height = A4
        c.saveState()
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(30, 30, width - 60, height - 60)  # Rectangle for formal border
        c.restoreState()

    # Build the PDF
    pdf.build(elements, onFirstPage=add_border)
    print(f"Transfer Certificate generated successfully: {file_name}")

def mainpage1():
    def open_tc_generator():
        w.destroy()
        tc()

    def logout():
        w.destroy()
        userlogin()

    w = ctk.CTk()
    w.title("Main page")
    w.geometry("800x500")
    w.configure(bg='#FFCEFE')  # Set a light grey background

    tc_button = ctk.CTkButton(w, text="TC Generator", command=open_tc_generator, font=('Helvetica', 16, "bold"), fg_color="#32CD32", hover_color="#228B22", text_color="#FFFFFF")
    tc_button.pack(padx=10, pady=20)

    logout_button = ctk.CTkButton(w, text="Logout", command=logout, font=('Helvetica', 16, "bold"), fg_color="#FF6347", hover_color="#FF4500", text_color="#FFFFFF")
    logout_button.pack(padx=10, pady=20)

    w.mainloop()

def mainpage2():
    def open_tc_approval():
        w.destroy()
        principal_approve(main_page_callback=mainpage2, mainpage2=mainpage2)
        
    def logout():
        w.destroy()
        userlogin()
    w=ctk.CTk()
    w.title('Main page')
    w.geometry("800x500")
    w.configure(bg='#FFCEFE')  # Set a light grey background

    approval_button = ctk.CTkButton(w, text="Approval", command=open_tc_approval, font=('Helvetica', 16, "bold"), fg_color="#32CD32", hover_color="#228B22", text_color="#FFFFFF")
    approval_button.pack(padx=10, pady=20)

    logout_button = ctk.CTkButton(w, text="Logout", command=logout, font=('Helvetica', 16, "bold"), fg_color="#FF6347", hover_color="#FF4500", text_color="#FFFFFF")
    logout_button.pack(padx=10, pady=20)

    w.mainloop()   

def userlogin():
    def collect_input():
        f = open('Data.csv', 'r')
        username = username_entry.get()
        password = password_entry.get()
        data = list(csv.reader(f))
        if username == data[1][0] and password == data[1][1]:
            w.destroy()
            mainpage1()
        elif username == data[2][0] and password == data[2][1]:
            w.destroy()
            mainpage2()
        else:
            messagebox.showerror("Login error", "Invalid username or password")
            username_entry.delete(0, ctk.END)
            password_entry.delete(0, ctk.END)
        f.close()

    def reset_password():
        w.destroy()

        def update_password():
            f = open('Data.csv', 'r')
            data = list(csv.reader(f))
            new_password = new_password_entry.get()
            if username_entry.get() == data[1][0]:
                if new_password == confirm_password_entry.get():
                    data[1][1] = new_password
                    messagebox.showinfo("Success", "Password has been reset successfully.")
                    reset_w.destroy()
                    userlogin()
                else:
                    messagebox.showerror("Error", "Passwords do not match.")
                    new_password_entry.delete(0, ctk.END)
                    confirm_password_entry.delete(0, ctk.END)
            elif username_entry.get() == data[2][0]:
                if new_password == confirm_password_entry.get():
                    data[2][1] = new_password
                    messagebox.showinfo("Success", "Password has been reset successfully.")
                    reset_w.destroy()
                    userlogin()
                else:
                    messagebox.showerror("Error", "Passwords do not match.")
                    new_password_entry.delete(0, ctk.END)
                    confirm_password_entry.delete(0, ctk.END)
            else:
                messagebox.showerror("Reset password error", "Invalid username")
                username_entry.delete(0, ctk.END)
                new_password_entry.delete(0, ctk.END)
            f.close()

            f = open('Data.csv', 'w', newline='')
            w = csv.writer(f)
            w.writerows(data)
            f.close()

        reset_w = ctk.CTk()
        reset_w.title("Reset password")
        reset_w.geometry("800x500")

        # Set the background color
        reset_w.configure(fg_color='#FFCEFE')

        label = ctk.CTkLabel(reset_w, text="Reset password", font=("Comic Sans MS", 24, "bold"), text_color="#10439F")
        label.pack(padx=50, pady=25)

        label = ctk.CTkLabel(reset_w, text="Username", font=("Comic Sans MS", 16), text_color="#10439F")
        label.pack(padx=10, pady=5)
        username_entry = ctk.CTkEntry(reset_w, border_color="#4A90E2", fg_color="#FFFFFF")
        username_entry.pack(padx=10, pady=5)

        label = ctk.CTkLabel(reset_w, text="New Password", font=("Comic Sans MS", 16), text_color="#10439F")
        label.pack(padx=10, pady=5)
        new_password_entry = ctk.CTkEntry(reset_w, border_color="#4A90E2", fg_color="#FFFFFF")
        new_password_entry.pack(padx=10, pady=5)

        label = ctk.CTkLabel(reset_w, text="Confirm Password", font=("Comic Sans MS", 16), text_color="#10439F")
        label.pack(padx=10, pady=5)
        confirm_password_entry = ctk.CTkEntry(reset_w, border_color="#4A90E2", fg_color="#FFFFFF")
        confirm_password_entry.pack(padx=10, pady=5)

        submit_button = ctk.CTkButton(reset_w, text="Submit", command=update_password, fg_color="#E3ACF9", hover_color="#E3ACF9", text_color="#10439F", font=("Comic Sans MS", 16, "bold"))
        submit_button.pack(padx=10, pady=20)

        reset_w.mainloop()

    w = ctk.CTk()
    w.title("User Login")
    w.geometry("800x500")

    # Set the correct background color
    bg_color = "#FFCEFE"  # Light red background
    form_bg_color = "#E3ACF9"  # Darker grey area for the form

    w.configure(fg_color=bg_color)

    # Create a frame for the form background
    form_frame = ctk.CTkFrame(w, width=600, height=300, corner_radius=20, fg_color=form_bg_color)
    form_frame.pack(pady=200)

    # Title label
    label = ctk.CTkLabel(w, text="Login", font=("Comic Sans MS", 24, "bold"), text_color="#10439F")
    label.place(relx=0.5, rely=0.15, anchor="center")

    # Username label and entry
    username_entry = ctk.CTkEntry(w, placeholder_text="Username", font=("Comic Sans MS", 16), width=250)
    username_entry.place(relx=0.5, rely=0.45, anchor="center")

    # Password label and entry
    password_entry = ctk.CTkEntry(w, show="*", placeholder_text="Password", font=("Comic Sans MS", 16), width=250)
    password_entry.place(relx=0.5, rely=0.55, anchor="center")

    # Submit button
    submit_button = ctk.CTkButton(w, text="Login", command=collect_input, fg_color="#C780FA", hover_color="#C780FA", text_color="#10439F", font=("Comic Sans MS", 16, "bold"))
    submit_button.place(relx=0.5, rely=0.7, anchor="center")

    # Reset Password button
    reset_button = ctk.CTkButton(w, text="Reset Password", command=reset_password, fg_color="#C780FA", hover_color="#C780FA", text_color="#10439F", font=("Comic Sans MS", 16, "bold"))
    reset_button.place(relx=0.5, rely=0.8, anchor="center")

    w.mainloop()


userlogin()








