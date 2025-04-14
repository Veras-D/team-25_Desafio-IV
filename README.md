# 📊 Crypto Dashboard with Streamlit & Plotly

![image](https://github.com/user-attachments/assets/83474ca5-0c3a-4c25-aebe-73fe303262ba)

**Real-time crypto analysis & macroeconomic insights powered by Python, Streamlit, Plotly, and Monte Carlo simulations.**

---

## 🌟 Features

| Module | Description |
|--------|-------------|
| 🏠 **Home** | Welcome screen with project logo and navigation |
| 🔍 **Crypto Analytics** | Analyze crypto returns, aggregated performance by day/month/week |
| 🏛️ **Macroeconomic View** | Explore U.S. macro indicators (interest rates, unemployment, consumer confidence) |
| 📊 **Comparative Returns** | Compare selected crypto assets with BTC, S&P 500 and IBOVESPA |
| 🚀 **Monte Carlo Simulation** | Simulate price behavior over 100 days using Monte Carlo analysis |

---

## ⚙️ Tech Stack

- **Streamlit** for web UI
- **Plotly** for interactive visualizations
- **Pandas + NumPy** for data wrangling
- **Matplotlib** for additional plots
- **Custom Python module** `DataDashboard` to retrieve and preprocess data

---

## 🧪 Live Demo

🚀 Check it out live:  
**[https://dashboardcripto.streamlit.app](https://dashboardcripto.streamlit.app)**

---

## 🧰 How to Run Locally

```bash
# Clone the repo
git clone git@github.com:Veras-D/team-25_Desafio-IV.git
cd team-25_Desafio-IV/dados

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run 1_🏠_Home.py
```

---

## 📈 Monte Carlo Forecasting Example

Monte Carlo simulations are used to forecast future price scenarios:

- **100 future days**
- **100 simulations**
- **Mean, variance & confidence bounds visualized**

Great for **risk analysis and price expectation modeling**.

---

## 📊 Sample Visuals

| Crypto Selection | Return Charts | Macroeconomy | Monte Carlo |
|------------------|---------------|--------------|-------------|
| ![image](https://github.com/user-attachments/assets/77c7e054-fa7f-4010-aca5-e96a4c9701f2) | ![image](https://github.com/user-attachments/assets/86cf62e5-7cbe-4d24-8d16-8f03fe2f741e) | ![image](https://github.com/user-attachments/assets/91e0e091-b074-48ee-b62c-9a91d2c3d466) | ![image](https://github.com/user-attachments/assets/7163c505-4703-4e62-8548-3b36e9813a18) |

---

## 🧠 Future Improvements

- ✅ Add predictive models (e.g. LSTM, Prophet)
- 🌎 Add support for multi-language interface (EN/PT-BR)
- 📱 Make responsive for mobile

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---
