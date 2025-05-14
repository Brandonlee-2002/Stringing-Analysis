import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.core.algorithms import nunique_ints


# Load dataset (replace 'your_data.csv' with actual file)
df = pd.read_csv("/Users/brandonlee/PycharmProjects/Badminton_Racket_Analysis/data/RestringLog.csv")

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
plt.savefig("/Users/brandonlee/PycharmProjects/Badminton_Racket_Analysis/images/tension_distribution.png")

# Top Racket Usage
plt.figure(figsize=(10,5))
sns.barplot(x=top_rackets.index, y=top_rackets.values)
plt.xticks(rotation=45)
plt.xlabel("Racket")
plt.ylabel("Count")
plt.title("Top 10 Most Used Rackets")
plt.savefig("/Users/brandonlee/PycharmProjects/Badminton_Racket_Analysis/images/top_rackets.png")

# Top String Usage
plt.figure(figsize=(10,5))
sns.barplot(x=top_strings.index, y=top_strings.values)
plt.xticks(rotation=45)
plt.xlabel("String")
plt.ylabel("Count")
plt.title("Top 10 Most Used Strings")
plt.savefig("/Users/brandonlee/PycharmProjects/Badminton_Racket_Analysis/images/top_strings.png")

# 3. Outlier Detection (Boxplot)
plt.figure(figsize=(8,5))
sns.boxplot(x=df["Tension"])
plt.xlabel("String Tension (lbs)")
plt.title("Boxplot of String Tension")
plt.savefig("/Users/brandonlee/PycharmProjects/Badminton_Racket_Analysis/images/boxplot_tension.png")

# Identify outliers
Q1 = df["Tension"].quantile(0.25)
Q3 = df["Tension"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["Tension"] < lower_bound) | (df["Tension"] > upper_bound)]
summary_lines.append(f"\n## ⚠️ Tension Outliers\n")
summary_lines.append(f"Total Outliers Detected: **{len(outliers)}**")

with open("summary.md", "w") as f:
    f.write("\n".join(summary_lines))

