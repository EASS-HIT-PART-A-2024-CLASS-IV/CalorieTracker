# Calorie Tracker

Welcome to the Calorie Tracker GitHub repository! This project provides a user-friendly interface for managing your daily meals and tracking their calorie intake. Below you will find detailed instructions on how to set up and run the application, as well as an overview of its components and technologies used.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Technologies Used](#technologies-used)

## Introduction

The Calorie Tracker is designed to help users keep track of their daily meals, including their names, calorie values, and dates. It consists of a frontend interface built with Streamlit and a backend API developed with FastAPI. Redis is used as the database for storing meal information.

## Features

- View all meals along with their calorie values and dates.
- Create new meals by providing their names and calorie values.
- Update existing meal information, including names and calorie values.
- Delete meals that are no longer needed.

## Installation

To run the Calorie Tracker locally, you need to have Docker installed on your system. Follow these steps to set up the application:

1. **Clone this GitHub repository to your local machine:**

    ```
    git clone gh repo clone EASS-HIT-PART-A-2024-CLASS-IV/CalorieTracker
    ```

2. **Navigate to the root directory of the project:**

    ```
    cd calorie-tracker
    ```

3. **Run the following command to build and start the Docker containers:**

    ```
    docker-compose up --build
    ```

4. **Once the containers are up and running, you can access the application at [http://localhost:8501](http://localhost:8501) in your web browser.**

## Usage

After launching the application, you will be presented with a user-friendly interface allowing you to navigate through different pages:

- **Home**: View all meals along with their calorie values and dates. The total calorie value is displayed, and warnings are shown if the daily recommended intake is exceeded.

- **Create Meal**: Create a new meal by providing its name and calorie value.

- **Delete Meals**: View all meals and delete those that are no longer needed.

- **Update Meals**: Update existing meal information, including names and calorie values.

## Technologies Used

The Calorie Tracker utilizes the following technologies:

- **Frontend**:
  - Streamlit: A Python library for building interactive web applications.
  - Pandas: A powerful data manipulation library for Python.
  - Requests: A Python library for making HTTP requests.

- **Backend**:
  - FastAPI: A modern, fast (high-performance), web framework for building APIs with Python.
  - Redis: An open-source, in-memory data structure store used as a database.

- **Infrastructure**:
  - Docker: A platform for developing, shipping, and running applications in containers.

Video: https://youtu.be/578IhlKqKZg
