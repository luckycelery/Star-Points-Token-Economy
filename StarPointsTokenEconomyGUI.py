"""
Title: Star Points
Assignment: SDEV140 Final Project Status Report II
Last Edited: 02/22/25
Author: Emma Kaufman
This GUI program will act as an electronic token economy
that tracks progress, points earned, etc. *** ADD MORE***
"""

import tkinter as tk
import tkinter.font as tkFont

def create_main_window():
    """Create and return the main window"""
    root = tk.Tk()  # Create main window (aka 'root')
    root.title("Star Points")  # Create title of the window
    configure_grid(root)  # Call grid config function
    root.configure(bg="light blue")  # Set background color
    return root

def configure_grid(root):
    """Configure the grid layout for the main window"""
    # Set the grid column configuration and assign weights
    root.columnconfigure(0, weight=2)  # First column
    root.columnconfigure(1, weight=2)  # Second column
    root.columnconfigure(2, weight=1)  # Third column
    root.columnconfigure(3, weight=1)  # Fourth column
    root.columnconfigure(4, weight=1)  # Fifth column
    root.columnconfigure(5, weight=1)  # Sixth column

def create_fonts():
    """Define and return the fonts that will be used"""
    banner_font = tkFont.Font(family="Times New Roman", size=50, weight="bold")
    header_font = tkFont.Font(family="Times New Roman", size=20, weight="bold")
    return banner_font, header_font

def create_banner(root, banner_font):
    """Create and place the banner title on the main page"""
    mainPageBanner = tk.Label(
        root, text="Star Points", font=banner_font,
        fg="blue", bg="light blue"
    )
    mainPageBanner.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

def create_taskComplete(root, header_font, items):
    """Create and format the tasks completed section on the main page"""
    tasksCompletedHeader = tk.Label(
        root, text="What did you do today?",
        font=header_font, fg="gray", bg="light blue"
    )
    tasksCompletedHeader.grid(row=1, column=0, sticky="w", padx=10, pady=10)
    create_taskChecklist(root, items)  # Make sure items are passed

def create_taskChecklist(root, items):
    """Create a list of checkboxes in the main window"""
    taskList = []  # List to store BooleanVar for each checkbox

    checkbox_frame = tk.Frame(root, bg="light blue")
    checkbox_frame.grid(row=2, column=0, columnspan=6, sticky="w", padx=25, pady=10)
    
    for item in items:
        var = tk.BooleanVar()
        taskList.append(var)
        checkbox = tk.Checkbutton(
            checkbox_frame, text=item, variable=var,
            bg="light blue"
        )
        checkbox.pack(anchor="w", padx=5, pady=2)
    return taskList
    

def create_selfGrade(root, header_font):
    """Create Self Grade section of main window"""
    selfGradeHeader = tk.Label(
        root, text="What grade do you give yourself? (1-10)",
        font=header_font, fg="gray", bg="light blue"
    )
    selfGradeHeader.grid(row=3, column=0, sticky="w",padx=10, pady=30)
    #create empty field for user to enter number
    selfGradeEntry = tk.Entry(root, width=15,)
    selfGradeEntry.grid(row=4, column=0, sticky="w", padx=25, pady=10 )

def create_actualGrade(root, header_font):
    """Create Actual Grade section of the main window"""
    actualGradeHeader = tk.Label(
        root, text="What was your actual grade? (1-10)",
        font=header_font, fg="gray", bg="light blue"
    )
    actualGradeHeader.grid(row=5, column=0, sticky="w", padx=10, pady=10)
    actualGradeEntry = tk.Entry(root, width=15)
    actualGradeEntry.grid(row=6, column=0, sticky="w", padx=25, pady=10 )

def create_stats(root, header_font):
    """Create the Stats section of the main window"""
    statsHeader = tk.Label(
        root, text="Stats",
        font=header_font, fg="gray", bg="light blue"
    )
    statsHeader.grid(row=1, column=5, sticky="e", padx=10, pady=10)

def create_rewards(root, header_font):
    """Create You've Earned section of the main window"""
    rewardsHeader = tk.Label(
        root, text="Earned Rewards: *** ADD MORE ***",
        font=header_font, fg="gray", bg="light blue"
    )
    rewardsHeader.grid(row=4, column=5, columnspan=6, padx=10, pady=10)

def create_bonus(root, header_font):
    "Create Bonus section on main window"
    bonusPointsHeader = tk.Label(
        root, text="Bonus Points: *** ADD MORE ***",
        font=header_font, fg="gray", bg="light blue"
    )
    bonusPointsHeader.grid(row=5, column=2, sticky="w", padx=10, pady=10)
    bonusPoints = tk.Entry(root, width=15)
    bonusPoints.grid(row=6, column=2, sticky="w", padx=25, pady=10 )

def create_ParentButton(root):
    """Create Parent Portal Button on main window"""
    def on_pbutton_click():
        print('clicked parent protal')
    
    parentButton = tk.Button(
        root, text="Parent Portal", command=on_pbutton_click, 
        font=("Times New Roman", 15, "bold"), bg="light blue"
    )
    parentButton.grid(row=6, column=5,sticky="w", padx=10, pady=10 )

def create_refreshButton(root):
    """Create Refresh Button on main window"""
    def on_rbutton_click():
        print('clicked refresh button')
    
    refreshButton = tk.Button(
        root, text="Refresh", command=on_rbutton_click,
        font=("Times New Roman", 15, "bold"), bg="light blue" 
    )
    refreshButton.grid(row=6, column=6,sticky="w", padx=50, pady=10)

def create_enterButton(root):
    """Create Enter button on main window"""
    def on_ebutton_click():
        print('clicked Enter button')
    
    enterButton= tk.Button(
        root, text="Enter", command=on_ebutton_click,
        font=("Times New Roman", 15, "bold"), bg="light blue"
    )
    enterButton.grid(row=3, column=2,sticky="w", padx=10, pady=10)

def main():
    root = create_main_window()
    banner_font, header_font = create_fonts()
    create_banner(root, banner_font)
    
    # List of items for checkboxes
    checkbox_items = ["Task 1", "Task 2", "Task 3", "Task 4", "task 5", "task 6", "task 7"]

    create_taskComplete(root, header_font, checkbox_items)  # Pass items to taskComplete
    create_selfGrade(root, header_font)
    create_actualGrade(root, header_font)
    create_stats(root, header_font)
    create_rewards(root, header_font)
    create_bonus(root, header_font)
    create_ParentButton(root)
    create_refreshButton(root)
    create_enterButton(root)
    root.mainloop()

if __name__ == "__main__":
    main()