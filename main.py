import customtkinter as ctk
from PIL import Image, ImageTk
import os
from datetime import datetime
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tkinter import filedialog

load_dotenv()

model = ChatOpenAI(model="gpt-4o")

server_params = StdioServerParameters(
    command="python",
    args=["server.py"]
)

colors = {
    "black": "#121212",
    "blue": "#007BFF",
    "purple": "#8A2BE2",
    "charcoal": "#1E1E2E",
    "lavender": "#C084FC"
}

async def run_agent(prompt):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools=await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke(
                {"messages":prompt}
            )
            return agent_response["messages"][-1].content

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Dashboard")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True)
        
        self.sidebar_visible = True
        self.create_sidebar()  # Left sidebar - Navigation (1/5)
        self.create_main_section()  # Middle - Main content (3/5)
        self.create_chatbot()  # Right - AI Chatbot (1/5)

    def create_sidebar(self):
        # Left sidebar for navigation (1/5 of screen)
        self.sidebar_frame = ctk.CTkFrame(self.main_container, width=240, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y", expand=False)
        
        # App Logo/Title
        self.greeting_text = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Clarus", 
            font=("Tahoma", 35, "bold"),
            text_color=colors["lavender"]
        )
        self.greeting_text.pack()
        
        # Navigation buttons
        self.nav_buttons = []
        nav_items = [
            ("Dashboard", "home")
        ]
        
        for text, page in nav_items:
            button = ctk.CTkButton(
                self.sidebar_frame, 
                text=text, 
                fg_color="transparent", 
                text_color=("gray10", "gray90"),
                anchor="w",
                height=50,
                font=("Tahoma", 12),
                command=lambda p=page: self.navigate_to(p)
            )
            button.pack(fill="x", padx=20, pady=5)
            self.nav_buttons.append(button)
        
        # Highlight current page (Dashboard by default)
        self.nav_buttons[0].configure(fg_color=("gray75", "gray25"))
        self.current_page = "home"
        
        # User profile at bottom
        self.sidebar_frame.pack_propagate(False)
        
        # Bottom section for user profile
        self.user_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.user_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.user_label = ctk.CTkLabel(self.user_frame, text="John Doe", font=("Arial", 14, "bold"))
        self.user_label.pack(anchor="w")
        
        self.role_label = ctk.CTkLabel(self.user_frame, text="Administrator", font=("Arial", 12))
        self.role_label.pack(anchor="w")
        
        self.settings_button = ctk.CTkButton(
            self.user_frame, 
            text="Settings", 
            fg_color="transparent",
            font=("Tahoma", 12),
            text_color=("gray10", "gray90"),
            width=100,
        )
        self.settings_button.pack(anchor="w", pady=(10, 0))

    def create_main_section(self):
        # Main content area (3/5 of screen)
        self.main_frame = ctk.CTkFrame(self.main_container)
        self.main_frame.pack(side="left", fill="both", expand=True)
        
        # Top bar with toggle button and title
        self.top_bar = ctk.CTkFrame(self.main_frame, height=60, fg_color=("#eeeeee", "#333333"))
        self.top_bar.pack(fill="x", expand=False)
        self.top_bar.pack_propagate(False)
        
        # Toggle sidebar button
        self.toggle_button = ctk.CTkButton(
            self.top_bar, 
            text="≡",
            width=40, 
            font=("Tahoma", 20),
            command=self.toggle_sidebar
        )
        self.toggle_button.pack(side="left", padx=15)
        
        # Current page title
        self.page_title = ctk.CTkLabel(
            self.top_bar, 
            text="Dashboard", 
            font=("Tahoma", 18, "bold")
        )
        self.page_title.pack(side="left", padx=15)
        
        # Current date/time on right
        self.datetime_label = ctk.CTkLabel(
            self.top_bar,
            text=datetime.now().strftime("%A, %d %B %Y"),
            font=("Tahoma", 14)
        )
        self.datetime_label.pack(side="right", padx=20)
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create different page contents (only dashboard is visible initially)
        self.pages = {}
        
        # Dashboard page
        self.pages["home"] = self.create_dashboard_page()
        
        # Analytics page (hidden initially)
        self.pages["analytics"] = self.create_analytics_page()
        self.pages["analytics"].pack_forget()
        
        # History page (hidden initially)
        self.pages["history"] = self.create_history_page()
        self.pages["history"].pack_forget()
        

    def create_dashboard_page(self):
        frame = ctk.CTkFrame(self.content_frame)
        frame.pack(fill="both", expand=True)

        # Generate a input field for the user to input the directory and a button to submit the directory
        directory_frame = ctk.CTkFrame(frame, fg_color="transparent")
        directory_frame.pack(fill="x", expand=True, padx=20, pady=20)

        # Store the entry widget as an instance variable so we can access it in submit_directory
        self.directory_input = ctk.CTkEntry(directory_frame, width=200)
        self.directory_input.pack(pady=10)

        # Add Choose Folder button
        choose_folder_button = ctk.CTkButton(
            directory_frame, 
            text="Choose Folder", 
            command=self.choose_folder,
            width=100
        )
        choose_folder_button.pack( pady=10)

        submit_button = ctk.CTkButton(directory_frame, text="Submit", command=self.submit_directory)
        submit_button.pack(pady=10)

        return frame

    def choose_folder(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.directory_input.delete(0, 'end')
            self.directory_input.insert(0, directory_path)
            
    def submit_directory(self):
        global directory_path
        directory_path = self.directory_input.get()
        print(f"Selected directory: {directory_path}")
        # Here you can add any additional processing for the selected directory

    def create_analytics_page(self):
        frame = ctk.CTkFrame(self.content_frame)
        
        label = ctk.CTkLabel(frame, text="Analytics Content", font=("Arial", 24, "bold"))
        label.pack(pady=100)
        
        subtitle = ctk.CTkLabel(frame, text="Analytics page coming soon...")
        subtitle.pack()
        
        return frame

    def create_history_page(self):
        frame = ctk.CTkFrame(self.content_frame)
        
        label = ctk.CTkLabel(frame, text="History Content", font=("Arial", 24, "bold"))
        label.pack(pady=100)
        
        subtitle = ctk.CTkLabel(frame, text="History page coming soon...")
        subtitle.pack()
        
        return frame

    def create_chatbot(self):
        # Right sidebar for AI chatbot (1/5 of screen)
        self.chatbot_frame = ctk.CTkFrame(self.main_container, width=290, corner_radius=0)
        self.chatbot_frame.pack(side="right", fill="y", expand=False)
        self.chatbot_frame.pack_propagate(False)
        
        # Chatbot header
        self.chatbot_header = ctk.CTkFrame(self.chatbot_frame, height=60, fg_color=("#eeeeee", "#333333"))
        self.chatbot_header.pack(fill="x", expand=False)
        self.chatbot_header.pack_propagate(False)
        
        self.chatbot_title = ctk.CTkLabel(
            self.chatbot_header, 
            text="AI Assistant", 
            font=("Tahoma", 16, "bold")
        )
        self.chatbot_title.pack(side="left", padx=15)
        
        # Chat messages area
        self.chat_area = ctk.CTkScrollableFrame(self.chatbot_frame)
        self.chat_area.pack(fill="both", expand=True, padx=9, pady=9)
        
        # Flag to track conversation state
        self.conversation_active = False
        
        # Show greeting initially
        self.show_greeting()
        
        # Input area
        self.input_frame = ctk.CTkFrame(self.chatbot_frame, height=80, fg_color="transparent")
        self.input_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        self.chat_input = ctk.CTkTextbox(self.input_frame, height=40)
        self.chat_input.pack(fill="x", side="left", expand=True, padx=(0, 5))
        
        self.send_button = ctk.CTkButton(
            self.input_frame, 
            text="Send",
            width=60,
            command=self.send_message,
            font=("Tahoma", 12)
        )
        self.send_button.pack(side="right")
        
        # Bind Enter key to send message
        self.chat_input.bind("<Return>", lambda event: self.send_message())

    def show_greeting(self):
        # Clear chat area first
        for widget in self.chat_area.winfo_children():
            widget.destroy()
            
        # Add welcome message
        greeting_frame = ctk.CTkFrame(self.chat_area, fg_color=("#4a7dff", "#3a66cc"))
        greeting_frame.pack(fill="x", pady=5, padx=(5, 40), anchor="w")
        
        greeting_label = ctk.CTkLabel(
            greeting_frame,
            text="Hello! I'm your AI assistant. How can I help you today?",
            text_color="white",
            font=("Tahoma", 12),
            justify="left",
            wraplength=180
        )
        greeting_label.pack(padx=10, pady=8)
        
        warning_label = ctk.CTkLabel(
            greeting_frame,
            text="Keep in mind I don't remember your previous requests",
            text_color="white",
            font=("Tahoma", 12),
            justify="left",
            wraplength=180
        )
        warning_label.pack(padx=10, pady=8)
        
        # Reset conversation state
        self.conversation_active = False

    def add_user_message(self, message):
        message_frame = ctk.CTkFrame(self.chat_area, fg_color=("#e0e0e0", "#555555"))
        message_frame.pack(fill="x", pady=5, padx=(40, 5), anchor="e")
        
        message_label = ctk.CTkLabel(
            message_frame, 
            text=message,
            justify="left",
            wraplength=180
        )
        message_label.pack(padx=10, pady=8)

    def add_bot_message(self, message):
        message_frame = ctk.CTkFrame(self.chat_area, fg_color=("#4a7dff", "#3a66cc"))
        message_frame.pack(fill="x", pady=5, padx=(5, 40), anchor="w")
        
        message_label = ctk.CTkLabel(
            message_frame, 
            text=message,
            text_color="white",
            justify="left",
            wraplength=180
        )
        message_label.pack(padx=10, pady=8)

    def send_message(self):
        message = self.chat_input.get("0.0", "end-1c").strip()
        if not message:
            return
            
        if self.conversation_active:
            self.show_greeting()
            self.root.after(100, lambda: self.continue_conversation(message))
        else:
            self.continue_conversation(message)
    
    def continue_conversation(self, message):
        global directory_path
        self.add_user_message(message)
        self.chat_input.delete("0.0", "end")
        
        self.conversation_active = True

        print(message)

        result = asyncio.run(run_agent(message + " in " + directory_path))
        print(result)
                
        self.root.after(500, lambda: self.add_bot_message(result))

    def navigate_to(self, page):
        for p in self.pages.values():
            p.pack_forget()
        
        self.pages[page].pack(fill="both", expand=True)
        
        page_titles = {
            "home": "Dashboard",
            "analytics": "Analytics",
            "history": "History"
        }
        self.page_title.configure(text=page_titles[page])
        
        for i, (text, p) in enumerate(zip(["Dashboard", "Analytics", "History"], 
                                      ["home", "analytics", "history"])):
            if p == page:
                self.nav_buttons[i].configure(fg_color=("gray75", "gray25"))
            else:
                self.nav_buttons[i].configure(fg_color="transparent")
        
        self.current_page = page

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.sidebar_visible = False
        else:
            self.main_frame.pack_forget()
            self.chatbot_frame.pack_forget()
            
            self.sidebar_frame.pack(side="left", fill="y", expand=False)
            self.main_frame.pack(side="left", fill="both", expand=True)
            self.chatbot_frame.pack(side="right", fill="y", expand=False)
            
            self.sidebar_visible = True

    def logout(self):
        print("Settings button clicked")

if __name__ == "__main__":
    root = ctk.CTk()
    app = DashboardApp(root)
    root.mainloop()