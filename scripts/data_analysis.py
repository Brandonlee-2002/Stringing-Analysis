import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.core.algorithms import nunique_ints


# Load dataset
df = pd.read_csv("data/RestringLog.csv")

# Start of Markdown Summary
summary_lines = []

# 1. Basic Descriptive Statistics
unique_players = df['NameID'].nunique()
unique_rackets = df['RacketID'].nunique()
unique_strings = df['StringID'].nunique()

summary_lines.append(f"#Stringing Analysis Summary\n")
summary_lines.append(f"**Unique Players:** {unique_players}")
summary_lines.append(f"**Unique Rackets:** {unique_rackets}")
summary_lines.append(f"**Unique Strings:** {unique_strings}\n")

# Most popular rackets and strings
top_rackets = df['Racket'].value_counts().head(10)
top_strings = df['String'].value_counts().head(10)

summary_lines.append("## 🏸 Top 10 Most Used Rackets\n")
summary_lines.append(top_rackets.to_markdown())

summary_lines.append(("## 🧵Top 10 Most Used Strings\n"))
summary_lines.append(top_strings.to_markdown())

# Average string tension per racket
avg_tension_racket = df.groupby("Racket")["Tension"].mean().sort_values(ascending=False)
summary_lines.append("\n## 📈 Average String Tension by Racket (Top 10)\n")
summary_lines.append(avg_tension_racket.head(10).to_frame().to_markdown())

# 2. Visualizations

# Tension Distribution
plt.figure(figsize=(8,5))
sns.histplot(df["Tension"], bins=20, kde=True)
plt.xlabel("String Tension (lbs)")
plt.ylabel("Frequency")
plt.title("Distribution of String Tension")
plt.savefig("images/tension_distribution.png")

# Top Racket Usage
plt.figure(figsize=(10,5))
sns.barplot(x=top_rackets.index, y=top_rackets.values)
plt.xticks(rotation=45)
plt.xlabel("Racket")
plt.ylabel("Count")
plt.title("Top 10 Most Used Rackets")
plt.savefig("images/top_rackets.png")

# Top String Usage
plt.figure(figsize=(10,5))
sns.barplot(x=top_strings.index, y=top_strings.values)
plt.xticks(rotation=45)
plt.xlabel("String")
plt.ylabel("Count")
plt.title("Top 10 Most Used Strings")
plt.savefig("images/top_strings.png")

# 3. Outlier Detection (Boxplot)
plt.figure(figsize=(8,5))
sns.boxplot(x=df["Tension"])
plt.xlabel("String Tension (lbs)")
plt.title("Boxplot of String Tension")
plt.savefig("images/boxplot_tension.png")

# Identify outliers
Q1 = df["Tension"].quantile(0.25)
Q3 = df["Tension"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["Tension"] < lower_bound) | (df["Tension"] > upper_bound)]
summary_lines.append(f"\n## ⚠️ Tension Outliers\n")
summary_lines.append(f"Total Outliers Detected: **{len(outliers)}**")

# 5. Gender Comparison Visualizations
os.makedirs("images/gender_comparison", exist_ok=True)

# Ensure 'Gender' exists
if "Gender" in df.columns:

    # Tension Distribution KDE by Gender (Overlayed)
    plt.figure(figsize=(8, 5))
    for gender in df["Gender"].dropna().unique():
        sns.kdeplot(df[df["Gender"] == gender]["Tension"], label=gender, fill=True)
    plt.xlabel("String Tension (lbs)")
    plt.ylabel("Density")
    plt.title("Tension Distribution by Gender")
    plt.legend()
    plt.savefig("images/gender_comparison/tension_distribution_by_gender.png")
    plt.close()

    # Grouped Bar Chart: Top Rackets by Gender
    top_rackets_gender = (
        df.groupby(["Gender", "Racket"]).size().reset_index(name="Count")
    )
    top_rackets_overall = df["Racket"].value_counts().head(5).index.tolist()
    top_rackets_gender_filtered = top_rackets_gender[
        top_rackets_gender["Racket"].isin(top_rackets_overall)
    ]

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=top_rackets_gender_filtered,
        x="Racket",
        y="Count",
        hue="Gender"
    )
    plt.title("Top 5 Rackets Used by Gender")
    plt.xlabel("Racket")
    plt.ylabel("Usage Count")
    plt.legend(title="Gender")
    plt.savefig("images/gender_comparison/top_rackets_by_gender.png")
    plt.close()

    # Grouped Bar Chart: Top Strings by Gender
    top_strings_gender = (
        df.groupby(["Gender", "String"]).size().reset_index(name="Count")
    )
    top_strings_overall = df["String"].value_counts().head(5).index.tolist()
    top_strings_gender_filtered = top_strings_gender[
        top_strings_gender["String"].isin(top_strings_overall)
    ]

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=top_strings_gender_filtered,
        x="String",
        y="Count",
        hue="Gender"
    )
    plt.title("Top 5 Strings Used by Gender")
    plt.xlabel("String")
    plt.ylabel("Usage Count")
    plt.legend(title="Gender")
    plt.savefig("images/gender_comparison/top_strings_by_gender.png")
    plt.close()

summary_lines.append("\n## 👥 Gender-Based Comparison Summary")

# Top 5 Rackets by Gender (table format)
summary_lines.append("### 🏸 Top 5 Rackets by Gender")
top_rackets_summary = (
    df[df["Racket"].isin(top_rackets_overall)]
    .groupby(["Racket", "Gender"])
    .size()
    .unstack(fill_value=0)
    .sort_values(by=top_rackets_overall, ascending=False)
)
summary_lines.append(top_rackets_summary.to_markdown())

# Top 5 Strings by Gender (table format)
summary_lines.append("### 🧵 Top 5 Strings by Gender")
top_strings_summary = (
    df[df["String"].isin(top_strings_overall)]
    .groupby(["String", "Gender"])
    .size()
    .unstack(fill_value=0)
    .sort_values(by=top_strings_overall, ascending=False)
)
summary_lines.append(top_strings_summary.to_markdown())

# Average Tension by Gender
summary_lines.append("### 📏 Average Tension by Gender")
avg_tension_gender = df.groupby("Gender")["Tension"].mean().round(2)
summary_lines.append(avg_tension_gender.to_frame(name="Average Tension").to_markdown())


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = os.path.dirname(SCRIPT_DIR)

summary_path = os.path.join(ROOT_DIR, "summary.md")

with open("../summary.md", "w") as f:
    f.write("\n".join(summary_lines))

