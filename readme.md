# Clicker 6000

Clicker 6000 is an automation tool that simulates mouse clicks at specified intervals. It allows for automated clicking at predefined locations on your screen, with options for customizing the click behavior (e.g., left or right clicks, single or double clicks).

## Features

- Set click interval (hours, minutes, seconds, milliseconds).
- Choose between left or right mouse button.
- Option for single or double-click mode.
- Record and save multiple locations for automated clicking.
- Infinite or repeatable click options.
- Easy-to-use graphical interface built with Tkinter.

## How to Use

1. **Set the Click Interval**:
   - **Hours**: Enter the number of hours between clicks (optional).
   - **Minutes**: Enter the number of minutes between clicks (optional).
   - **Seconds**: Enter the number of seconds between clicks. (optional)
   - **Milliseconds**: Enter the number of milliseconds between clicks.

2. **Choose the Click Behavior**:
   - **Button**: Select the mouse button to use for the clicks:
     - **Left**: Left mouse button click.
     - **Right**: Right mouse button click.
   - **Mode**: Select the type of click:
     - **Single**: A single click.
     - **Double**: A double click.

3. **Record Locations**:
   - Click on **"Add"** to add a new location where the click will occur.
   - To record the location, click on **"Pick"** then click on your target location. The X and Y coordinates will be recorded.
   - To remove a location, click on **"Remove"** next to the recorded location.
   - You can add multiple locations if you need clicks at different spots on the screen.

4. **Set the Repeat Options**:
   - **Repeat Count**: Enter the number of times you want to repeat the clicks.
   - **Infinite**: Toggle this setting to make the clicks repeat indefinitely. Click **ON** for infinite clicks, or **OFF** to set a specific repeat count.

5. **Start and Stop the Clicker**:
   - Click **"START"** to begin the automated clicking. The program will simulate the clicks at the specified intervals and locations.
   - To stop the clicking process, click **"STOP"**.

6. **Notes**:
   - The program will run in the background, so avoid using the mouse during the clicking process.
   - If you want to change the interval or locations while it's running, stop the process, make your changes, and then restart it.
