import tkinter as tk

# List to store data points and their values
data_points_left = []
data_points_right = []
drop_counter_left = 1  # Counter to label each new data point as "Drop X"
drop_counter_right = 1  # Counter to label each new data point as "Drop X"
Moving_ave_Window_Size = 12

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

def save_parameters():
    global Beginning_Volume_mL_value, Additional_Drop_Volume_mL_value, Additional_Concentration_value, Initial_Voltage_Measured_value, Active_Ingredient_Volume_value, Flexo_Channel_Baseline_Voltage_value
    Beginning_Volume_mL_value = float(entry1.get())
    Additional_Drop_Volume_mL_value = float(entry2.get())
    Additional_Concentration_value = float(entry3.get())
    Initial_Voltage_Measured_value = float(entry4.get())
    Active_Ingredient_Volume_value = float(entry5.get())
    Flexo_Channel_Baseline_Voltage_value = float(entry6.get())

    # Initialize data_points with an initial reading
    initial_reading = (f"Initial Reading", Initial_Voltage_Measured_value)
    data_points_left.append(initial_reading)

    print(f"Parameters saved: {Beginning_Volume_mL_value}, {Additional_Drop_Volume_mL_value}, {Additional_Concentration_value}, {Initial_Voltage_Measured_value}, {Active_Ingredient_Volume_value}, {Flexo_Channel_Baseline_Voltage_value}")


def save_credentials():
    global pwd, UserName

# Function to add a new data point
def add_data_point(DropCounter,EntryDataPointValue,DataPointsList,Listbox):

    value = float(EntryDataPointValue.get())
    if value:
        drop_name = f"Drop {DropCounter}"
        DataPointsList.append((drop_name, value))
        update_data_points_list(Listbox,DataPointsList,)  # Update the displayed list of drops
        DropCounter += 1
        print(f"Data point added: {drop_name} = {value}")
        EntryDataPointValue.delete(0, tk.END)  # Clear the entry after adding


#------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to update the listbox with the current data points
def update_data_points_list(listbox, data_points_list):
    listbox.delete(0, tk.END)  # Clear the current list
    for name, value in data_points_list:
        listbox.insert(tk.END, f"{name}: {value}")









# Determines Calibration Coefficient Volume using initial volume, volume of additional drops, and number of drops added
def Calibration_Coeff_Volume(i):
     return Beginning_Volume_mL_value+Additional_Drop_Volume_mL_value*i


# Creates list of concentration values to determine slope (x axis)
def Create_Concentration_List(Additional_Drops):
    
    # Creates list for Concentration (x-axis), initializes first value as 0
    Concentration_List_x = [0]

    i = 1
    while i < Additional_Drops:

        # Calculates Concentration after adding each drop, based on current and pre
        Concentration = ((float(Concentration_List_x[i-1])*Calibration_Coeff_Volume(i-1))+(Additional_Drop_Volume_mL_value*Additional_Concentration_value))/float(Calibration_Coeff_Volume(i))

        Concentration_List_x.append(Concentration)
        i+=1

    return(Concentration_List_x)








def Generate_Slope(x, y):
    
    N = len(x)

    print(x)
    print(y)

    # Calculate the sum of x, y, x*y, and x^2
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(N))
    sum_x_squared = sum(x[i] ** 2 for i in range(N))

    # Calculate the slope using the least squares method
    slope = (N * sum_xy - sum_x * sum_y) / (N * sum_x_squared - sum_x ** 2)

    print("Slope:", slope)
    
    return (slope)

def display_slope():
    global slope

    if len(data_points) < 2:
        slope_label.config(text="Not enough points to calculate slope")
    else:
        print(data_points)
        slope = 1/ (1000*Generate_Slope(Create_Concentration_List(drop_counter),[value for name, value in data_points]))
        slope_label.config(text=f"Slope: {slope}")





def moving_average(time_list, value_list, window_size):
    global Area_Under_V_Curve

    if len(value_list) < window_size:
        raise ValueError("Value list must be at least as long as the window size.")

    moving_averages = []
    
    for i in range(len(value_list) - window_size + 1):
        # Calculate the average for the current window
        window_average = sum(value_list[i:i + window_size]) / window_size
        moving_averages.append(window_average)

    # Adjust time list for moving averages
    adjusted_time_list = time_list[window_size - 1:]  # Align time with moving averages
    
    Area_Under_V_Curve = sum(moving_averages)

    return adjusted_time_list, moving_averages


def calculate_flow():
    return ((Active_Ingredient_Volume_value*1000)*(1/slope)*(1/Area_Under_V_Curve))






# Initialize the main window
root = tk.Tk()
root.title("Main Menu with Parameters and Data Points")
root.geometry("600x600")

# Create a container to stack all frames
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Create four menus (frames)
menu1 = tk.Frame(container)
menu2 = tk.Frame(container)
menu3 = tk.Frame(container)
menuCredentials = tk.Frame(container)
menu_flows = tk.Frame(container)

left_frame = tk.Frame(menu3)
left_frame.grid(row=0, column=0, padx=10)

right_frame = tk.Frame(menu3)
right_frame.grid(row=0, column=1, padx=10)

# Position all frames in the same location, so they can overlap
for frame in (menu1, menu2, menu3, menuCredentials, menu_flows):
    frame.grid(row=0, column=0, sticky="nsew")

# ===================== MENU 1: Main Menu =====================
label1 = tk.Label(menu1, text="Main Menu", font=("Arial", 24))
label1.pack(pady=20)

GoToParameters_Button = tk.Button(menu1, text="Go to Parameters Menu", font=("Arial", 14), command=lambda: show_frame(menu2))
GoToParameters_Button.pack(pady=10)

button2 = tk.Button(menu1, text="Go to Add Data Points Menu", font=("Arial", 14), command=lambda: show_frame(menu3))
button2.pack(pady=10)

button_credentials = tk.Button(menu1, text="Go to FlowWorks Parameters/Credentials Menu", font=("Arial", 14), command=lambda: show_frame(menuCredentials))
button_credentials.pack(pady=10)

# Button to go to Flows Menu
button_flows = tk.Button(menu1, text="Go to Flows Menu", font=("Arial", 14), command=lambda: show_flows_menu())
button_flows.pack(pady=10)

# ===================== MENU 2: Parameters Menu =====================
label2 = tk.Label(menu2, text="Parameters Menu", font=("Arial", 24))
label2.pack(pady=10)

# Create labels and entry boxes for the 6 parameters
Beginning_Volume_mL = tk.StringVar(value = 500)
Additional_Drop_Volume_mL = tk.StringVar(value = 0.5)
Additional_Concentration = tk.StringVar(value =2199.6)
Initial_Voltage_Measured = tk.StringVar(value = 0)
Active_Ingredient_Volume = tk.StringVar(value = 0.11)
Flexo_Channel_Baseline_Voltage = tk.StringVar(value = 0.0325)

tk.Label(menu2, text="Beginning Volume (ml):", font=("Arial", 12)).pack()
entry1 = tk.Entry(menu2, textvariable=Beginning_Volume_mL, font=("Arial", 12))
entry1.pack(pady=5)

tk.Label(menu2, text="Additional Drop Volume (ml):", font=("Arial", 12)).pack()
entry2 = tk.Entry(menu2, textvariable=Additional_Drop_Volume_mL, font=("Arial", 12))
entry2.pack(pady=5)

tk.Label(menu2, text="Concentration of Calibration Solution (ug/L):", font=("Arial", 12)).pack()
entry3 = tk.Entry(menu2, textvariable=Additional_Concentration, font=("Arial", 12))
entry3.pack(pady=5)

tk.Label(menu2, text="Initial Voltage Reading (V):", font=("Arial", 12)).pack()
entry4 = tk.Entry(menu2, textvariable=Initial_Voltage_Measured, font=("Arial", 12))
entry4.pack(pady=5)

tk.Label(menu2, text="Volume of Active Ingredient (g):", font=("Arial", 12)).pack()
entry5 = tk.Entry(menu2, textvariable=Active_Ingredient_Volume, font=("Arial", 12))
entry5.pack(pady=5)

tk.Label(menu2, text="Flexo Channel Baseline Voltage (V):", font=("Arial", 12)).pack()
entry6 = tk.Entry(menu2, textvariable=Flexo_Channel_Baseline_Voltage, font=("Arial", 12))
entry6.pack(pady=5)

# Button to save the parameters
save_button = tk.Button(menu2, text="Save Parameters", font=("Arial", 14), command=save_parameters)
save_button.pack(pady=20)

# Button to go back to the Main Menu
button2 = tk.Button(menu2, text="Go to Main Menu", font=("Arial", 14), command=lambda: show_frame(menu1))
button2.pack(pady=10)

# ===================== MENU 3: Add Data Points Menu =====================
# Place widgets in `menu3` using `grid`

# --------------------------------------------------------------------------------------------------------Left Section
label_left = tk.Label(left_frame, text="Add Data Points Menu (Left)", font=("Arial", 16))
label_left.grid(row=0, column=0, pady=10)

drop_label_left = tk.Label(left_frame, text="Enter value for Drop X (Left):", font=("Arial", 12))
drop_label_left.grid(row=1, column=0)

entry_data_point_value_left = tk.Entry(left_frame, font=("Arial", 12))
entry_data_point_value_left.grid(row=2, column=0, pady=5)


# Listbox to display data points in left section
listbox_data_points_left = tk.Listbox(left_frame, font=("Arial", 12), height=8, width=30)
listbox_data_points_left.grid(row=4, column=0, pady=10)


# Button to add data point in left section
add_button_left = tk.Button(left_frame, text="Add Data Point", font=("Arial", 12), command=lambda: add_data_point(drop_counter_left,entry_data_point_value_left,data_points_left, listbox_data_points_left))
add_button_left.grid(row=3, column=0, pady=10)

# --------------------------------------------------------------------------------------------------------Right Section
label_right = tk.Label(right_frame, text="Add Data Points Menu (Right)", font=("Arial", 16))
label_right.grid(row=0, column=0, pady=10)

drop_label_right = tk.Label(right_frame, text="Enter value for Drop X (Right):", font=("Arial", 12))
drop_label_right.grid(row=1, column=0)

entry_data_point_value_right = tk.Entry(right_frame, font=("Arial", 12))
entry_data_point_value_right.grid(row=2, column=0, pady=5)

listbox_data_points_right = tk.Listbox(right_frame, font=("Arial", 12), height=8, width=30)
listbox_data_points_right.grid(row=4, column=0, pady=10)

add_button_right = tk.Button(right_frame, text="Add Data Point", font=("Arial", 12), command=lambda: add_data_point(drop_counter_right,entry_data_point_value_right,data_points_right, listbox_data_points_right))
add_button_right.grid(row=3, column=0, pady=10)

# Slope Button and Slope Label in `menu3`, using grid
slope_button = tk.Button(menu3, text="Calculate Slope", font=("Arial", 14))
slope_button.grid(row=1, column=0, columnspan=2, pady=10)

slope_label = tk.Label(menu3, text="Slope: Not calculated", font=("Arial", 12))
slope_label.grid(row=2, column=0, columnspan=2, pady=10)

# Button to go back to the Main Menu
button_back2 = tk.Button(menu3, text="Go to Main Menu", font=("Arial", 14), command=lambda: show_frame(menu1))
button_back2.grid(row=3, column=0, columnspan=2, pady=10)



# ===================== MENU: FlowWorks Setup Page =====================
label_flowworks = tk.Label(menuCredentials, text="FlowWorks Setup Page", font=("Arial", 24))
label_flowworks.pack(pady=20)

# Entry for Username
label_username = tk.Label(menuCredentials, text="Username:", font=("Arial", 12))
label_username.pack()
entry_username = tk.Entry(menuCredentials, font=("Arial", 12))
entry_username.pack(pady=5)

# Entry for Password
label_password = tk.Label(menuCredentials, text="Password:", font=("Arial", 12))
label_password.pack()
entry_password = tk.Entry(menuCredentials, show="*", font=("Arial", 12))
entry_password.pack(pady=5)

# Entry for Start Date
label_start_date = tk.Label(menuCredentials, text="Start Date (YYYY-MM-DD):", font=("Arial", 12))
label_start_date.pack()
entry_start_date = tk.Entry(menuCredentials, font=("Arial", 12))
entry_start_date.pack(pady=5)

# Entry for End Date
label_end_date = tk.Label(menuCredentials, text="End Date (YYYY-MM-DD):", font=("Arial", 12))
label_end_date.pack()
entry_end_date = tk.Entry(menuCredentials, font=("Arial", 12))
entry_end_date.pack(pady=5)

# Button to go back to the Main Menu
back_to_main_button = tk.Button(menuCredentials, text="Back to Main Menu", font=("Arial", 14), command=lambda: show_frame(menu1))
back_to_main_button.pack(pady=20)



# ===================== MENU 4: Flows Menu =====================
  # Initialize the Flows Menu frame

# Function to show the Flows Menu
def show_flows_menu():
    show_frame(menu_flows)


# Label for the Flows Menu
label_flows = tk.Label(menu_flows, text="Flows Menu", font=("Arial", 24))
label_flows.pack(pady=10)

# Output value display
output_value = tk.StringVar(value="Flow: 0")
label_output = tk.Label(menu_flows, textvariable=output_value, font=("Arial", 16))
label_output.pack(pady=20)

# Canvas for the graph
canvas = tk.Canvas(menu_flows, width=500, height=400)
canvas.pack(pady=10)

# Example graph drawing function (replace with actual graph logic)
def draw_graph():
    # Example: Drawing a simple line graph (replace with your actual graphing code)
    canvas.delete("all")  # Clear the canvas
    canvas.create_line(50, 350, 450, 50, fill="blue", width=2)  # Sample line

# Button to refresh the graph (if needed)
button_draw_graph = tk.Button(menu_flows, text="Draw Graph", font=("Arial", 14), command=draw_graph)
button_draw_graph.pack(pady=10)

# Button to go back to the Main Menu
button_back_flows = tk.Button(menu_flows, text="Go to Main Menu", font=("Arial", 14), command=lambda: show_frame(menu1))
button_back_flows.pack(pady=10)

# Show the first frame (Main Menu) on startup
show_frame(menu1)

# Run the application
root.mainloop()

# Show the first frame (Main Menu) on startup
show_frame(menu1)

# Run the application
root.mainloop()