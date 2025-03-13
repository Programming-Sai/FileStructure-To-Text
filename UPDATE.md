This issue describes the addition of two new features for the **FileStructure-To-Text** Python project.

#### Feature 1: Skipping Files/Folders in the Display

- Add functionality that allows the user to specify a list of files or folders to skip when generating the folder structure. This list will be provided as a configuration (either through a file or command-line argument), and the script will exclude these files or folders from the display.

#### Feature 2: Template-Based Folder Structure Generation

- Implement a system where the user can define a folder structure in a text file. When the user runs the `ftt` command in an empty folder, the command will read the text file, and based on the structure defined inside it, the script will generate the corresponding folder structure.
- The user should be able to define the folder structure in a format similar to the following example:

  ```
  water-quality-prediction/
  ├── data/
  │   └── water_quality.csv        # The dataset
  ├── notebooks/
  │   └── data_exploration.ipynb   # For data exploration and visualization
  │   └── model_building.ipynb     # For training the model
  ├── src/
  │   ├── train.py                 # Training script
  │   ├── predict.py               # Prediction script
  │   └── utils.py                 # Utility functions
  ├── models/
  │   └── water_quality_model.pkl  # Saved model file
  ├── app/
  │   ├── app.py                   # Flask app for deployment
  │   └── templates/               # (Optional) HTML templates for the app
  ├── requirements.txt             # Python dependencies
  └── README.md
  ```

- After defining this structure, the user can run the `ftt` command in an empty folder, and the script will generate the corresponding folder structure, including the files, based on the template.

#### Steps to Implement:

- Add a `skip_files` or `skip_folders` option to the `ftt` command for excluding specific files and folders.
- Potentially a `.fttignore` file.
- Create a new function to read and parse a folder structure template file.
- Modify the script to generate the folder structure as defined in the template when the user runs the command in an empty folder.

#### Acceptance Criteria:

- The user can skip specific files or folders from the folder structure display using a list or configuration file.
- The user can define a folder structure template in a text file.
- Running the `ftt` command in an empty folder will generate the folder structure from the template.
---