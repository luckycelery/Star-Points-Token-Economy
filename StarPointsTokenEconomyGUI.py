"""
===========================================================
Project Title:        Star Points Token Economy
Assignment Name:      Module 8 Final Project
Last Edited:         03/04/25
Due Date:            03/05/25
===========================================================

Description:
------------
This Python GUI application, built using Tkinter, is designed to 
track and reward task completion. Users can check off tasks, 
self-evaluate their performance, and earn rewards based on 
their accumulated points. 

Main Features:
- Task checklist with checkboxes
- Self-grading system (1-10)
- Reward redemption system based on earned points
- Parent Portal for modifying tasks and rewards
- Bonus point entry and data persistence

This application promotes motivation and engagement by allowing 
users to earn rewards for completing individualized tasks.
===========================================================
"""
import tkinter as tk #Import Tkiner library for GUI dev
import tkinter.font as tkFont #Import the font mod from Tkinter for custom fonts
import pickle #Import pickle to save and load persistent data
import random  #Import random to allow for random selection of rewards
from tkinter import messagebox #Import messagebox for validation checking

class DataManager:
    """
    DataManager class handles loading and saving data using pickle.
    Manges tasks, rewards, reward costs, and total points earned
    """
    def __init__(self):
        """Initialize the data by loading from files or setting defaults"""

        # Load task list from file or use defualt names is file doesn't exist
        self.tasks = self.load_data("tasks.pkl", [
            "Task 1", "Task 2", "Task 3",
            "Task 4", "Task 5", "Task 6", "Task 7"
         ])
        #load reward list from file of use defualt names if file doesn't exist 
        self.rewards = self.load_data("rewards.pkl", ["Reward 1", "Reward 2", "Reward 3"])

        #load reward costs from file or set to default if no saved data
        self.reward_costs = self.load_data("reward_costs.pkl", [10, 20, 30])

        #load and initialize the total accumulated points from file or set to 0 if not found
        self.total_points = self.load_data("total_points.pkl", 0) 


    def load_data(self, filename, default_data):
        """
        Load data from a file using Pickle. If File not found - return default value.
        Arguments: 
            filename(str): name of the file to load data from
            default_data(any): default data to return if file doesn't exist
        Returns:
            loaded data or defualt value if no file found
        """

        try:
            #attmpt to open the file in binary read mode and load its contents
            with open(filename, "rb") as f: 
                return pickle.load(f) #deserialize and return stored data
        except FileNotFoundError:
            #if the file is missing, return default data
            return default_data

    def save_data(self, filename, data):
        """
        Save the data to a file using Pickle
        Arguments:
            filename(str): Name of the file to save data to
            data(any): the data to be serialized and saved
        """

        #open the file in binary write mode and dave the data using pickle
        with open(filename, "wb") as f:
            pickle.dump(data, f) #serialize and write data to file


class WidgetCreator:
    """
    WidgetCreator class handles creating and managing Tkinter widgets for the GUI.
    It displays tasks, allows users to input grade, view rewards, adn interact with the program.
    """

    def __init__(self, root, data_manager):
        """
        Initialize the WidgetCreator with references to the root Tkinter window and DataManager
        """
        self.root = root #Main application window 
        self.data_manager = data_manager #DataManager instance for handling persistent data
        
        #Initialize donts for different UI elements
        self.banner_font, self.header_font, self.reward_font = self.create_fonts() 
        
        self.taskList = [] #List to hold checkboxes for tasks
        self.reward_buttons = None  #Frame to hold reward buttons
        self.total_points = self.data_manager.total_points  #Load persistent total points
        self.reward_cost_entries = []  #List to store entry widgets for reward costs
        self.reward_point_entries = []  #List to store manual points input fields

        self.load_images() #load images for UI elements
    

    def load_images(self):
        """
        Loads images for the GUI using Tkinter's built in PhotoImage.
        If an image error occurs, it prints and error message
        """

        try:
            self.star_img = tk.PhotoImage(file="Star.png").subsample(3,3) #Load and resize image
            self.astro_img = tk.PhotoImage(file="Astronaut.png").subsample(5,5) #load and resize image

        except Exception as e:
            #error message if image fails to load
            print(f" Unable to Load ImagesL {e}")
        

    def create_fonts(self):
        """
        Creates custom fonts for different text elements in the GUI.
        Returns:
            Tuple of font objects for banner, header, and rewards. 
        """

        #large font for banner on main window
        banner_font = tkFont.Font(family="Times New Roman", size=50, weight="bold")
        
        #medium font for section headers
        header_font = tkFont.Font(family="Times New Roman", size=20, weight="bold")

        #slightly smaller font for reward button/labels
        reward_font = tkFont.Font(family="Times New Roman", size=15, weight="bold")
        return banner_font, header_font, reward_font


    def create_banner(self):
        """
        Creates main banner for the application with the title "Star Points".
        Includes Astronaut image for visual appeal and theme.
        """

        #format the banner logo
        mainPageBanner = tk.Label(
            self.root, text="Star Points", font=self.banner_font, fg="blue", bg="light blue"
            )
        mainPageBanner.grid(row=0, column=0, columnspan=6, sticky="nesw", padx=10, pady=10)
        
        # Create a frame for the astronaut image to prevent layout shifting
        astro_frame = tk.Frame(self.root, bg="light blue")
        astro_frame.grid(row=1, column=1,columnspan=1 , sticky="e", padx=5, pady=5)

        # Load and place the astronaut image
        try:
            self.astro_img = tk.PhotoImage(file="Astronaut.png").subsample(5, 5)
            astro_label = tk.Label(astro_frame, image=self.astro_img, bg="light blue")
            astro_label.pack(anchor="e")  # Align inside the frame
        except Exception as e:
            #handle error message if image fails to load
            print(f"Error loading image: {e}")


    def create_task_complete(self, items):
        """
        Creates the task completion section of the application.
        This section includes header label and dynamic checklist.

        Parameters:  
            items(list): a lost of BooleanBar isntances with corresponding checkboxes
        """

        #create the header label that asks what the user has done today
        tasksCompletedHeader = tk.Label(
            self.root, text="What did you do today?", font=self.header_font, fg="gray", bg="light blue"
            )
        
        #call helper fucntion to create the checklist of tasks
        tasksCompletedHeader.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.create_task_checklist(items)


    def create_task_checklist(self, items):
        """
        Generates a checklist of tasks using Tkinter Checkboxes.
        Each task will have a corresponding BoolVar to track if checked off. 

        Parameters:
            items(list): a list of task descriptions
        Returns:
            list: a list of BooleanVar instances corresponding to checkboxes
        """

        taskList = [] #list to store boolean variables for each checkbox
        checkbox_frame = tk.Frame(self.root, bg="light blue") 
        checkbox_frame.grid(row=2, column=0, columnspan=6, sticky="w", padx=25, pady=10)

        #Loop through task list and create a checkbox for each task
        for item in items:
            var = tk.BooleanVar() #BoolVar to track checkbox state
            taskList.append(var) #store reference to variable

            #create checkbox and associate it with the boolean var
            checkbox = tk.Checkbutton(checkbox_frame, text=item, variable=var, bg="light blue")
            checkbox.pack(anchor="w", padx=5, pady=2) #align checkbox to the left

        #store the list of the boolean variable as an instance attribute
        self.taskList = taskList
        
        #return the list of BooleanVar instances for future use if needed
        return taskList


    def create_self_grade(self):
        """
        Creates a section where the user can enter self-assigned grade for performance.
        Grade should be a number between 1 and 10.
        """

        #label asking user to assign self grade
        selfGradeHeader = tk.Label(
            self.root, text="What grade do you give yourself? (1-10)",
             font=self.header_font, fg="gray", bg="light blue"
             )
        selfGradeHeader.grid(row=3, column=0, sticky="w", padx=10, pady=30)

        #entry widget for user to input grade
        self.selfGradeEntry = tk.Entry(self.root, width=15)
        self.selfGradeEntry.grid(row=4, column=0, sticky="w", padx=25, pady=10)

        def validate_grade():
            grade = self.selfGradeEntry.get().strip()  # Get input and remove spaces

            if not grade.isdigit():  # If input is not a number
                messagebox.showerror("Input Error", "Only enter numbers please.")
                self.selfGradeEntry.delete(0, tk.END)  # Clear incorrect input
                return

            grade = int(grade)
            if not (1 <= grade <= 10):  # If number is out of range
                messagebox.showerror("Input Error", "Enter a number between 1 and 10.")
                self.selfGradeEntry.delete(0, tk.END)

        # Button to trigger validation
        validate_button = tk.Button(
            self.root, text="Check Grade", command=validate_grade,
            font=("Times New Roman", 12, "bold"), bg="light blue"
        )
        validate_button.grid(row=4, column=1, padx=10, pady=10)

    
    def create_stats(self):
        """Creates a section displaying the "Sats" header"""

        #label for the stats section
        statsHeader = tk.Label(
            self.root, text="Stats", font=self.header_font, fg="gray", bg="light blue"
            )

        #position the stats head in the layout
        statsHeader.grid(row=1, column=5, sticky="n", padx=10, pady=10)


    def create_rewards(self):
        """
        Creates a section that displays the rewards that the user has earned.
        """

        #label that sats Earned Rewards:
        rewardsHeader = tk.Label(
            self.root, text="Earned Rewards:", font=self.header_font, fg="gray", bg="light blue"
            )
        rewardsHeader.grid(row=3, column=5, padx=10, pady=10, sticky="nesw")

        #frame to hold dynamically generated reward buttons
        self.reward_buttons = tk.Frame(self.root, bg="light blue")
        self.reward_buttons.grid(row=4, column=5, padx=10, pady=10, sticky="nesw")  # Ensure same row!


    def create_bonus(self):
        """
        Creates an entry field where user can enter bonus points.
        """
        #label prompting user to enter the bonus points
        bonusPointsHeader = tk.Label(
            self.root, text="Bonus Points: ", font=self.header_font, fg="gray", bg="light blue"
            )
        bonusPointsHeader.grid(row=6, column=0, sticky="w", padx=10, pady=10)

        #entry widget for entering bonus points
        self.bonusPoints = tk.Entry(self.root, width=15)
        self.bonusPoints.grid(row=7, column=0, sticky="w", padx=10, pady=10)


        # Validation Function
        # Validation Function
        def validate_bonus():
            bonus = self.bonusPoints.get().strip()  # Get input and remove spaces

            if not bonus.isdigit():  # If input is not a number
                messagebox.showerror("Input Error", "Only enter numbers please.")
                self.bonusPoints.delete(0, tk.END)  # Clear incorrect input
                return

            # Convert to integer (if needed later)
            bonus = int(bonus)

        # Button to trigger validation
        validate_button = tk.Button(
            self.root, text="Check Bonus", command=validate_bonus,
            font=("Times New Roman", 12, "bold"), bg="light blue"
        )
        validate_button.grid(row=7, column=1, padx=10, pady=10)


    def create_parent_button(self):
        """
        Creates a button that opens the Parent Portal when clicked.
        The Parent Portal allows parents to access specific functions.
        """

        parentButton = tk.Button(
            self.root, text="Parent Portal", command=self.open_parent_portal, 
            font=("Times New Roman", 15, "bold"), bg="light blue"
            )
        parentButton.grid(row=7, column=5, sticky="w", padx=10, pady=10)


    def create_refresh_button(self):
        """
        Creates a button that refreshes all data fields when clicked.
        """ 

        refreshButton = tk.Button(
            self.root, text="Refresh", command=self.refresh_data, 
            font=("Times New Roman", 15, "bold"), bg="light blue"
            )
        refreshButton.grid(row=7, column=4, sticky="w", padx=5, pady=10)


    def create_enter_button(self):
        """
        Creates a button that submits the entered data.
        When clicked, it collects user input, and calculates total points, 
        and updates the display.
        """

        enterButton = tk.Button(
            self.root, text="Enter", command=self.enter_data, 
            font=("Times New Roman", 15, "bold"), bg="light blue"
            )
        enterButton.grid(row=7, column=2, sticky="w", padx=30, pady=10)
    
    def create_exit_button(self):
        self.exit_button = tk.Button(
            self.root, text="Exit", font=("Times New Roman", 15, "bold"),bg="light blue",
            command=self.root.quit
            )
        self.exit_button.grid(row=7, column=5, sticky="e",padx=10, pady=10)

    def create_widgets(self):
        """
        Initializes and arranges all of the widgets in the application.
        This method calls various helper methods to create UI components.
        """

        #create main title banner
        self.create_banner()

        #retrieve list of tasks from DataManage and create task completion checkboxes
        checkbox_items = self.data_manager.tasks
        self.create_task_complete(checkbox_items)

        #create input field for self grading
        self.create_self_grade()

        #create stats section to display user points
        self.create_stats()

        #create the rewards display section
        self.create_rewards()

        #create an input field for bonus points
        self.create_bonus()

        #create buttons for various functions
        self.create_parent_button() #open parent portal
        self.create_refresh_button() #chlears input fields
        self.create_enter_button() #submits user input
        self.create_exit_button() #exits program 
 
        #label to display the user's total points
        total_points_label = tk.Label(
            self.root, text=f"Total Points: {self.total_points}",font=self.header_font,
             fg="gray", bg="light blue"
         )
        total_points_label.grid(row=2, column=5, sticky="nw", padx=10, pady=10)

        #display a star image as a visual 
        star_label = tk.Label(self.root, image=self.star_img, bg="light blue")
        star_label.grid(row=2, column=5, sticky="s", padx=10, pady=2)  # Positioned right below the label

        #create a frame to hold dynamically generated reward buttons
        self.reward_buttons = tk.Frame(self.root, bg="light blue")
        self.reward_buttons.grid(row=5, column= 5, padx=10, pady=10, sticky="e") # Ensure same row!

        #display the current rewards based on earned points
        self.display_rewards()


    def open_parent_portal(self):
        """
        Opens a new Parent Portal window, allows for parent/physician
        to view and edit task and rewards lists. 
        """
        #create a new top-level window
        parent_window = tk.Toplevel(self.root) 
        parent_window.title("Parent Portal") #set window title

        # Create labels for task list, reward list, and reward cost
        tk.Label(parent_window, text="Task List", font=self.header_font).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(parent_window, text="Rewards List", font=self.header_font).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(parent_window, text="Reward Cost (Points)", font=self.header_font).grid(row=0, column=2, padx=10, pady=10)

        #Code for displaying editable task list and rewards
        task_entries = []
        for i in range(10):
            task_entry = tk.Entry(parent_window, width=20)
            task_entries.append(task_entry)
            task_entry.grid(row=i+1, column=0, padx=10, pady=5)
            if i < len(self.data_manager.tasks):
                task_entry.insert(0, self.data_manager.tasks[i])

        #create editable fields for the rewards list and reward costs
        self.reward_cost_entries = []
        self.reward_point_entries = [] 
        for i in range(10): #allow up to 10 tasks
            reward_entry = tk.Entry(parent_window, width=20)
            self.reward_cost_entries.append(reward_entry)
            reward_entry.grid(row=i+1, column=1, padx=10, pady=5)

            #prepopulate with existing tasks, if available
            if i < len(self.data_manager.rewards):
                reward_entry.insert(0, self.data_manager.rewards[i])
            
            #entry field for reward costs
            reward_cost_entry = tk.Entry(parent_window, width=20)
            self.reward_point_entries.append(reward_cost_entry)
            reward_cost_entry.grid(row=i+1, column=2, padx=10, pady=5)

            #prepopulate with existing reward costs, if applicable
            if i < len(self.data_manager.reward_costs):
                # Display the cost for each reward
                reward_cost_entry.insert(0, str(self.data_manager.reward_costs[i]))

        save_button = tk.Button(
            parent_window, text="Save", command=lambda: self.save_entries(
                task_entries, parent_window
                ),
            font=("Times New Roman", 10, "bold")
            )
        save_button.grid(row=16, column=0, columnspan=3, pady=20)


    def save_entries(self, task_entries, parent_window):
        """
        Saves user input from the Parent Portal task and rewards lists. 
        Updates the stored task and reward data and saves it to the approp. files.

        Parameters: 
            task_entries(list): list of task entry widgets
            parent_window(TopLevel): parent portal window instance
        """

        #extract non-empty task entries for input fields
        self.data_manager.tasks = [entry.get() for entry in task_entries
         if entry.get().strip() != ""
         ]

         #extract non-empty reward names for input fields
        self.data_manager.rewards = [entry.get() for entry in self.reward_cost_entries
         if entry.get().strip() != ""
         ]

         #extract non-emtpy reward costs, ensuring valid interget conversion
        self.data_manager.reward_costs = [
            int(entry.get()) for entry in self.reward_point_entries 
            if entry.get().strip() != ""
            ]

        #save updated data to corresponding files using pickle
        self.data_manager.save_data("tasks.pkl", self.data_manager.tasks)
        self.data_manager.save_data("rewards.pkl", self.data_manager.rewards)
        self.data_manager.save_data("reward_costs.pkl", self.data_manager.reward_costs)

        #close Parent Portal window after saving
        parent_window.destroy()


    def display_rewards(self):
        """
         Displays a redeemable reward if the user has enough points.
         If multiple rewards are available, one is chosen randomly. 
         If no rewards are available at specified points, a message is displayed insted. 
        """

        # Clear previous reward button (if any)
        for widget in self.reward_buttons.winfo_children():
            widget.destroy()  # Fully remove old widgets to prevent overlapping

        # Get the list of redeemable rewards based on available points
        redeemable_rewards = [
            (reward, cost) for reward, cost in zip(self.data_manager.rewards,
             self.data_manager.reward_costs) if cost <= self.total_points
            ]

        if redeemable_rewards:
            #randomly selects one of the redeemable rewards from reward list
            reward, cost = random.choice(redeemable_rewards)

            # create and display the reward button under the "Earned Rewards" header
            button = tk.Button(self.reward_buttons, text=f"{reward} - {cost} pts", #format reward name and cost
                                # Assign function to redeem reward
                                command=lambda r=reward, c=cost: self.redeem_reward(r, c), 
                                font=self.reward_font, bg="light blue")
            button.grid(row=0, column=0, padx=10, pady=5)  # Align to the right
        else:
            #if no rewards are available, display a message 
            label = tk.Label(self.reward_buttons, text="No rewards available", 
                               font=self.reward_font, bg="light blue")
            label.grid(row=0, column=0, sticky="e", padx=10, pady=5)  # Align to the right


    def redeem_reward(self, reward, cost):
        """
        Handles the redemption of a selected award.
        """

        if self.total_points >= cost:

            #deduct the reward cost from the total available points
            self.total_points -= cost
            print(f"Redeemed {reward} for {cost} points!")
            self.update_total_points()
            self.display_rewards()  # Refresh the displayed rewards after redeeming
        else:
            #display mesage if not enought points available
            print("Not enough points to redeem this reward.")


    def update_total_points(self):
        """
        Updates the total points based of the user's activities/entries. 
        """

        #create a label to display the user's total points
        total_points_label = tk.Label(
            #dynamically update teh points value
            self.root, text=f"Total Points: {self.total_points}",
            font=self.header_font, fg="gray", bg="light blue")
        total_points_label.grid(row=2, column=5, sticky="nw", padx=10, pady=10
        )

        # Create a frame for the image to prevent layout shifting
        star_frame = tk.Frame(self.root, bg="light blue")
        star_frame.grid(row=3, column=5, columnspan=1, padx=5, pady=5)


    def refresh_data(self):
        """
        Resets the input fields and checkbozes, then refreshes the reward display.
        """

        # Clear self-entry fields by removing text input
        self.selfGradeEntry.delete(0, tk.END)

        #clear bonus points entry field by removing text input
        self.bonusPoints.delete(0, tk.END)

        #reset all checkboxes in task list to unchecked (False)
        for var in self.taskList:
            var.set(False)

        # Refresh the reward display to reflect cleared data
        self.display_rewards()


    def enter_data(self):
        """
        Handles user input for the self-grade, bonus points, and completed tasks. 
        """

        try:
            #retrieved self-grade input and convert to float
            self_grade = float(self.selfGradeEntry.get())

            #ensure that self-grade is in valid range(1-10)
            if self_grade < 0 or self_grade > 10:
                raise ValueError("Self grade must be between 0 and 10.")
        except ValueError as e:
            #handle invalid self-grade entry and display error message
            print(f"Invalid self grade: {e}")
            return

        try:
            #retrieve bonus points input and convert to float
            bonus_points = float(self.bonusPoints.get())
        except ValueError:
            #if conversion fails(empty input)- default points earned is 0
            bonus_points = 0

        #count the number of tasks that have been checked off
        checked_tasks = sum(1 for var in self.taskList if var.get())

        #calculate the total points from self-grade, bonus points, and completed tasks
        total_points = self_grade + bonus_points + checked_tasks

        #add the calculated points to the overall total points
        self.total_points += total_points

        #update the UI display to reflect the new total points
        self.update_total_points()

        #save the updated total points to a file fo persistance
        self.data_manager.save_data("total_points.pkl", self.total_points)


class StarPointsApp:
    """
    The main application class for the Star Points Application.
    """

    #placed under DataManager and WidgetCreator classes because it references them
    def __init__(self, root):
        """
        Initialized the application window and its components.
        """
        self.root = root
        self.root.geometry("1200x950")
        self.root.title("Star Points")
        self.root.configure(bg="light blue")

        #create instances of other classes 
        self.data_manager = DataManager()
        self.widget_creator = WidgetCreator(self.root, self.data_manager)

        #generate and display all widgets in the application
        self.widget_creator.create_widgets()


if __name__ == "__main__":
    """
    Entry point of the program. Ensures that script runs only
    when executed directly. Not when imported as a module for another
    script. 
    """

    root = tk.Tk() #create the main Tkinter window
    app = StarPointsApp(root) #instantiate the StarPointsApp class
    root.mainloop() #start the tkinter event loop to keep the GUI running

