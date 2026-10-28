import pandas as pd
import os

# Step 1: Load the cleaned dataset
df = pd.read_csv(
    "data/processed/cleaned_restaurants.csv",
    encoding="latin1"
)

# Step 2: Convert rating and cost columns to numeric values
df["aggregate_rating"] = pd.to_numeric(
    df["aggregate_rating"], errors="coerce"
)

df["average_cost_for_two"] = pd.to_numeric(
    df["average_cost_for_two"], errors="coerce"
)

# Step 3: Create a dataset containing restaurants with ratings
rated_df = df.dropna(subset=["aggregate_rating"]).copy()

# Step 4: Analyze average ratings by city
city_ratings = (
    rated_df.groupby("city")
    .agg(
        average_rating=("aggregate_rating", "mean"),
        restaurant_count=("restaurant_id", "size")
    )
    .reset_index()
)

city_ratings = city_ratings.sort_values(
    "average_rating",
    ascending=False
)

print("\n--- TOP 10 CITIES BY AVERAGE RATING ---")
print(city_ratings.head(10))

# Step 5: Analyze ratings by cuisine
# The dataset's cuisines column contains cuisine names.
cuisine_ratings = (
    rated_df.dropna(subset=["cuisines"])
    .groupby("cuisines")
    .agg(
        average_rating=("aggregate_rating", "mean"),
        restaurant_count=("aggregate_rating", "size")
    )
    .reset_index()
)

cuisine_ratings = cuisine_ratings.sort_values(
    "average_rating",
    ascending=False
)

print("\n--- TOP 10 CUISINES BY AVERAGE RATING ---")
print(cuisine_ratings.head(10))

# Step 6: Analyze the relationship between cost and rating
cost_rating = rated_df[
    ["average_cost_for_two", "aggregate_rating"]
].dropna()

print("\n--- COST AND RATING CORRELATION ---")
print(cost_rating.corr())

# Step 7: Analyze restaurant locations by city
location_summary = (
    df.dropna(subset=["latitude", "longitude"])
    .groupby("city")
    .agg(
        restaurant_count=("restaurant_id", "size"),
        avg_latitude=("latitude", "mean"),
        avg_longitude=("longitude", "mean")
    )
    .reset_index()
)

print("\n--- RESTAURANT LOCATION SUMMARY ---")
print(location_summary.head(10))

# Step 8: Save analysis results
os.makedirs("outputs", exist_ok=True)

city_ratings.to_csv(
    "outputs/city_ratings.csv",
    index=False
)

cuisine_ratings.to_csv(
    "outputs/cuisine_ratings.csv",
    index=False
)

location_summary.to_csv(
    "outputs/city_restaurant_counts.csv",
    index=False
)

cost_rating.to_csv(
    "outputs/cost_rating_analysis.csv",
    index=False
)

print("\nAnalysis completed successfully!")
print("All analysis files have been saved in the outputs folder.")

