"""
Weidian Scraper GUI

A graphical user interface for the Weidian Product Scraper. This module provides
a user-friendly way to input multiple Weidian product links and process them
using the weidian_Scraper module.

Dependencies:
    - tkinter
    - threading
    - weidian_Scraper
"""

import tkinter as tk
from tkinter import messagebox, Toplevel, Label
from threading import Thread
from weidian_Scraper import main  # Make sure this function exists in weidian_scraper.py


def process_links(links, loading_popup):
    """
    Process the provided Weidian links using the scraper module.
    
    Args:
        links (list): List of Weidian product URLs to process
        loading_popup (Toplevel): Tkinter window showing loading status
        
    This function runs in a separate thread to prevent GUI freezing.
    It handles success and error cases by showing appropriate messages.
    """
    try:
        main(links)
        loading_popup.destroy()
        messagebox.showinfo("Success", "Links have been processed.")
    except Exception as e:
        loading_popup.destroy()
        messagebox.showerror("Error", f"An error occurred: {e}")


def submit_links():
    """
    Handle the submission of links from the GUI.
    
    This function:
    1. Retrieves links from the text box
    2. Validates the input
    3. Creates a loading popup
    4. Starts the processing in a separate thread
    """
    links_text = text_box.get("1.0", tk.END).strip()
    links = [link.strip() for link in links_text.splitlines() if link.strip()]
    if not links:
        messagebox.showwarning("Input Error", "Please enter at least one link.")
        return

    # Create and configure loading popup
    loading_popup = Toplevel(root)
    loading_popup.title("Loading")
    loading_popup.geometry("250x80")
    loading_popup.resizable(False, False)
    Label(loading_popup, text="Processing, please wait...").pack(pady=20)
    loading_popup.grab_set()
    loading_popup.update()

    # Start processing in a separate thread
    thread = Thread(target=process_links, args=(links, loading_popup))
    thread.start()


# Initialize the main application window
root = tk.Tk()
root.title("Weidian Scraper GUI")

# Create and configure GUI elements
label = tk.Label(root, text="Enter Weidian links (one per line):")
label.pack(padx=10, pady=(10, 0))

text_box = tk.Text(root, height=10, width=50)
text_box.pack(padx=10, pady=10)

submit_button = tk.Button(root, text="Submit", command=submit_links)
submit_button.pack(padx=10, pady=(0, 10))

# Start the main event loop
root.mainloop()