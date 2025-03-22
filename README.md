# Backend.AIGenerator.WebJob

## Overview
an asynchronous service that processes file uploads, extracts text content using OCR, and interfaces with external LLM APIs to generate quizzes, flashcards, and other interactive educational content, ensuring efficient file handling and reliable data transfer to third-party AI services for real-time content generation.

## Database Schema Details

For comprehensive details on the database schema, please refer to the [Database Schema Documentation](https://github.com/MyRockae/Rockae.Domain.WebAPI/blob/main/BackendSchema.md).

## What technologies are used for this project?

This project is built with .

- Python
- Django
- Django rest-framework

Below is a set of step-by-step instructions in Markdown format that you can add directly to your README or another documentation file. These steps cover creating a feature branch, pushing your changes, and then creating a pull request (PR) on GitHub.

---




## How to Push Changes Using a Feature Branch and Create a Pull Request

1. **Clone the Repository (if you haven’t already):**  
   Open your terminal and run:  
   ```bash
   git clone https://github.com/MyRockae/Backend.AIGenerator.WebJob.git
   cd Rockae.Domain.WebAPI
   ```

2. **Create a New Feature Branch:**  
   Create and switch to a new branch for your feature. Replace `your-feature-name` with a descriptive name for your feature.
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes and Save Your Work:**  
   Edit your code locally. When you are ready, stage your changes with:
   ```bash
   git add .
   ```
   *(Tip: You can replace the dot (`.`) with specific file names if you don’t want to add everything.)*

4. **Commit Your Changes:**  
   Commit your staged changes with a meaningful commit message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

5. **Push Your Feature Branch to GitHub:**  
   Push your branch and set the upstream branch:
   ```bash
   git push -u origin feature/your-feature-name
   ```

6. **Create a Pull Request (PR) on GitHub:**  
   - Open your web browser and navigate to your repository: [https://github.com/MyRockae/Backend.AIGenerator.WebJob](https://github.com/MyRockae/Backend.AIGenerator.WebJob)
   - You should see a prompt to create a pull request for your recently pushed branch. Click **"Compare & pull request"**.
   - Fill in the title and description for your PR, then click **"Create pull request"**.

7. **Review and Merge:**  
   Once the PR is created, it can be reviewed by our team. After approval, the changes can be merged into the main branch and the CICD pipline would automatically update the production app.

---
