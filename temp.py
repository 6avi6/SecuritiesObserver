import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV file
data = pd.read_csv('base.csv')

# Define columns and create DataFrame
columns = ['paper name', 'price', 'date sec', 'page url id', 'pagealias']
df = pd.DataFrame(data, columns=columns)

# Convert 'date sec' to datetime format
df['date sec'] = pd.to_datetime(df['date sec'], unit='s')

# Function to plot chart for selected paper name
def plot_chart():
    selected_paper = dropdown_var.get()
    group_df = df[df['paper name'] == selected_paper]
    
    # Clear previous plot
    plt.cla()
    
    # Plot the chart
    plt.plot(group_df['date sec'], group_df['price'], marker='o', linestyle='-', label='Price')
    plt.title(f'Price for {selected_paper}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.legend()

    # Add trend line to the plot
    z = np.polyfit(range(len(group_df['date sec'])), group_df['price'], 1)
    p = np.poly1d(z)
    plt.plot(group_df['date sec'], p(range(len(group_df['date sec']))), "r--")
    
    # Refresh canvas
    canvas.draw()

# Create a tkinter window
window = tk.Tk()
window.title("Matplotlib Charts for Paper Names")

# Create a Matplotlib figure
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)

# Create a canvas to display Matplotlib figure in tkinter window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

# Create a list of paper names
paper_names = df.groupby('paper name').size()


# Create a variable to store the selected paper name
dropdown_var = tk.StringVar(window)
dropdown_var.set(paper_names[0])  # Set default value

# Create a dropdown menu
dropdown_menu = ttk.Combobox(window, textvariable=dropdown_var, values=paper_names)
dropdown_menu.pack()

# Create a button to plot the chart
plot_button = ttk.Button(window, text="Plot", command=plot_chart)
plot_button.pack()

# Run the tkinter event loop
window.mainloop()
