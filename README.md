Here's a step-by-step guide for users on how to download your repository and run the script in their terminal:
Installation Guide for Instagram Profile Data Grabber

Follow these steps to download and run the Instagram Profile Data Grabber:
Prerequisites

    Python 3.x: Ensure you have Python installed on your system. You can download it from python.org.
    Pip: This is usually included with Python. If you need to install it, refer to the pip installation guide.

Step 1: Clone the Repository

Open your terminal (Command Prompt, PowerShell, or Terminal) and run the following command to clone the repository:

bash

    git clone https://github.com/furkhad/Instagram-Profile-Data-Grabber.git


Replace yourusername and your-repo-name with your actual GitHub username and repository name.
Step 2: Navigate to the Project Directory

Change to the directory of the cloned repository:

bash

    cd Instagram-Profile-Data-Grabber

Step 3: Install Instaloader

Make sure you have the Instaloader library installed. Run the following command:

bash

    sudo apt install python3-pip python3-venv
    python3 -m venv venv
    source venv/bin/activate
    pip install instaloader

Step 4: Run the Script

Now, you can run the script using the following command:

bash

     python main.py

When prompted, enter the Instagram username you want to gather data for.
Step 5: View the Results

After running the script, you will see the extracted data displayed in the terminal, and any downloaded content will be saved in the project directory.
