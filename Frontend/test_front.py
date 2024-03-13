import pytest
from unittest.mock import patch
import streamlit as st
import streamlitFront

@pytest.fixture
def mock_requests_post():
    with patch("requests.post") as mock_post:
        yield mock_post

@pytest.fixture
def mock_streamlit_text_input():
    with patch("streamlit.text_input") as mock_text_input:
        yield mock_text_input

@pytest.fixture
def mock_streamlit_number_input():
    with patch("streamlit.number_input") as mock_number_input:
        yield mock_number_input

@pytest.fixture
def mock_streamlit_button():
    with patch("streamlit.button") as mock_button:
        yield mock_button

@pytest.fixture
def mock_streamlit_success():
    with patch("streamlit.success") as mock_success:
        yield mock_success

def test_display_create_meal(mock_streamlit_text_input, mock_streamlit_number_input,
                             mock_streamlit_button, mock_requests_post, mock_streamlit_success, mock_streamlit_error):

    mock_streamlit_text_input.return_value = "Grilled Salmon"
    mock_streamlit_number_input.return_value = 350.0

    mock_streamlit_button.return_value = True

    mock_requests_post.return_value.json.return_value = {"meal_id": 123}

    mock_streamlit_success.return_value = None

    with patch("app.display_create_meal"):
        streamlitFront.display_create_meal()

    # Assertions
    mock_streamlit_text_input.assert_called_once_with("Meal Name")
    mock_streamlit_number_input.assert_called_once_with("Calories", min_value=0.0)
    mock_streamlit_button.assert_called_once()
    mock_requests_post.assert_called_once_with(f"{streamlitFront.FASTAPI_BASE_URL}/meals", json={"text": "Grilled Salmon", "cal_value": 350.0})
    mock_streamlit_success.assert_called_once_with("Meal created successfully.")

if __name__ == '__main__':
    pytest.main()
