import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("customers.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Latest Date
today = df['Date'].max()

# RFM calculation 
rfm = df.groupby('CustomerID').agg({
    'Date': lambda x: (today - x.max()).days,
    'CustomerID': 'count',
    'Amount': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

# Segmentation Logic
def segment(row):
    if row['Monetary'] > 1500:
        return "High Value"
    elif row['Monetary'] > 800:
        return "Medium Value"
    else:
        return "Low Value"
    
rfm['Segment'] = rfm.apply(segment, axis=1)
print("\n📊 RFM Table:\n")
print(rfm)

# Styling

sns.set_style("whitegrid")
sns.set_palette("Set2")

# BAR Chart (Segment Count)

rfm['Segment'].value_counts().plot(kind='bar')
plt.title("Customer Segments", fontsize=16)
plt.xlabel("Segment")
plt.ylabel("Numbers of Customers")
plt.savefig("segments.png", dpi=600, bbox_inches="tight")
plt.clf()

#Scatter Plot (Sales vs Frequency)
sns.scatterplot(x="Frequency", y="Monetary", hue="Segment", data=rfm, s=100)
plt.title("Customer Behaviour (Frequency vs Monetary)")
plt.savefig("customer_behavior.png", dpi=600, bbox_inches="tight")
plt.clf()
print("\n Done! Graph Saved (segment.png, customer-scatter.png)")