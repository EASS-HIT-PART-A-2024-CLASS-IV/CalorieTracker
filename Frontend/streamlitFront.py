import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

FASTAPI_BASE_URL = "http://backend:8000"

def main():
    st.title("Calorie Tracker App")

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Select a page", ["Home", "Create Meal", "Delete Meals", "Update Meals"])

    if page == "Home":
        display_home()
    elif page == "Create Meal":
        display_create_meal()
    elif page == "Delete Meals":
        display_delete_meals()
    elif page == "Update Meals":
        display_update_meals()


RECOMMENDED_CALORIES_PER_DAY = 2500

def display_home():
    st.subheader("Here you can view your meals.")


    response = requests.get(f"{FASTAPI_BASE_URL}/meals")
    meals = response.json()

    if meals:

        meals_df = pd.DataFrame(meals)
        meals_df = meals_df[['text', 'cal_value', 'date']]

        meals_df.index = meals_df.index + 1
        meals_df = meals_df.rename(columns={'text': 'Food', 'cal_value': 'Calorie value', 'date': 'Date'})

        st.table(meals_df)

        total_calories = meals_df['Calorie value'].sum()
        st.success(f"Total Calorie Value: {total_calories} calories")

        if total_calories >= 3000:
            st.warning("Warning: You are above the recommended calorie intake per day!")

        elif total_calories >= RECOMMENDED_CALORIES_PER_DAY:
            st.error("Attention: You are at the recommended calorie intake per day.")

    else:
        st.warning("No meals found.")

def display_create_meal():
    st.header("Create a New Meal")

    text = st.text_input("Meal Name")
    cal_value = st.number_input("Calories", min_value=0.0)

    if st.button("Create Meal"):
        payload = {"text": text, "cal_value": cal_value}
        response = requests.post(f"{FASTAPI_BASE_URL}/meals", json=payload)

        if 'meal_id' in response.json():
            st.success(f"Meal created successfully on {datetime.now().strftime('%d/%m/%Y')}!")
        else:
            st.error("Failed to create meal. Check the response for details.")


def display_delete_meals():
    st.header("View All Meals")

    response = requests.get(f"{FASTAPI_BASE_URL}/meals")
    meals = response.json()

    if not meals:
        st.warning("No meals found.")
    else:
        meals_sorted = sorted(meals, key=lambda x: x['meal_id'])

        for meal in meals_sorted:
            st.write(f"{meal['text']}, Calories: {meal['cal_value']}")

            delete_button_key = f"delete_button_{meal['meal_id']}"

            if st.button("Delete", key=delete_button_key):
                delete_response = requests.delete(f"{FASTAPI_BASE_URL}/meals/{meal['meal_id']}")
                if 'message' in delete_response.json() and "deleted" in delete_response.json()["message"]:
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to delete meal {meal['meal_id']}. Check the response for details.")

def display_update_meals():
    st.header("Update Meal Information")

    response = requests.get(f"{FASTAPI_BASE_URL}/meals")
    meals = response.json()
    if not meals:
        st.warning("No meals found.")

    else:
        meal_options = {f"{meal['text']} (Calories: {meal['cal_value']})": meal['meal_id'] for meal in meals}

        selected_meal = st.selectbox("Select Meal to Update", list(meal_options.keys()))

        meal_id = meal_options[selected_meal]

        selected_meal_name, selected_meal_calories = selected_meal.split('(Calories: ')
        selected_meal_calories = float(selected_meal_calories[:-1])

        new_text = st.text_input("New Meal Name", value=selected_meal_name.strip())
        new_cal_value = st.number_input("New Calorie Value", value=selected_meal_calories, min_value=0.0, step=0.1)

        if st.button("Update Meal"):
            data = {
                "text": new_text,
                "cal_value": new_cal_value
            }

            response = requests.put(f"{FASTAPI_BASE_URL}/meals/{meal_id}", json=data)

            if response.status_code == 200:
                st.success(f"Meal '{selected_meal_name.strip()}' updated successfully.")
            elif response.status_code == 404:
                st.error(f"Meal '{selected_meal_name.strip()}' not found. Please select a valid meal.")
            elif response.status_code == 422:
                st.error(f"Invalid data provided. Check the input values.")
            else:
                st.error(f"Error updating meal. Status code: {response.status_code}. Check the response for details.")



if __name__ == "__main__":
    main()
