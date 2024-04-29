import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd #Use of dataframes
import numpy as np #To calculate trend line


# Load data from CSV file
data = pd.read_csv('base.csv')

# Define columns and create DataFrame
columns = ['paper name', 'price', 'date sec']
df = pd.DataFrame(data, columns=columns)

# Convert 'date sec' to datetime format
df['date sec'] = pd.to_datetime(df['date sec'], unit='s')

# Function to plot chart for selected paper name
def plot_chart():
    #Setting to current selected otion
    selected_paper = dropdown_var.get()
    group_df = df[df['paper name'] == selected_paper]
    
    # Clear previous plot
    ax.clear()
    
    # Plot the chart
    ax.plot(group_df['date sec'], group_df['price'], marker='o', linestyle='-', label='Price')
    ax.set_title(f'Price for {selected_paper}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()

    # Add trend line to the plot
    z = np.polyfit(range(len(group_df['date sec'])), group_df['price'], 1)
    p = np.poly1d(z)
    ax.plot(group_df['date sec'], p(range(len(group_df['date sec']))), "r--")
    
    # Refresh canvas
    canvas.draw()

# Create a tkinter window
window = tk.Tk()
window.title("Charts of price")

# Create a Matplotlib figure
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)

# Create a canvas to display Matplotlib figure in tkinter window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

# Create a list of paper names
paper_names = df['paper name'].unique().tolist()

# Create a variable to store the selected paper name
dropdown_var = tk.StringVar(window)
dropdown_var.set(paper_names[0])  # Set default value

# Create a dropdown menu
dropdown_menu = ttk.Combobox(window, textvariable=dropdown_var, values=paper_names)
dropdown_menu.pack()

# Create a button to plot the chart
plot_button = ttk.Button(window, text="Change Plot", command=plot_chart)
plot_button.pack()

# Plot the initial chart
plot_chart()

# Run the tkinter event loop
window.mainloop()
