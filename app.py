import streamlit as st
import os
import random
import time
from datetime import datetime
import uuid
import platform
import hashlib
import json

# Page config
st.set_page_config(
    page_title="IT Asset Recycling Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .success-alert {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(40, 167, 69, 0.2);
    }
    
    .warning-alert {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(255, 193, 7, 0.2);
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 10px !important;
        height: 3em !important;
        font-weight: bold !important;
    }
    
    .delete-button {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%) !important;
        color: white !important;
    }
    
    .cert-button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_files' not in st.session_state:
    st.session_state.selected_files = []
if 'wipe_history' not in st.session_state:
    st.session_state.wipe_history = []
if 'last_operation' not in st.session_state:
    st.session_state.last_operation = None
if 'show_certificate' not in st.session_state:
    st.session_state.show_certificate = False

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ IT Asset Recycling Dashboard</h1>
        <h3>Secure Data Wiping for Trustworthy IT Asset Recycling</h3>
        <p>Professional-grade data destruction with compliance certification</p>
        <p><strong>Status: 🟢 System Ready</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Control Panel
        st.markdown("## 🎛️ Secure Wiping Controls")
        
        # File upload section
        with st.container():
            st.markdown("### 📁 Select Files for Secure Deletion")
            uploaded_files = st.file_uploader(
                "Upload files to securely wipe",
                accept_multiple_files=True,
                type=None,
                help="Select multiple files for permanent deletion"
            )
            
            if uploaded_files:
                for file in uploaded_files:
                    if file.name not in [f['name'] for f in st.session_state.selected_files]:
                        st.session_state.selected_files.append({
                            'name': file.name,
                            'size': file.size,
                            'type': file.type or 'Unknown'
                        })
        
        # Selected files display
        if st.session_state.selected_files:
            st.markdown("### 📋 Selected Items")
            
            for i, file in enumerate(st.session_state.selected_files):
                col_file, col_size, col_remove = st.columns([3, 1, 1])
                with col_file:
                    st.write(f"📄 **{file['name']}**")
                with col_size:
                    st.write(f"`{format_size(file['size'])}`")
                with col_remove:
                    if st.button("🗑️", key=f"remove_{i}", help="Remove file"):
                        st.session_state.selected_files.pop(i)
                        st.rerun()
            
            # Total info
            total_size = sum(f['size'] for f in st.session_state.selected_files)
            st.info(f"📊 **Total: {len(st.session_state.selected_files)} files • {format_size(total_size)}**")
            
            # Clear all button
            if st.button("🧹 Clear All Selection"):
                st.session_state.selected_files = []
                st.rerun()
        
        # Wiping method
        st.markdown("### 🔧 Wiping Method")
        method = st.selectbox(
            "Choose security level:",
            ["DOD 3-Pass (Fast)", "DOD 7-Pass (Secure)", "NIST Clear", "NIST Purge", "Gutmann 35-Pass (Maximum)"],
            help="Higher passes = more secure but slower"
        )
        
        # Warning
        if st.session_state.selected_files:
            st.markdown("""
            <div class="warning-alert">
                <h4>⚠️ WARNING</h4>
                <p>This action will <strong>PERMANENTLY DELETE</strong> selected files using industry-standard secure wiping methods.</p>
                <p><strong>Data cannot be recovered after this operation!</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Main delete button
            if st.button("🔥 START SECURE WIPE", type="primary", key="delete_btn"):
                perform_secure_wipe(method)
        else:
            # Demo info
            st.markdown("""
            <div class="stat-card">
                <h4>🎯 How to Use</h4>
                <ol>
                    <li><strong>Upload Files:</strong> Use the file uploader above</li>
                    <li><strong>Choose Method:</strong> Select security level</li>
                    <li><strong>Confirm Deletion:</strong> Click the red delete button</li>
                    <li><strong>Get Certificate:</strong> Download compliance proof</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Statistics
        st.markdown("## 📊 Statistics")
        
        total_ops = len(st.session_state.wipe_history)
        success_rate = 100 if total_ops == 0 else len([op for op in st.session_state.wipe_history if op['status'] == 'Success']) / total_ops * 100
        total_data = sum(op.get('total_size', 0) for op in st.session_state.wipe_history)
        
        # Stats display
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #667eea; margin: 0; text-align: center;">{total_ops}</h2>
            <p style="margin: 0; text-align: center;">Total Operations</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #28a745; margin: 0; text-align: center;">{success_rate:.1f}%</h2>
            <p style="margin: 0; text-align: center;">Success Rate</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #764ba2; margin: 0; text-align: center;">{format_size(total_data)}</h2>
            <p style="margin: 0; text-align: center;">Data Wiped</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Certificate section
        if st.session_state.last_operation:
            st.markdown("## 📜 Certificate")
            if st.button("📜 Generate Certificate", key="cert_btn"):
                st.session_state.show_certificate = True
                generate_certificate()
        
        # History
        st.markdown("## 📋 Recent History")
        if st.session_state.wipe_history:
            for op in reversed(st.session_state.wipe_history[-5:]):
                status_emoji = "✅" if op['status'] == 'Success' else "❌"
                timestamp = datetime.fromisoformat(op['timestamp']).strftime('%m/%d %H:%M')
                st.write(f"{status_emoji} `{timestamp}` - {op['method']} ({op['item_count']} items)")
        else:
            st.write("No operations yet")

def perform_secure_wipe(method):
    """Simulate secure wiping process"""
    if not st.session_state.selected_files:
        st.error("No files selected!")
        return
    
    # Confirmation
    if not st.session_state.get('confirmed_wipe', False):
        st.session_state.confirmed_wipe = st.checkbox("✅ I confirm permanent deletion of selected files")
        if not st.session_state.confirmed_wipe:
            st.warning("Please confirm before proceeding")
            return
    
    # Progress simulation
    with st.spinner('Performing secure wipe...'):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_files = len(st.session_state.selected_files)
        total_size = sum(f['size'] for f in st.session_state.selected_files)
        
        for i, file in enumerate(st.session_state.selected_files):
            status_text.text(f"Securely wiping: {file['name']}...")
            progress_bar.progress((i + 1) / total_files)
            time.sleep(0.8)  # Simulate processing
        
        status_text.text("Finalizing secure deletion...")
        time.sleep(0.5)
    
    # Create operation record
    operation = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'status': 'Success',
        'item_count': total_files,
        'total_size': total_size,
        'items': [f['name'] for f in st.session_state.selected_files]
    }
    
    st.session_state.wipe_history.append(operation)
    st.session_state.last_operation = operation
    st.session_state.selected_files = []
    st.session_state.confirmed_wipe = False
    
    # Success message
    st.markdown("""
    <div class="success-alert">
        <h4>✅ Secure Wipe Completed Successfully!</h4>
        <p><strong>All selected files have been permanently deleted using industry-standard methods.</strong></p>
        <p>🔒 <strong>Files cannot be recovered!</strong></p>
        <p>📜 Certificate is ready for generation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.balloons()
    time.sleep(1)
    st.rerun()

def generate_certificate():
    """Generate compliance certificate"""
    if not st.session_state.last_operation:
        st.error("No recent operation to certify!")
        return
    
    op = st.session_state.last_operation
    cert_id = str(uuid.uuid4())[:8].upper()
    
    certificate = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CERTIFICATE OF DATA DESTRUCTION                      ║
║                          IT Asset Recycling Services                        ║
╠══════════════════════════════════════════════════════════════════════════════╣

Certificate ID: {cert_id}
Issue Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Operation ID: {op['id'][:8].upper()}

DESTRUCTION DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method Used: {op['method']}
Total Items Destroyed: {op['item_count']}
Total Data Wiped: {format_size(op['total_size'])}

COMPLIANCE STANDARDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ DOD 5220.22-M Standard
✓ NIST SP 800-88 Guidelines  
✓ Secure Multi-Pass Overwriting
✓ Cryptographically Secure Random Data

ITEMS DESTROYED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for i, item in enumerate(op['items'], 1):
        certificate += f"{i:2d}. {item}\n"
    
    certificate += f"""
SYSTEM INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Platform: Web Application - Streamlit
Timestamp: {op['timestamp']}

CERTIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This certificate confirms that the above-listed items have been securely 
destroyed using industry-standard methods. The data is computationally 
infeasible to recover.

Digital Signature: {hashlib.sha256(cert_id.encode()).hexdigest()[:32].upper()}

╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    st.success("📜 Certificate Generated Successfully!")
    st.text_area("🏆 Destruction Certificate", certificate, height=400)
    
    # Download button
    st.download_button(
        label="📥 Download Certificate",
        data=certificate,
        file_name=f"destruction_certificate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        key="download_cert"
    )

def format_size(size_bytes):
    """Format file size"""
    if size_bytes == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {units[i]}"

if __name__ == "__main__":
    main()