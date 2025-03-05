import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset (replace 'your_data.csv' with actual file)
df = pd.read_csv("/Users/brandonlee/PycharmProjects/Badminton_Racket_Analysis/data/RestringLog.csv")

# 1. Basic Descriptive Statistics
print("Unique Players:", df['NameId'].nunique())
print("Unique Rackets:", df['RacketId'].nunique())
print("Unique Strings:", df['StringId'].nunique())

# Most popular rackets and strings
top_rackets = df['Racket'].value_counts().head(10)
top_strings = df['String'].value_counts().head(10)

print("\nTop Rackets:\n", top_rackets)
print("\nTop Strings:\n", top_strings)

# Average string tension per racket
avg_tension_racket = df.groupby("Racket")["Tension"].mean().sort_values(ascending=False)
print("\nAverage Tension by Racket:\n", avg_tension_racket.head(10))

# 2. Visualizations

# Tension Distribution
plt.figure(figsize=(8,5))
sns.histplot(df["Tension"], bins=20, kde=True)
plt.xlabel("String Tension (lbs)")
plt.ylabel("Frequency")
plt.title("Distribution of String Tension")
plt.show()

# Top Racket Usage
plt.figure(figsize=(10,5))
sns.barplot(x=top_rackets.index, y=top_rackets.values)
plt.xticks(rotation=45)
plt.xlabel("Racket")
plt.ylabel("Count")
plt.title("Top 10 Most Used Rackets")
plt.show()

# Top String Usage
plt.figure(figsize=(10,5))
sns.barplot(x=top_strings.index, y=top_strings.values)
plt.xticks(rotation=45)
plt.xlabel("String")
plt.ylabel("Count")
plt.title("Top 10 Most Used Strings")
plt.show()

# 3. Outlier Detection (Boxplot)
plt.figure(figsize=(8,5))
sns.boxplot(x=df["Tension"])
plt.xlabel("String Tension (lbs)")
plt.title("Boxplot of String Tension")
plt.show()

# Identify outliers
Q1 = df["Tension"].quantile(0.25)
Q3 = df["Tension"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["Tension"] < lower_bound) | (df["Tension"] > upper_bound)]
print("\nOutliers in String Tension:\n", outliers)

