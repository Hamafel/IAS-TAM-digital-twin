import tkinter as tk
from tkinter import ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from PIL import Image

# Function to generate sample data
# we haven't had time to create realtime monotoring
def generate_data():
    data = {
        'Time': pd.date_range('2022-01-01', periods=100, freq='D'),
        'CO2': pd.Series(range(100)),
        'Temperature': pd.Series(range(100)) * 2,
    }
    return pd.DataFrame(data)

# Function to plot data inside the Tkinter window
def plot_data():
    df = generate_data()

    # Create a figure to be displayed in Tkinter
    fig, ax = plt.subplots(1, 3, figsize=(10, 6))
    sns.set_style('whitegrid')

    # Plot both CO2 and Temperature on separate subplots
    sns.lineplot(x='Time', y='CO2', data=df, label='CO2 Evolution', ax=ax[0])
    sns.lineplot(x='Time', y='Temperature', data=df, label='Temperature Level', ax=ax[1])
    
    # Set titles for each subplot
    ax[0].set_title('CO2 Evolution')
    ax[1].set_title('Temperature Level over Time')

    # Format the x-axis to display date labels correctly
    ax[0].xaxis.set_major_locator(mdates.AutoDateLocator())
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    ax[1].xaxis.set_major_locator(mdates.AutoDateLocator())
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Rotate and align the x-axis labels
    plt.setp(ax[0].xaxis.get_majorticklabels(), rotation=45, ha='right')
    plt.setp(ax[1].xaxis.get_majorticklabels(), rotation=45, ha='right')

    img = Image.open("Bird.jpeg")
    ax[2].imshow(img)
    ax[2].set_title("solar panal image")

    ax[2].legend()

    # Add legends
    ax[0].legend()
    ax[1].legend()

    # Embed the figure into the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to handle the window close event
def on_closing():
    # Close the Tkinter window
    root.quit()
    root.destroy()

# Initialize the main window
root = tk.Tk()
root.title("Dynamic Plotting with Tkinter")

# Set window size
root.geometry("1300x800")

# Create a frame for the plot area
plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

# Plot the data inside the Tkinter window
plot_data()

# Protocol to handle the "X" button (close window event)
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()
