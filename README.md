# Badminton Racket Restringing Analysis

## 📌 Project Overview
This project explores trends in badminton racket and string preferences, analyzing string tension distributions and detecting outliers.

## 📊 Quantitative Analysis
- Most popular rackets and strings
- Average string tension per racket
- Outlier detection using IQR method
- Visualizations of tension distribution

### 🔑 Key Takeaways
- AX88D Pro (including the 3rd Gen) is the most popular because it is marketed as one of the best doubles head-heavy rackets. 
- Most players prefer BG66UM because it is a high repulsion string. High repulsion means power in exchange for durability. The string is very thin as a result and pop quicker than most strings, especially strung at max recommended tension.
- Based on the data, most players that I have strung for prefer the 28-29 tension. 

#### 📈 Boxplot
- Line inside box means median string tension
- IQR Box
  - Box itself represents the middle 50% of the data (between Q1 and Q3)
  - shorter box means most tensions are more clustered
- Whiskers (lines extending from the box)
  - Whiskers indicate the range of non-outliers
  - They usually extend to 1.5 times the IQR
- Outliers 
  - the Dots outside the whiskers are considered outliers (ex. 22, 23, 24, 25, 30 lbs)
  - Represents uncommon stringing preferences (extreme high or low tensions)
  - These outliers are more unique customer preferences


## 📁 Project Structure
- **data/**: Contains raw datasets used for the analysis.
- **notebooks/**: Jupyter Notebooks where the exploratory data analysis (EDA) and other analyses are performed.
- **scripts/**: Python scripts for running data analysis, cleaning, and other tasks.
- **images/**: Folder to store visualizations created during analysis.
- **README.md**: Documentation file to describe the project, setup, and usage.
- **requirements.txt**: Lists the Python packages required to run the project


## 📈 Results
### **Most Popular Rackets**
![racket chart](images/top_rackets.png)

### **Most Popular Strings**
![string chart](images/top_strings.png)

### **String Tension Distribution**
![tension chart](images/tension_distribution.png)

### **Boxplot**
![boxplot](images/boxplot_tension.png)

### **Output**
Unique Players: 36
Unique Rackets: 30
Unique Strings: 13

Top Rackets: <br>
 Racket <br>
AX88D Pro     45 <br>
AX88D         36 <br>
AX100ZZ       26 <br>
Arc 11 Pro    20 <br>
NF800 Pro     18 <br>
AX88D Pro     10 <br>
NF800         10 <br>
Assorted      10 <br>
Z Strike       8 <br>
AX77 Pro       8 <br>
Name: count, dtype: int64

Top Strings: <br>
 String <br>
BG66U       73 <br>
NBG95       56 <br>
BG65Ti      37 <br>
BG80        19 <br>
Gosen       17 <br>
BG65         8 <br>
NBG98        7 <br>
Exbolt65     5 <br>
Ex65         4 <br>
AB           3 <br>
Name: count, dtype: int64

Average Tension by Racket:
 Racket
Ryuga II       29.000000
Z Strike       28.875000
AX100ZZ        28.423077
AX77 Pro       28.375000
AX99 Pro       28.200000
AX88D          28.027778
Vanguard 11    28.000000
Drive9X        28.000000
NR800          28.000000
V11            28.000000
Name: Tension, dtype: float64


## 🔧 Installation
To run this project locally:
```bash
git clone https://github.com/yourusername/badminton-analysis.git
cd badminton-analysis
pip install -r requirements.txt
jupyter notebook
```

