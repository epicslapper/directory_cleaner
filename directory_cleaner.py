import os
import streamlit as st
import pyperclip  # New library for clipboard access

# Config
TARGET_DIR = "E:/pycharms/uvtemplate1"
IGNORE_DIRS = {'.git', '__pycache__', 'venv', '.idea', '.vscode', '.env'}
IGNORE_EXTS = {'.tmp', '.log', '.bak'}


def main():
    st.title("📂 Project Structure Visualizer")

    # Filter options
    st.sidebar.header("Display Options")
    show_py_only = st.sidebar.checkbox("Only Python files", False)
    show_hidden = st.sidebar.checkbox("Show hidden files", False)
    max_depth = st.sidebar.slider("Max folder depth", 1, 5, 3)

    # Scan directory
    structure = scan_directory(TARGET_DIR, max_depth, show_py_only, show_hidden)

    # Display structure
    st.subheader("Folder Structure")
    st.code(structure, language="text")

    # Working copy button
    if st.button("📋 Copy Structure to Clipboard"):
        try:
            pyperclip.copy(structure)
            st.success("Copied to clipboard!")
        except Exception as e:
            st.error(f"Copy failed: {e}")


def scan_directory(root_dir, max_depth, py_only=False, show_hidden=False):
    """Generate clean folder structure with filters"""
    structure = []

    for root, dirs, files in os.walk(root_dir):
        # Filter directories
        dirs[:] = [d for d in dirs if not (d.startswith('.') and not show_hidden) and d not in IGNORE_DIRS]

        current_depth = root[len(root_dir):].count(os.sep)
        if current_depth > max_depth:
            continue

        # Add current directory to structure
        indent = "    " * current_depth
        structure.append(f"{indent}📁 {os.path.basename(root)}/")

        # Add files
        for file in files:
            if py_only and not file.endswith('.py'):
                continue
            if not show_hidden and file.startswith('.'):
                continue
            if os.path.splitext(file)[1] in IGNORE_EXTS:
                continue

            structure.append(f"{indent}    📄 {file}")

    return "\n".join(structure)


if __name__ == "__main__":
    main()