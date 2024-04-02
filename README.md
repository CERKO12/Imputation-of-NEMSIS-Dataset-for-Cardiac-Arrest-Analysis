# Imputation of NEMSIS Dataset for Cardiac Arrest Analysis

## Overview
The core objective of this project is to impute the EMS data from the National Emergency Medical Services Information System (NEMSIS) in order to find predictors that can forecast cardiac arrest outcomes in ICU patients by urbanicity/rurality. More specifically:
  * Appraise different data imputation methodologies, primarily focusing on MICE and MissForest.
  * Set the groundwork for subsequent modeling of prediction of cardiac arrest patients' outcomes are good or poor.

## Table of Contents
* data: The data sets required for this project and the imputed data sets.
  * ASCII_2020: 2020 NEMSIS Datasets
    * processeddataCA.zip: EMS data of NEMSIS.
  * filtered_data: Processed datasets by scripts.
  * Imputed_Data_MICE: Imputed datasets by using MICE.
  * Imputed_Data_MICE&MissForest: Imputed datasets by using MICE and Miss Forest.
* fig: Figures used for analysis in this project.
* reference: NEMSIS data dictionary, case definition and other relevant materials.
* scr: Source code.
* eda.md: Instructions of reproducible environments and exploratory data analysis results.
* plan.md: Timelines of the project.
* proposal.md: The high-level project description and approach.
* README.md: Project overview and table of contents.
* requirements.md: Information of stakeholders, project backgrounds, and data source.
* environment.yml: Python dependencies

## Collaborations
* Guidance from Dr. Christine Lary and Dr. Qingchu Jin (primary POC) at The Roux Institute
* Connection with Dr. Teresa May at MaineHealth

## Resources & Data
* Original data source: [NEMSIS Database](https://www.nemsis.org/)
* A subset of the entire database is available via scientists at The Roux Institute.
  * filename: "processeddataCA.zip"
  * size: 55,649,704 bytes

## Environments
Install miniconda or anaconda for reproducible environment.
