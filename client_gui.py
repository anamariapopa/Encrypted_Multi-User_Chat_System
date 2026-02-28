import customtkinter as ctk
from tkinter import messagebox
from client_module import connect_to_server, send_message, set_message_callback

#setting theme and appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#chat window
class ChatWindow(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        self.title(f"Encrypted Chat – {username}")
        self.geometry("600x500")

        #main frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        #scrollable message zone
        self.textbox = ctk.CTkTextbox(self, wrap="word", state="disabled", font=("Arial", 14))
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        #input + button zone
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(bottom_frame, placeholder_text="Write a message...", font=("Arial", 14))
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0,10))

        self.send_btn = ctk.CTkButton(bottom_frame, text="Send", command=self.send_msg)
        self.send_btn.grid(row=0, column=1)

        #callback for received messages
        set_message_callback(self.display_message)

    def send_msg(self):
        msg = self.entry.get().strip()
        if msg:
            send_message(msg)
            self.entry.delete(0, "end")

    def display_message(self, msg):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", msg + "\n")
        self.textbox.configure(state="disabled")
        self.textbox.see("end")


#login window
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Conectare Chat Criptat")
        self.geometry("400x300")
        self.resizable(False, False)

        #layout
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Chat Criptat", font=("Arial", 28))
        title.grid(row=0, column=0, pady=20)

        self.ip_entry = ctk.CTkEntry(self, placeholder_text="IP server", font=("Arial", 14))
        self.ip_entry.grid(row=1, column=0, padx=40, pady=10, sticky="ew")

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username", font=("Arial", 14))
        self.user_entry.grid(row=2, column=0, padx=40, pady=10, sticky="ew")

        self.connect_btn = ctk.CTkButton(self, text="Connect", command=self.connect_action)
        self.connect_btn.grid(row=3, column=0, pady=20)

    def connect_action(self):
        ip = self.ip_entry.get().strip()
        username = self.user_entry.get().strip()

        if not ip or not username:
            messagebox.showerror("Error", "Enter IP and Username")
            return

        try:
            ok = connect_to_server(ip, username)
            if ok:
                self.destroy()
                chat = ChatWindow(username)
                chat.mainloop()
        except Exception as e:
            messagebox.showerror("Connection error", f"Can't connect\n{e}")



if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
