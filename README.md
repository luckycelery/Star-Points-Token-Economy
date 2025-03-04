Star-Points-Token-Economy
The intended purpose of this program is to serve as an electronic form of a token economy. It should provide children, particularly those with autism, with a fun and engaging way to track their progress toward earning rewards through task completion. The application allows for personalization per client, helping to maintain motivation and interest.

Overarching Goals for Final Application:
•	Provide children with an engaging way to track their progress toward completing tasks and earning rewards.
•	Help children practice essential life skills, such as event recall, accountability, and self-regulation.
•	Offer a personalized approach, with options that can be tailored by parents, therapists, or teachers.
•	Allow children to see their progress in real-time, reinforcing motivation and positive behavior.
•	Give parents, therapists, or teachers an easy way to manage and adjust the task/reward system as needed.

Overview:
The Star Points Application is a Tkinter-based GUI program designed to help users track tasks, assign self-grades, earn rewards, and access a Parent Portal for managing task and reward lists. The program implements validation for secure input handling and offers an intuitive, user-friendly experience.
Features:
•	Task tracking system with checkboxes for completed tasks
•	Self-grading functionality for progress evaluation
•	Bonus point entry with validation to ensure numeric input
•	Parent Portal for managing tasks and rewards
•	Reward redemption system based on earned points
•	Secure input handling with validation checks

Installation Instructions:
•	Ensure you have Python 3.x installed on your system.
•	Install Tkinter (comes pre-installed with standard Python distributions).
•	Download or clone the project files from the GitHub repository.
•	Ensure required images (e.g., Astronaut.png) are in the same directory as the Python script.
•	Run the script using: python star_points.py

How to Use the Application:
•	Launching the Program: Run the Python script to open the main application window.
•	Completing Tasks: Check off completed tasks to track progress.
•	Self-Grading: Enter a self-grade to assess performance.
•	Earning Bonus Points: Input valid numeric values in the Bonus Points field.
•	Redeeming Rewards: Earn enough points to unlock and redeem rewards.
•	Using the Parent Portal: Access and update tasks, rewards, and costs.
•	Saving Changes: Save modifications in the Parent Portal to update stored data.

Validation and Error Handling:
•	The Bonus Points entry only accepts numeric input; invalid entries trigger an error message.
•	The Self-Grade entry also ensures valid numeric input.
•	The Parent Portal prevents blank task/reward entries from being saved.
•	All user input is validated to maintain secure and error-free functionality.
