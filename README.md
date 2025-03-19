### Guide on How to Make a Pull Request

Follow these detailed steps to contribute to the repository:

1. **Clone the Repository**  
   - Open your terminal and run the following command to clone the repository:  
     ```bash
     git clone https://github.com/MyRockae/QuizGenAI.git
     ```
   - Navigate to the repository directory:  
     ```bash
     cd QuizGenAI
     ```

2. **Create a Descriptive Folder for Your Work**  
   - Within the cloned repository, create a new folder that clearly reflects the purpose of your contribution.  
   - **Example:** For a module that downloads files over FTP, name the folder `test_module_to_download_files_over_ftp`.

3. **Add Your Files**  
   - Place your Jupyter Notebook (`.ipynb`) and any supporting files into the new folder.  
   - Ensure your files are organized and well-documented so that reviewers can understand your contribution.

4. **Create a Feature Branch**  
   - Before making any changes, create a new branch to isolate your work from the main branch:  
     ```bash
     git checkout -b feature/test_module_to_download_files_over_ftp
     ```

5. **Stage and Commit Your Changes**  
   - Stage all your changes by running:  
     ```bash
     git add .
     ```
   - Commit your changes with a clear, descriptive commit message:  
     ```bash
     git commit -m "Add module to download files over FTP with Jupyter Notebook implementation"
     ```

6. **Push Your Feature Branch to the Remote Repository**  
   - Push your branch to GitHub:  
     ```bash
     git push origin feature/test_module_to_download_files_over_ftp
     ```

7. **Create a Pull Request (PR)**  
   - Go to the GitHub repository page and navigate to the "Pull Requests" tab.
   - Click on "New Pull Request."
   - Select your feature branch (`feature/test_module_to_download_files_over_ftp`) as the source and the main branch as the target.
   - Provide a detailed description of your changes, the purpose behind them, and any additional context that might help reviewers understand your work.

8. **Wait for Review and Approval**  
   - Once your pull request is submitted, wait for the project maintainers to review your changes.
   - Be responsive to any feedback or requested modifications until your PR is approved and merged.
