# RMIT - ANZ: ESG Automation 

This repository comprises the coursework for PGRD Data Science project, as part of the Master of Data Science syllabus at RMIT University.

## Background

We are tasked with working with the Australia and New Zealand Banking group (ANZ). They are one of the Big Four Banks in Australia with operations in retail and commercial banking. The Client Insights and solutions team at ANZ works to provide customers with insights across different operating domains to make better decisions.

This knowledge-based approach with clients leads to the need of reports for different sectors across a variety of performance metrics. The Insights team released a paper in 2022 that focused on emerging ESG trends (Environmental, Social and Governance) in the Retail Industry. ESG refers to the overall framework a company uses to assess their impact on the environment and society at large and looks at the different methods they have adopted to improve their practices.
 
The current process consists of exhaustive and time-consuming manual interpretation of reports from each corporation. The interpreted data is then collated into a sheet where the common themes are identified. Each corporation’s performance on each metric for that year is then recorded. An analyst then works to aggregate and consolidate the data before extracting valuable insights.

## Aim

The goal of this project is to transition to AI driven approaches by gathering and evaluating the ESG data of the retail industry and streamline the process for client insights and solution team. This will allow the CIS team to focus more on the important insights gained from the automation.
 
Our team will be focusing on automating the step where CIS team manually goes through the reports and will help them find the recurring themes and goals associated with the selected ESG category in the form of excel.

## Proposed Solution

![Proposed Solution](Images/ProposedSolution.png)

## Project Structure

```text
|-- Images
|   `-- ProposedSolution.png            # Image illustrating the proposed solution for the project.

|-- NotebookScripts
|   |-- mvp_v1_similarity.py            # Script for calculating similarity metrics, version 1 of the MVP (Minimum Viable Product).
|   |-- mvp_v2_similarity.py            # Script for calculating similarity metrics, version 2 of the MVP.
|   `-- pdf_parser.py                   # Script for parsing PDF documents to extract relevant data.

|-- Notebooks
|   |-- MVP_V1_Analysis.ipynb           # Jupyter notebook analyzing data and results for MVP version 1.
|   |-- MVP_V2_Analysis.ipynb           # Jupyter notebook analyzing data and results for MVP version 2.
|   |-- POC_Analysis.ipynb              # Jupyter notebook for proof-of-concept analysis.
|   |-- Regex_Analysis.ipynb            # Jupyter notebook analyzing regular expressions used in the project.
|   |-- Sentence_Parser_Analysis.ipynb  # Jupyter notebook analyzing sentence parsing techniques.
|   `-- Validation_Template.ipynb       # Jupyter notebook template for validating data and results.

|-- README.md                           # Markdown file providing an overview and instructions for the project.

|-- Resources
|   |-- ANZ_RMIT_Automating_ESG_Analysis.pptm            # PowerPoint presentation on automating ESG analysis.
|   |-- CIS Retail Paper -Company Annual Reports.docx    # Word document on retail paper and company annual reports.
|   |-- ESG - Circular Economy framework analysis.xlsx   # Excel sheet analyzing the circular economy framework in ESG.
|   |-- Progress_Report-1.pptx                           # PowerPoint presentation detailing the project's progress.
|   `-- Sus Fin Data Sheet - UPDATED.xlsx                # Updated Excel sheet with sustainable finance data.

|-- SampleReports
|   |-- 2022_BBunting_Report.pdf        # PDF report for Baby Bunting for the year 2022.
|   |-- 2022_HNorman_Report.pdf         # PDF report for Harvey Norman for the year 2022.
|   |-- 2023_Coles_Report.pdf           # PDF report for Coles for the year 2023.
|   `-- 2023_KMD_Report.pdf             # PDF report for Kathmandu for the year 2023.

|-- app.py                              # Main application script for running the project.

|-- input                               # Directory intended for input files (currently empty).

|-- script.py                           # Script containing additional functionality or utilities for the project.

|-- static
|   |-- esg_final.jpg                   # Image file used in the project's frontend.
|   `-- styles.css                      # CSS file for styling the project's frontend.

|-- templates
    |-- login.html                      # HTML template for the login page.
    |-- pdfParser.html                  # HTML template for the PDF parser page.
    |-- registration.html               # HTML template for the registration page.
    `-- results.html                    # HTML template for the results page.

9 directories, 28 files
```
