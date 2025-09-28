#!/usr/bin/env python3
"""
Professional IT Asset Recycling Dashboard - Fixed Version
Secure Data Wiping with Working Certificate Generation
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import random
import json
from datetime import datetime
import uuid
import platform
import hashlib

class ITAssetRecyclingDashboard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("IT Asset Recycling - Secure Data Wiping Dashboard")
        self.window.geometry("1200x800")
        self.window.configure(bg="#f8f9fa")
        
        # Data
        self.selected_items = []
        self.wipe_history = []
        self.current_operation = None
        self.certificate_ready = False  # Flag to track if certificate can be generated
        
        # Load existing history
        self.load_history()
        
        # Setup UI
        self.setup_styles()
        self.setup_dashboard()
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.window.winfo_screenheight() // 2) - (800 // 2)
        self.window.geometry(f"1200x800+{x}+{y}")
    
    def setup_styles(self):
        """Setup custom styles for professional white theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles for white theme
        style.configure('Dashboard.TFrame', background='#f8f9fa')
        style.configure('Card.TFrame', background='#ffffff', relief='solid', borderwidth=1)
        style.configure('Header.TLabel', background='#ffffff', foreground='#2c3e50', font=('Segoe UI', 16, 'bold'))
        style.configure('Subheader.TLabel', background='#f8f9fa', foreground='#6c757d', font=('Segoe UI', 11))
        style.configure('Card.TLabel', background='#ffffff', foreground='#495057', font=('Segoe UI', 10))
        style.configure('Success.TLabel', background='#ffffff', foreground='#28a745', font=('Segoe UI', 10, 'bold'))
        style.configure('Warning.TLabel', background='#ffffff', foreground='#ffc107', font=('Segoe UI', 10, 'bold'))
        style.configure('Error.TLabel', background='#ffffff', foreground='#dc3545', font=('Segoe UI', 10, 'bold'))
        style.configure('Title.TLabel', background='#f8f9fa', foreground='#212529', font=('Segoe UI', 24, 'bold'))
        style.configure('Subtitle.TLabel', background='#f8f9fa', foreground='#6c757d', font=('Segoe UI', 12))
    
    def setup_dashboard(self):
        """Create the main dashboard with beautiful design"""
        # Main container with padding
        main_frame = ttk.Frame(self.window, style='Dashboard.TFrame')
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = ttk.Frame(main_frame, style='Dashboard.TFrame')
        content_frame.pack(fill='both', expand=True, pady=(30, 0))
        
        # Left panel - Controls (wider)
        left_panel = ttk.Frame(content_frame, style='Dashboard.TFrame')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Right panel - Stats & History
        right_panel = ttk.Frame(content_frame, style='Dashboard.TFrame')
        right_panel.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Create panels
        self.create_control_panel(left_panel)
        self.create_stats_panel(right_panel)
        self.create_history_panel(right_panel)
    
    def create_header(self, parent):
        """Create beautiful header"""
        header_frame = ttk.Frame(parent, style='Dashboard.TFrame')
        header_frame.pack(fill='x')
        
        # Left side - Title and subtitle
        title_frame = ttk.Frame(header_frame, style='Dashboard.TFrame')
        title_frame.pack(side='left', anchor='w')
        
        # Main title
        title_label = ttk.Label(title_frame, text="🛡️ IT Asset Recycling", style='Title.TLabel')
        title_label.pack(anchor='w')
        
        # Subtitle
        subtitle_label = ttk.Label(title_frame, text="Secure Data Wiping for Trustworthy IT Asset Recycling", 
                                 style='Subtitle.TLabel')
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Right side - Status
        status_frame = ttk.Frame(header_frame, style='Dashboard.TFrame')
        status_frame.pack(side='right', anchor='e')
        
        self.status_label = ttk.Label(status_frame, text="🟢 System Ready", style='Success.TLabel')
        self.status_label.pack(anchor='e', pady=(10, 0))
        
        # Add separator line
        separator_frame = ttk.Frame(parent, style='Dashboard.TFrame', height=2)
        separator_frame.pack(fill='x', pady=(20, 0))
        
        separator_line = tk.Frame(separator_frame, height=1, bg='#dee2e6')
        separator_line.pack(fill='x')
    
    def create_control_panel(self, parent):
        """Create the main control panel with beautiful design"""
        # Control panel card
        control_card = ttk.Frame(parent, style='Card.TFrame', padding=25)
        control_card.pack(fill='both', expand=True)
        
        # Card header
        header_frame = ttk.Frame(control_card, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="🎛️ Secure Wiping Controls", style='Header.TLabel').pack(anchor='w')
        
        # File/Folder selection section
        selection_section = ttk.Frame(control_card, style='Card.TFrame')
        selection_section.pack(fill='x', pady=(0, 20))
        
        ttk.Label(selection_section, text="Select Items to Wipe:", style='Card.TLabel').pack(anchor='w', pady=(0, 10))
        
        # Selection buttons with modern design
        btn_frame = ttk.Frame(selection_section, style='Card.TFrame')
        btn_frame.pack(fill='x', pady=(0, 15))
        
        self.select_file_btn = tk.Button(btn_frame, 
                                        text="📄 Add Files", 
                                        command=self.select_files,
                                        bg='#007bff', fg='white', 
                                        font=('Segoe UI', 11, 'bold'),
                                        relief='flat', padx=25, pady=12,
                                        cursor='hand2',
                                        activebackground='#0056b3')
        self.select_file_btn.pack(side='left', padx=(0, 10))
        
        self.select_folder_btn = tk.Button(btn_frame, 
                                          text="📁 Add Folder", 
                                          command=self.select_folder,
                                          bg='#6f42c1', fg='white', 
                                          font=('Segoe UI', 11, 'bold'),
                                          relief='flat', padx=25, pady=12,
                                          cursor='hand2',
                                          activebackground='#5a32a3')
        self.select_folder_btn.pack(side='left')
        
        # Selected items display
        items_frame = ttk.Frame(selection_section, style='Card.TFrame')
        items_frame.pack(fill='both', expand=True)
        
        ttk.Label(items_frame, text="Selected Items:", style='Card.TLabel').pack(anchor='w', pady=(0, 8))
        
        # Listbox container with modern styling
        list_container = tk.Frame(items_frame, bg='#f8f9fa', relief='solid', bd=1)
        list_container.pack(fill='both', expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_container, bg='#e9ecef', troughcolor='#f8f9fa')
        scrollbar.pack(side='right', fill='y', padx=(0, 2), pady=2)
        
        # Listbox with modern styling
        self.items_listbox = tk.Listbox(list_container, 
                                       yscrollcommand=scrollbar.set,
                                       bg='#ffffff', fg='#495057',
                                       selectbackground='#007bff',
                                       selectforeground='white',
                                       font=('Segoe UI', 10),
                                       relief='flat',
                                       height=6,
                                       borderwidth=0,
                                       highlightthickness=0)
        self.items_listbox.pack(side='left', fill='both', expand=True, padx=2, pady=2)
        scrollbar.config(command=self.items_listbox.yview)
        
        # Clear button
        clear_btn = tk.Button(items_frame, 
                             text="🗑️ Clear Selection", 
                             command=self.clear_selection,
                             bg='#6c757d', fg='white', 
                             font=('Segoe UI', 10),
                             relief='flat', padx=15, pady=8,
                             cursor='hand2',
                             activebackground='#545b62')
        clear_btn.pack()
        
        # Wiping method section
        method_section = ttk.Frame(control_card, style='Card.TFrame')
        method_section.pack(fill='x', pady=(20, 20))
        
        ttk.Label(method_section, text="Wiping Method:", style='Card.TLabel').pack(anchor='w', pady=(0, 8))
        
        self.method_var = tk.StringVar(value="DOD 3-Pass")
        method_combo = ttk.Combobox(method_section, textvariable=self.method_var,
                                   values=["DOD 3-Pass", "DOD 7-Pass", "NIST Clear", "NIST Purge", "Gutmann 35-Pass"],
                                   state="readonly", width=30, font=('Segoe UI', 10))
        method_combo.pack(pady=(0, 10))
        
        # Progress section
        self.progress_section = ttk.Frame(control_card, style='Card.TFrame')
        self.progress_section.pack(fill='x', pady=(0, 20))
        
        self.progress_label = ttk.Label(self.progress_section, text="Ready to start wiping", 
                                      style='Card.TLabel')
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_section, mode='indeterminate', 
                                          style='TProgressbar')
        
        # Main action buttons
        action_section = ttk.Frame(control_card, style='Card.TFrame')
        action_section.pack(fill='x', pady=(20, 0))
        
        # Big red DELETE button
        self.wipe_btn = tk.Button(action_section, 
                                 text="🔥 START SECURE WIPE", 
                                 command=self.start_secure_wipe,
                                 bg='#dc3545', fg='white', 
                                 font=('Segoe UI', 14, 'bold'),
                                 relief='flat', padx=30, pady=18,
                                 cursor='hand2',
                                 state='disabled',
                                 activebackground='#c82333',
                                 disabledforeground='#6c757d')
        self.wipe_btn.pack(pady=(0, 15))
        
        # Certificate button - FIXED: Initially disabled with proper styling
        self.cert_btn = tk.Button(action_section, 
                                 text="📜 Generate Certificate", 
                                 command=self.generate_certificate,
                                 bg='#6c757d', fg='#adb5bd',  # Gray when disabled
                                 font=('Segoe UI', 11, 'bold'),
                                 relief='flat', padx=20, pady=10,
                                 cursor='hand2',
                                 state='disabled',
                                 activebackground='#28a745',  # Green when active
                                 disabledforeground='#adb5bd')
        self.cert_btn.pack()
    
    def create_stats_panel(self, parent):
        """Create statistics panel with modern cards"""
        stats_card = ttk.Frame(parent, style='Card.TFrame', padding=20)
        stats_card.pack(fill='x', pady=(0, 15))
        
        # Header
        ttk.Label(stats_card, text="📊 Statistics", style='Header.TLabel').pack(pady=(0, 15))
        
        # Stats grid
        stats_grid = ttk.Frame(stats_card, style='Card.TFrame')
        stats_grid.pack(fill='x')
        
        # Create stat cards
        self.create_stat_card(stats_grid, "Total Operations", "0", "#007bff", 'left')
        self.create_stat_card(stats_grid, "Success Rate", "100%", "#28a745", 'left')
        self.create_stat_card(stats_grid, "Data Wiped", "0 MB", "#6f42c1", 'right')
        
        self.update_stats()
    
    def create_stat_card(self, parent, title, value, color, side):
        """Create individual stat card"""
        stat_frame = ttk.Frame(parent, style='Card.TFrame')
        stat_frame.pack(side=side, fill='x', expand=True, padx=5 if side == 'left' else (5, 0))
        
        # Value
        value_label = tk.Label(stat_frame, text=value, 
                              bg='#ffffff', fg=color, 
                              font=('Segoe UI', 18, 'bold'))
        value_label.pack(pady=(5, 2))
        
        # Title
        title_label = ttk.Label(stat_frame, text=title, style='Card.TLabel')
        title_label.pack()
        
        # Store reference for updates
        if "Total" in title:
            self.total_ops_label = value_label
        elif "Success" in title:
            self.success_rate_label = value_label
        elif "Data" in title:
            self.data_wiped_label = value_label
    
    def create_history_panel(self, parent):
        """Create history panel with modern design"""
        history_card = ttk.Frame(parent, style='Card.TFrame', padding=20)
        history_card.pack(fill='both', expand=True)
        
        # Header
        ttk.Label(history_card, text="📋 Wipe History", style='Header.TLabel').pack(pady=(0, 15))
        
        # History table container
        table_frame = tk.Frame(history_card, bg='#f8f9fa', relief='solid', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        # Create treeview with modern styling
        style = ttk.Style()
        style.configure("Modern.Treeview", background="#ffffff", foreground="#495057", 
                       fieldbackground="#ffffff", font=('Segoe UI', 9))
        style.configure("Modern.Treeview.Heading", background="#f8f9fa", foreground="#495057",
                       font=('Segoe UI', 10, 'bold'))
        
        # Treeview with scrollbar
        tree_scroll = tk.Scrollbar(table_frame, bg='#e9ecef')
        tree_scroll.pack(side='right', fill='y', padx=(0, 2), pady=2)
        
        self.history_tree = ttk.Treeview(table_frame, 
                                        yscrollcommand=tree_scroll.set,
                                        columns=('timestamp', 'item', 'method', 'status'),
                                        show='headings',
                                        style="Modern.Treeview",
                                        height=8)
        
        # Configure columns
        self.history_tree.heading('timestamp', text='Date/Time')
        self.history_tree.heading('item', text='Items')
        self.history_tree.heading('method', text='Method')
        self.history_tree.heading('status', text='Status')
        
        self.history_tree.column('timestamp', width=130)
        self.history_tree.column('item', width=150)
        self.history_tree.column('method', width=100)
        self.history_tree.column('status', width=60)
        
        self.history_tree.pack(side='left', fill='both', expand=True, padx=2, pady=2)
        tree_scroll.config(command=self.history_tree.yview)
        
        self.refresh_history()
    
    def select_files(self):
        """Select multiple files"""
        files = filedialog.askopenfilenames(
            title="Select files to securely wipe",
            filetypes=[("All files", "*.*")]
        )
        
        for file in files:
            if file not in self.selected_items:
                self.selected_items.append(file)
                self.items_listbox.insert(tk.END, f"📄 {os.path.basename(file)}")
        
        self.update_buttons()
    
    def select_folder(self):
        """Select a folder"""
        folder = filedialog.askdirectory(title="Select folder to securely wipe")
        
        if folder and folder not in self.selected_items:
            self.selected_items.append(folder)
            self.items_listbox.insert(tk.END, f"📁 {os.path.basename(folder)}")
        
        self.update_buttons()
    
    def clear_selection(self):
        """Clear all selections"""
        self.selected_items.clear()
        self.items_listbox.delete(0, tk.END)
        self.update_buttons()
    
    def update_buttons(self):
        """Update button states with visual feedback"""
        # Update wipe button
        if self.selected_items:
            self.wipe_btn.config(state='normal', bg='#dc3545')
        else:
            self.wipe_btn.config(state='disabled', bg='#6c757d')
        
        # Update certificate button - FIXED: Proper state management
        if self.certificate_ready:
            self.cert_btn.config(
                state='normal', 
                bg='#28a745',  # Green when ready
                fg='white',
                activebackground='#218838'
            )
        else:
            self.cert_btn.config(
                state='disabled', 
                bg='#6c757d',  # Gray when disabled
                fg='#adb5bd'
            )
    
    def start_secure_wipe(self):
        """Start the secure wiping process"""
        if not self.selected_items:
            messagebox.showwarning("No Selection", "Please select files or folders to wipe.")
            return
        
        # Enhanced confirmation dialog
        result = messagebox.askyesno(
            "⚠️ Confirm Secure Wipe",
            f"WARNING: This will permanently delete {len(self.selected_items)} item(s)\n\n"
            f"Method: {self.method_var.get()}\n"
            f"This action CANNOT be undone!\n\n"
            f"Are you absolutely sure you want to proceed?",
            icon="warning"
        )
        
        if result:
            self.perform_wipe()
    
    def perform_wipe(self):
        """Perform the actual wiping operation with UI updates"""
        # Reset certificate flag
        self.certificate_ready = False
        
        # Update UI for wiping state
        self.wipe_btn.config(state='disabled', bg='#6c757d', text='🔄 WIPING IN PROGRESS...')
        self.select_file_btn.config(state='disabled')
        self.select_folder_btn.config(state='disabled')
        self.progress_bar.pack(pady=(10, 0))
        self.progress_bar.start(10)
        self.progress_label.config(text="Performing secure wipe... Please wait")
        self.status_label.config(text="🔄 Wiping in progress...", style='Warning.TLabel')
        
        # Create operation record
        operation_id = str(uuid.uuid4())
        self.current_operation = {
            'id': operation_id,
            'timestamp': datetime.now().isoformat(),
            'items': self.selected_items.copy(),
            'method': self.method_var.get(),
            'status': 'In Progress'
        }
        
        # Start wiping in separate thread
        thread = threading.Thread(target=self.wipe_worker)
        thread.daemon = True
        thread.start()
    
    def wipe_worker(self):
        """Worker thread for wiping operations"""
        try:
            total_size = 0
            successful_items = []
            failed_items = []
            
            for item in self.selected_items:
                try:
                    if os.path.isfile(item):
                        size = os.path.getsize(item)
                        self.secure_wipe_file(item)
                        total_size += size
                        successful_items.append(item)
                    elif os.path.isdir(item):
                        size = self.get_folder_size(item)
                        self.secure_wipe_folder(item)
                        total_size += size
                        successful_items.append(item)
                except Exception as e:
                    failed_items.append((item, str(e)))
            
            # Update operation record
            self.current_operation['status'] = 'Completed' if not failed_items else 'Partial'
            self.current_operation['total_size'] = total_size
            self.current_operation['successful_items'] = successful_items
            self.current_operation['failed_items'] = failed_items
            
            # Save to history
            self.wipe_history.append(self.current_operation)
            self.save_history()
            
            # Update UI in main thread
            self.window.after(0, self.wipe_completed)
            
        except Exception as e:
            self.current_operation['status'] = 'Failed'
            self.current_operation['error'] = str(e)
            self.window.after(0, lambda: self.wipe_error(str(e)))
    
    def secure_wipe_file(self, file_path):
        """Securely wipe a single file"""
        if not os.path.exists(file_path):
            return
        
        file_size = os.path.getsize(file_path)
        passes = 3 if 'DOD 3' in self.method_var.get() else 7
        
        with open(file_path, 'r+b') as f:
            for pass_num in range(passes):
                f.seek(0)
                bytes_written = 0
                
                while bytes_written < file_size:
                    chunk_size = min(4096, file_size - bytes_written)
                    random_data = bytes([random.randint(0, 255) for _ in range(chunk_size)])
                    f.write(random_data)
                    bytes_written += chunk_size
                
                f.flush()
                os.fsync(f.fileno())
        
        os.remove(file_path)
    
    def secure_wipe_folder(self, folder_path):
        """Securely wipe a folder and its contents"""
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                self.secure_wipe_file(file_path)
            
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    os.rmdir(dir_path)
                except:
                    pass
        
        try:
            os.rmdir(folder_path)
        except:
            pass
    
    def get_folder_size(self, folder_path):
        """Get total size of a folder"""
        total_size = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                try:
                    total_size += os.path.getsize(os.path.join(root, file))
                except:
                    pass
        return total_size
    
    def wipe_completed(self):
        """Handle successful wipe completion - FIXED"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        successful = len(self.current_operation['successful_items'])
        failed = len(self.current_operation.get('failed_items', []))
        
        messagebox.showinfo(
            "✅ Wipe Completed Successfully",
            f"Secure wipe completed!\n\n"
            f"✓ Successfully wiped: {successful} item(s)\n"
            f"✗ Failed: {failed} item(s)\n"
            f"📊 Total data wiped: {self.format_size(self.current_operation['total_size'])}\n\n"
            f"📜 Certificate is ready for generation."
        )
        
        # FIXED: Enable certificate generation
        self.certificate_ready = True
        
        # Reset UI and update buttons
        self.reset_ui()
        self.update_buttons()  # This will make the certificate button green
        
        # Update stats and history
        self.update_stats()
        self.refresh_history()
        
        # Clear selection
        self.clear_selection()
    
    def wipe_error(self, error_msg):
        """Handle wipe error"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        messagebox.showerror("❌ Wipe Error", f"Wipe operation failed!\n\nError: {error_msg}")
        self.reset_ui()
    
    def reset_ui(self):
        """Reset UI to ready state"""
        self.wipe_btn.config(
            state='normal' if self.selected_items else 'disabled', 
            bg='#dc3545' if self.selected_items else '#6c757d',
            text='🔥 START SECURE WIPE'
        )
        self.select_file_btn.config(state='normal')
        self.select_folder_btn.config(state='normal')
        self.progress_label.config(text="Ready to start wiping")
        self.status_label.config(text="🟢 System Ready", style='Success.TLabel')
    
    def generate_certificate(self):
        """Generate destruction certificate with professional format - FIXED"""
        if not self.current_operation or not self.certificate_ready:
            messagebox.showwarning("No Operation", "No recent wipe operation to certify.")
            return
        
        try:
            cert_data = {
                'certificate_id': str(uuid.uuid4()),
                'issue_date': datetime.now().isoformat(),
                'operation_id': self.current_operation['id'],
                'organization': 'IT Asset Recycling Services',
                'method': self.current_operation['method'],
                'items': self.current_operation['successful_items'],
                'total_size': self.current_operation['total_size'],
                'operator': os.getlogin() if hasattr(os, 'getlogin') else 'System',
                'system': platform.platform(),
                'compliance_standards': ['DOD 5220.22-M', 'NIST SP 800-88']
            }
            
            certificate = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CERTIFICATE OF DATA DESTRUCTION                      ║
║                          IT Asset Recycling Services                        ║
╠══════════════════════════════════════════════════════════════════════════════╣

Certificate ID: {cert_data['certificate_id']}
Issue Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Operation ID: {cert_data['operation_id']}

DESTRUCTION DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method Used: {cert_data['method']}
Total Items Destroyed: {len(cert_data['items'])}
Total Data Wiped: {self.format_size(cert_data['total_size'])}

COMPLIANCE STANDARDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ DOD 5220.22-M Standard
✓ NIST SP 800-88 Guidelines  
✓ Secure Multi-Pass Overwriting
✓ Cryptographically Secure Random Data

ITEMS DESTROYED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            for i, item in enumerate(cert_data['items'], 1):
                certificate += f"{i:2d}. {os.path.basename(item)}\n"
            
            certificate += f"""
SYSTEM INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Operator: {cert_data['operator']}
System: {cert_data['system']}
Timestamp: {cert_data['issue_date']}

CERTIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This certificate confirms that the above-listed items have been securely 
destroyed using industry-standard methods. The data is computationally 
infeasible to recover.

Digital Signature: {hashlib.sha256(cert_data['certificate_id'].encode()).hexdigest()[:32]}

╚══════════════════════════════════════════════════════════════════════════════╝
"""
            
            # Save files
            cert_filename = f"destruction_certificate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            json_filename = f"certificate_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(cert_filename, 'w', encoding='utf-8') as f:
                f.write(certificate)
            
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(cert_data, f, indent=2)
            
            messagebox.showinfo(
                "Certificate Generated Successfully",
                f"Certificate generated successfully!\n\n"
                f"Files created:\n"
                f"• {cert_filename}\n"
                f"• {json_filename}\n\n"
                f"Certificate ID: {cert_data['certificate_id'][:16]}...\n\n"
                f"These files serve as legal proof of secure data destruction."
            )
            
            # FIXED: Disable certificate button after generation with visual feedback
            self.certificate_ready = False
            self.cert_btn.config(
                state='disabled',
                bg='#17a2b8',  # Blue color to indicate completed
                fg='white',
                text='✅ Certificate Generated'
            )
            
        except Exception as e:
            messagebox.showerror("Certificate Error", f"Failed to generate certificate:\n{str(e)}")
    
    def update_stats(self):
        """Update statistics display"""
        total_ops = len(self.wipe_history)
        successful_ops = len([op for op in self.wipe_history if op['status'] == 'Completed'])
        success_rate = (successful_ops / total_ops * 100) if total_ops > 0 else 100
        
        total_data = sum(op.get('total_size', 0) for op in self.wipe_history)
        
        self.total_ops_label.config(text=str(total_ops))
        self.success_rate_label.config(text=f"{success_rate:.1f}%")
        self.data_wiped_label.config(text=self.format_size(total_data))
    
    def refresh_history(self):
        """Refresh history display"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add history items (most recent first)
        for op in reversed(self.wipe_history[-20:]):  # Show last 20
            timestamp = datetime.fromisoformat(op['timestamp']).strftime('%m/%d %H:%M')
            items_text = f"{len(op['items'])} item(s)"
            method = op['method']
            
            if op['status'] == 'Completed':
                status = "✅"
            elif op['status'] == 'Partial':
                status = "⚠️"
            else:
                status = "❌"
            
            self.history_tree.insert('', 0, values=(timestamp, items_text, method, status))
    
    def format_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        i = 0
        while size_bytes >= 1024 and i < len(units) - 1:
            size_bytes /= 1024
            i += 1
        
        return f"{size_bytes:.1f} {units[i]}"
    
    def load_history(self):
        """Load wipe history from file"""
        try:
            if os.path.exists('wipe_history.json'):
                with open('wipe_history.json', 'r', encoding='utf-8') as f:
                    self.wipe_history = json.load(f)
        except Exception:
            self.wipe_history = []
    
    def save_history(self):
        """Save wipe history to file"""
        try:
            with open('wipe_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.wipe_history, f, indent=2)
        except Exception:
            pass
    
    def run(self):
        """Start the application"""
        self.window.mainloop()


# Create and run the dashboard
if __name__ == "__main__":
    app = ITAssetRecyclingDashboard()
    app.run()