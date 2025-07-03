import customtkinter as ctk
import requests

GEMINI_API_URL='https://generativelanguage.googleapis.com/vlbeta/models/gemini-1.5-flash:generateContent'
GEMINI_API_KEY='AIzaSyCe8wGOlzFo62W-Y3MkmosVaXZbT9m9zbA'

def get_gemini_response(user_message):
    headers={
        'Content-Type':'application/json',
    }
    data ={
        'contents':[
            {'parts':[{"text":user_message}]}
        ]
    }
    params={
        'key': GEMINI_API_KEY
    }
    try:
        response= requests.post(GEMINI_API_URL,headers=headers,params=params, json=data)
        response.raise_for_status()
        result=response.json()
        #Extract the responce text
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error:{e}"
    
class GeminiChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gemini Chatbot (Advanced UI)")
        self.geometry("800x600")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.minsize(700, 500)

        #layout: Sidebar | Main area
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Sidebar
        self.sidebar= ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(2, weight=1)
        self.sidebar_label=ctk.CTkLabel(self.sidebar,text="Gemini\nChatbot",font=ctk.CTkFont(size=20, weight="bold"), justify="left")
        self.sidebar_label.grid(row=0, column=0,padx=20, pady=(30,10), sticky="w")
        self.clear_button= ctk.CTkButton(self.sidebar,text="Clear Chat", command=self.clear_chat, fg_color="#FF5C5C", hover_color="#FF1C1C")
        self.clear_button.grid(row=1, column=0, padx=20,pady=(10,0), sticky="ew")
        #Placeholder for future freatures
        self.sidebar_footer= ctk.CTkLabel(self.sidebar, text="\nSettings\nHistory\n", font=ctk.CTkFont(size=12), text_color="#888")
        self.sidebar_footer.grid(row=2, column=0, padx=20, pady=(0,20), sticky="sw")

        #Main Area
        self.main_frame=ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        #Title bar
        self.title_label= ctk.CTkLabel(self.main_frame, text="Gemini Chatbox", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(15,5))
        #chat area (scrollable frame)
        self.chat_canvas=ctk.CTkCanvas(self.main_frame, bg="#F0F4F8", highlightthickness=0)
        self.chat_scrollbar=ctk.CTkScrollbar(self.main_frame, orientation="vertical", command=self.chat_canvas.yview)
        self.chat_frame= ctk.CTkFrame(self.chat_canvas, fg_color="#F0F4F8")
        self.chat_frame.bind(
             "<Configure>",lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        self.chat_canvas.grid(row=1, column=0, sticky="nsew", padx=(20,0), pady=(0,10))
        self.chat_scrollbar.grid(row=1, column=1, sticky="ns", pady=(0,10))
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

         # Input Area
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="#E8EAF6")
        self.input_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.entry = ctk.CTkEntry(self.input_frame, width=500, placeholder_text="Type your message...")
        self.entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.entry.bind('<Return>', self.send_message)
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message, width=100)
        self.send_button.grid(row=0, column=1, padx=(5, 10), pady=10)

        self.messages = []  # Store messages for alternating bubbles

    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        if not user_message:
               return
        self.add_message(user_message, sender="user")
        self.entry.delete(0, ctk.END)
        self.after(100, self.get_bot_response, user_message)

    def get_bot_response(self, user_message):
        bot_response = get_gemini_response(user_message)
        self.add_message(bot_response, sender="bot")

    def add_message(self, message, sender="user"):
        bubble_color = "#1976D2" if sender == "user" else "#E3F2FD"
        text_color = "#fff" if sender == "user" else "#222"
        anchor = "e" if sender == "user" else "w"
        padx = (80, 10) if sender == "user" else (10, 80)
        bubble = ctk.CTkLabel(self.chat_frame, text=message, fg_color=bubble_color, text_color=text_color,
                              font=ctk.CTkFont(size=15), corner_radius=15, justify="left", wraplength=400, anchor=anchor, padx=15, pady=10)
        bubble.pack(anchor=anchor, padx=padx, pady=5, fill="none")
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
        self.messages.append((message, sender))

    def clear_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.messages.clear()

if __name__ == "__main__":
    app = GeminiChatbotApp()
    app.mainloop()
