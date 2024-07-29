**Download [this](https://drive.google.com/file/d/1NuMuKesm0MWbZyFDapbVqx45EE8SVGbd/view?usp=sharing) Safetensor file and place it in the fine_tuned_model folder.**

Job Matching System

Overview

This application allows you to upload candidate data and query job descriptions to find the most relevant candidates. It consists of a React frontend and a Flask backend.

Prerequisites

    Node.js and npm (for React)
    Python and pip (for Flask)
    MongoDB (for database)
    Elasticsearch (for search engine)

Getting Started

Backend Setup

1.Clone the Repository:

    git clone https://github.com/sameer-suman/Interactly_SameerSuman.git
  
2.Install Python Dependencies:

    cd <repository-folder>
    pip install -r requirements.txt

3.Set Up MongoDB:
    
    Ensure MongoDB is installed and running. The Flask backend will connect to the MongoDB instance.

4.Set Up Elasticsearch:

    Ensure Elasticsearch is installed and running. The Flask backend will connect to the Elasticsearch instance.

5.Run the Flask Application:

    python app.py
    The Flask server will start and listen on http://localhost:5000.

Frontend Setup

1.Navigate to the Frontend Directory:
      
      cd job-matching-frontend

2.Install Node.js Dependencies:

      npm install

3.Run the React Application:
  
      npm start

    The React application will start and open in your default web browser at http://localhost:3000.

Usage

Upload Candidates Data

    Click on the "Upload Candidates Data" section.
    Choose a xlsx file containing the candidate data.
    Click the "Upload" button to send the file to the backend.

Query Job Description

    Enter a job description in the provided text area.
    Click the "Query" button to retrieve the top candidates based on the job description.
    The results will be displayed in an overlay with a close button.

Clear Data

    Click the "Clear Data" button to remove all candidates from the backend.

Notes

    Ensure the Flask server is running before starting the React application.
    The React application is set up to interact with the Flask server running on http://localhost:5000.
    Make sure MongoDB and Elasticsearch are running before starting the Flask application.

License

This project is licensed under the MIT License.
