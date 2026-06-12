# 🚗 US Car Market Intelligence Dashboard

> **Analyzing US car sales before, during, and after the COVID-19 pandemic**  
> Built with Python · Pandas · Plotly · Streamlit

---

## 📌 Overview

This project performs an end-to-end data analysis of the US car sales market, covering temporal trends, customer segmentation, regional performance, and the measurable impact of COVID-19 on vehicle sales. The final deliverable is a fully interactive **Streamlit dashboard** for decision-oriented exploration.

---

## 🎯 Key Objectives

- 📈 Identify **sales trends** and seasonal patterns across years
- 🦠 Measure the **COVID-19 impact** on revenue and quantities sold (2019–2021)
- 👤 Segment customers using **RFM Analysis** (Recency, Frequency, Monetary)
- 🌍 Evaluate **regional stability** across US sales zones
- 🎂 Explore **car preferences by customer age group**
- 🖥️ Deliver a live **interactive dashboard** for business decision-makers

---

## 📊 Dashboard Features

| Section | Description |
|---|---|
| **Global KPIs** | Revenue, Orders, Customers, Avg Basket |
| **Sales Evolution** | Monthly & yearly trend lines |
| **Seasonality Analysis** | Quarterly revenue aggregation |
| **COVID-19 Impact** | Revenue comparison 2019–2021 |
| **Product Performance** | Top N & Bottom N car brands |
| **Customer Pareto (80/20)** | Cumulative revenue by customer |
| **Customer Loyalty** | Repeat purchase analysis |
| **Seller Performance** | Top salespeople by revenue |
| **Regional Stability** | Volatility index per region |
| **Age Preferences** | Car brand popularity by age group |
| **RFM Segmentation** | Champions → Lost Customers pie chart |

---

## 🗂️ Project Structure

```
dashboard_project/
│
├── dashboard.py              # Streamlit interactive dashboard
├── cars.ipynb                # Jupyter notebook — full analysis
├── mini_projet_ADD.pptx      # Project presentation deck
├── README.md                 # This file
│
└── data/
    └── car_sales.csv         # Dataset (not included — see below)
```

---

## ⚙️ Setup & Installation

**Requirements:** Python 3.11+

### 1. Clone the repository

```bash
git clone https://github.com/your-username/car-sales-dashboard.git
cd car-sales-dashboard
```

### 2. Create and activate environment

```bash
conda create -n dashboard python=3.11
conda activate dashboard
```

Or with venv:

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Place `car_sales.csv` inside the `data/` folder.  
The file is expected at `data/car_sales.csv` relative to the project root.

### 5. Run the dashboard

```bash
cd dashboard_project
streamlit run dashboard.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📦 Dependencies

```
streamlit
pandas
plotly
numpy
```

Generate a `requirements.txt` with:

```bash
pip freeze > requirements.txt
```

---

## 📈 Key Findings

- **Q2 and Q4** consistently generate the highest revenues (~$49B and ~$50B respectively)
- **February** shows a structural seasonal dip across all years
- **COVID-19 (2020)** caused a significant revenue drop — lockdowns delayed purchases rather than cancelled them, confirmed by the strong 2021 rebound
- ~**20% of customers** generate ~**80% of total revenue** (Pareto principle holds)
- **Ohio and Tennessee** are the most stable sales regions; **Alabama** shows irregular volatility
- Younger customers (18–35) prefer compact/sporty models; older segments (46+) favor comfort and reliability

---

## 🧠 RFM Segments

| Segment | Share | Description |
|---|---|---|
| Champions | 12% | Recent, frequent, high spend |
| Loyal Customers | 25% | Consistent buyers |
| Potential Loyalists | 30% | Moderate, growing activity |
| At Risk | 20% | Declining engagement |
| Lost Customers | 13% | No recent activity |

---

## 👤 Author

**Gheraibia Chihab Eddine**  
Data Science / Computer Science  
📧 chihabghraibia2023@gmail.com

---

## 📄 License

This project is for educational purposes. Dataset rights belong to their respective owners.
