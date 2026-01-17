#!/usr/bin/env python3
"""
Student Loan Assistant - Desktop UI
Tkinter-based desktop application for local use.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys
import os
import json
from datetime import datetime
import queue

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import StudentLoanAssistant


class StudentLoanAssistantUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Student Loan Assistant - Desktop")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize system
        self.assistant = None
        self.initialized = False
        self.chat_history = []
        self.message_queue = queue.Queue()
        
        # Create UI
        self.setup_ui()
        self.initialize_system()
    
    def setup_ui(self):
        """Setup the main UI components."""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎓 Student Loan Assistant", 
                               font=('Arial', 20, 'bold'))
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="AI-Powered Guidance for Federal Student Loans",
                                  font=('Arial', 12))
        subtitle_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Chat tab
        self.create_chat_tab()
        
        # Evaluation tab
        self.create_evaluation_tab()
        
        # System tab
        self.create_system_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def create_chat_tab(self):
        """Create the chat interface tab."""
        chat_frame = ttk.Frame(self.notebook)
        self.notebook.add(chat_frame, text="💬 Chat")
        
        # Chat history area
        history_frame = ttk.LabelFrame(chat_frame, text="Conversation History")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(history_frame, height=20, wrap=tk.WORD)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input area
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Query input
        ttk.Label(input_frame, text="Ask your question:").pack(anchor=tk.W)
        
        self.query_input = scrolledtext.ScrolledText(input_frame, height=4, wrap=tk.WORD)
        self.query_input.pack(fill=tk.X, pady=(5, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X)
        
        # Send button
        self.send_button = ttk.Button(button_frame, text="🚀 Ask Assistant", 
                                     command=self.send_query, state=tk.DISABLED)
        self.send_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        ttk.Button(button_frame, text="🗑️ Clear History", 
                  command=self.clear_chat_history).pack(side=tk.LEFT)
        
        # Example queries
        example_frame = ttk.LabelFrame(chat_frame, text="💡 Example Queries")
        example_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        example_queries = [
            "What are the eligibility requirements for federal student loans?",
            "How do I apply for a Direct Loan?",
            "What are the current interest rates for student loans?",
            "How do I repay my student loans?",
            "What happens if I can't make my loan payments?",
            "What is the difference between subsidized and unsubsidized loans?"
        ]
        
        for i, query in enumerate(example_queries):
            btn = ttk.Button(example_frame, text=query[:50] + "...", 
                           command=lambda q=query: self.load_example_query(q))
            btn.pack(fill=tk.X, padx=5, pady=2)
    
    def create_evaluation_tab(self):
        """Create the evaluation tab."""
        eval_frame = ttk.Frame(self.notebook)
        self.notebook.add(eval_frame, text="📊 Evaluation")
        
        # Evaluation controls
        control_frame = ttk.LabelFrame(eval_frame, text="Evaluation Controls")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="📊 Run System Evaluation", 
                  command=self.run_evaluation).pack(pady=10)
        
        # Results area
        results_frame = ttk.LabelFrame(eval_frame, text="Evaluation Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.eval_display = scrolledtext.ScrolledText(results_frame, height=20, wrap=tk.WORD)
        self.eval_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_system_tab(self):
        """Create the system information tab."""
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="🔧 System")
        
        # System status
        status_frame = ttk.LabelFrame(system_frame, text="System Status")
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_display = scrolledtext.ScrolledText(status_frame, height=10, wrap=tk.WORD)
        self.status_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # System controls
        control_frame = ttk.LabelFrame(system_frame, text="System Controls")
        control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(control_frame, text="🔄 Reinitialize System", 
                  command=self.reinitialize_system).pack(side=tk.LEFT, padx=5, pady=10)
        
        ttk.Button(control_frame, text="💾 Save Chat History", 
                  command=self.save_chat_history).pack(side=tk.LEFT, padx=5, pady=10)
        
        ttk.Button(control_frame, text="📁 Load Chat History", 
                  command=self.load_chat_history).pack(side=tk.LEFT, padx=5, pady=10)
    
    def initialize_system(self):
        """Initialize the Student Loan Assistant system."""
        self.status_var.set("Initializing system...")
        self.root.update()
        
        def init_thread():
            try:
                self.assistant = StudentLoanAssistant()
                init_result = self.assistant.initialize_system()
                
                if init_result["status"] == "success":
                    self.initialized = True
                    self.message_queue.put(("success", "System initialized successfully!"))
                    self.message_queue.put(("status", "System Ready"))
                    self.send_button.config(state=tk.NORMAL)
                else:
                    self.message_queue.put(("error", f"Initialization failed: {init_result.get('error', 'Unknown error')}"))
                    self.message_queue.put(("status", "Initialization Failed"))
            except Exception as e:
                self.message_queue.put(("error", f"Error during initialization: {str(e)}"))
                self.message_queue.put(("status", "Error"))
        
        threading.Thread(target=init_thread, daemon=True).start()
        self.root.after(100, self.check_message_queue)
    
    def check_message_queue(self):
        """Check for messages from background threads."""
        try:
            while True:
                msg_type, message = self.message_queue.get_nowait()
                
                if msg_type == "success":
                    messagebox.showinfo("Success", message)
                elif msg_type == "error":
                    messagebox.showerror("Error", message)
                elif msg_type == "status":
                    self.status_var.set(message)
                elif msg_type == "chat":
                    self.add_chat_message(message)
                elif msg_type == "eval":
                    self.eval_display.insert(tk.END, message + "\n")
                    self.eval_display.see(tk.END)
                elif msg_type == "system":
                    self.status_display.insert(tk.END, message + "\n")
                    self.status_display.see(tk.END)
                
                self.message_queue.task_done()
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_message_queue)
    
    def send_query(self):
        """Send a user query to the assistant."""
        query = self.query_input.get("1.0", tk.END).strip()
        if not query:
            return
        
        # Add user message
        self.add_chat_message(f"👤 You: {query}")
        self.query_input.delete("1.0", tk.END)
        
        # Disable send button during processing
        self.send_button.config(state=tk.DISABLED)
        self.status_var.set("Processing query...")
        
        def process_thread():
            try:
                result = self.assistant.process_student_query(query)
                
                if "error" in result:
                    response = f"❌ Error: {result['error']}"
                else:
                    response = result.get("final_response", "No response generated.")
                
                self.message_queue.put(("chat", f"🤖 Assistant: {response}"))
                self.message_queue.put(("status", "Ready"))
                self.send_button.config(state=tk.NORMAL)
                
            except Exception as e:
                error_msg = f"❌ Error processing query: {str(e)}"
                self.message_queue.put(("chat", f"🤖 Assistant: {error_msg}"))
                self.message_queue.put(("status", "Error"))
                self.send_button.config(state=tk.NORMAL)
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def add_chat_message(self, message):
        """Add a message to the chat display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n\n"
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.see(tk.END)
        
        # Store in history
        self.chat_history.append({
            "timestamp": timestamp,
            "message": message
        })
    
    def load_example_query(self, query):
        """Load an example query into the input field."""
        self.query_input.delete("1.0", tk.END)
        self.query_input.insert("1.0", query)
    
    def clear_chat_history(self):
        """Clear the chat history."""
        self.chat_display.delete("1.0", tk.END)
        self.chat_history = []
    
    def run_evaluation(self):
        """Run system evaluation."""
        if not self.initialized:
            messagebox.showerror("Error", "System not initialized")
            return
        
        self.eval_display.delete("1.0", tk.END)
        self.status_var.set("Running evaluation...")
        
        def eval_thread():
            try:
                results = self.assistant.evaluate_system()
                
                if "error" in results:
                    self.message_queue.put(("eval", f"❌ Evaluation Error: {results['error']}"))
                else:
                    # Format and display results
                    self.message_queue.put(("eval", "📊 Evaluation Results:"))
                    self.message_queue.put(("eval", "=" * 50))
                    
                    summary = results.get("evaluation_summary", {})
                    self.message_queue.put(("eval", f"Total Metrics: {summary.get('total_metrics', 0)}"))
                    self.message_queue.put(("eval", f"Average Score: {summary.get('average_score', 0):.2f}"))
                    self.message_queue.put(("eval", f"Passing Rate: {summary.get('passing_score', 0):.1%}"))
                    
                    if "custom_metrics" in results:
                        self.message_queue.put(("eval", "\nCustom Metrics:"))
                        for metric, score in results["custom_metrics"].items():
                            self.message_queue.put(("eval", f"  {metric.title()}: {score:.2f}"))
                
                self.message_queue.put(("status", "Evaluation completed"))
                
            except Exception as e:
                self.message_queue.put(("eval", f"❌ Evaluation failed: {str(e)}"))
                self.message_queue.put(("status", "Evaluation failed"))
        
        threading.Thread(target=eval_thread, daemon=True).start()
    
    def reinitialize_system(self):
        """Reinitialize the system."""
        self.initialized = False
        self.assistant = None
        self.send_button.config(state=tk.DISABLED)
        self.initialize_system()
    
    def save_chat_history(self):
        """Save chat history to a file."""
        if not self.chat_history:
            messagebox.showwarning("Warning", "No chat history to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.chat_history, f, indent=2)
                messagebox.showinfo("Success", f"Chat history saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def load_chat_history(self):
        """Load chat history from a file."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    history = json.load(f)
                
                self.chat_history = history
                self.chat_display.delete("1.0", tk.END)
                
                for entry in history:
                    formatted_message = f"[{entry['timestamp']}] {entry['message']}\n\n"
                    self.chat_display.insert(tk.END, formatted_message)
                
                self.chat_display.see(tk.END)
                messagebox.showinfo("Success", f"Chat history loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")


def main():
    """Main function to run the desktop application."""
    root = tk.Tk()
    app = StudentLoanAssistantUI(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main() 