# Amazon Bestsellers Analysis

This project analyzes Amazon bestsellers data from the `Amazon_bestsellers_items_2025.csv` file and presents the findings in an interactive dashboard.

## Files

*   `Amazon_bestsellers_items_2025.csv`: The dataset containing the Amazon bestsellers items.
*   `Analysis.ipynb`: A Jupyter notebook for exploratory data analysis.
*   `dashboard.py`: A Python script to create an interactive dashboard to visualize the data.
*   `requirements.txt`: A list of Python packages required to run the project.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

*   **To run the analysis:**
    Open and run the `Analysis.ipynb` notebook in a Jupyter environment.

*   **To launch the dashboard:**
    ```bash
    python dashboard.py
    ```
    The dashboard will be available at `http://127.0.0.1:8050/` in your web browser.
