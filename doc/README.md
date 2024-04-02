# Imputation of NEMSIS Dataset for Cardiac Arrest Analysis

## Project Overview

This project focuses on analyzing cardiac arrest data from the 2020 National Emergency Medical Services Information System (NEMSIS) database. The primary aim is to identify key determinants influencing patient outcomes in Intensive Care Units (ICUs) and understand the impact of urbanicity on these outcomes. The project leverages advanced data imputation techniques, including Multiple Imputation by Chained Equations (MICE) and MissForest, to address missing data points, a common challenge in real-world clinical datasets.

## Repository Contents

- **data/**: Contains all datasets required for the project, including raw data and various imputed datasets.
  - **ASCII_2020/**: The 2020 NEMSIS Datasets in ASCII format, serving as the primary data source.
    - **processeddataCA.zip**: Processed EMS data focusing on cardiac arrest cases extracted from NEMSIS.
  - **filtered_data/**: Datasets processed and filtered for analysis.
  - **Imputed_Data_MICE/**: Datasets imputed using the MICE method.
  - **Imputed_Data_MICE&MissForest/**: Datasets imputed using both MICE and Miss Forest techniques.
- **fig/**: A collection of figures and visualizations generated from the data analysis.
- **doc/**: You are here.
- **reference/**: Includes the NEMSIS data dictionary, case definitions, and other important reference materials.
- **scr/**: Contains all source code scripts used in the project.
- **eda.md**: Documentation of exploratory data analysis (EDA) results and setup instructions for reproducible analysis environments.
- **plan.md**: Outlines the project timeline and key milestones.
- **proposal.md**: A high-level description of the project's goals, methodology, and approach.
- **README.md**: Overview of the project and repository structure.
- **requirements.md**: Information about stakeholders, project background, and data sources.
- **environment.yml**: Specifies the Python dependencies for setting up the project environment.

## Key Challenges

### Handling Missing Data
- **Complexity**: Choosing the right imputation method, such as MICE or MissForest, and ensuring the imputed values were clinically relevant.
- **Bias**: Balancing the trade-offs between different imputation techniques to avoid introducing bias.

### Data Quality and Consistency
- **Data Integrity**: Ensuring consistency and accuracy across a large and complex dataset.
- **Validation**: Implementing rigorous data cleaning and validation processes.

### Computational Complexity
- **Resource Intensive**: Managing the computational load and optimization due to the size of the NEMSIS dataset and complexity of imputation methods.

### Ethical and Privacy Considerations
- **Confidentiality**: Maintaining patient privacy and adhering to health data regulations.
- **Ethical Compliance**: Ensuring the ethical handling of sensitive medical data.

## Project Link
For more details about project, please go to [Cardiac Arrest Analysis Project](https://cerko12.github.io/DS5500_Frontend/)
