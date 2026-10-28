import pandas as pd
import os

# Define file paths

input_file = "zomato1.csv"
output_folder = "data/processed"
output_file = os.path.join(output_folder, "cleaned_restaurants.csv")

def clean_data():
    try:
        # Check whether the dataset exists
        if not os.path.exists(input_file):
            print("ERROR: zomato1.csv was not found.")
            print("Place the CSV file in the main project folder.")
            return

        # Load the dataset
        print("Loading dataset...")
        df = pd.read_csv(input_file, encoding="latin1")

        print("Dataset loaded successfully!")
        print("Original dataset shape:", df.shape)

        # Display column names
        print("\nDataset columns:")
        print(df.columns.tolist())

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Standardize column names
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(r"\s+", "_", regex=True)
        )

        # Create output folder
        os.makedirs(output_folder, exist_ok=True)

        # Save cleaned dataset
        df.to_csv(output_file, index=False)

        print("\nCleaning completed successfully!")
        print("Rows after removing duplicates:", len(df))
        print("Output file:", output_file)

    except Exception as error:
        print("\nAn error occurred:", error)

if __name__ == "__main__":
    clean_data()
