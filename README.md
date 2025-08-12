pip install -r requirements.txt
# FindMyRecipe 🍅🥗

A simple web app where you type in ingredients you have at home, and it finds recipes that include them.  
Powered by **Flask**, **Pandas**, and a basic **machine learning search** using TF-IDF + Nearest Neighbors.

---

## 📂 Project Structure

2025_08_Team3/
│── app.py                # Flask backend
│── data/
│   └── recipes.csv       # Recipe dataset
│── templates/
│   └── index.html        # Main frontend HTML
│── static/
│   └── style.css         # Styling
└── README.md             # This file

---

## 🚀 Features
- Search recipes by ingredient(s)  
- Option to require all entered ingredients  
- Fast similarity search powered by **scikit-learn**  
- Clean, responsive frontend with HTML + CSS

---

## 📦 Requirements

Create and activate a virtual environment, then install dependencies:  
```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:
```
Flask==3.1.1
pandas==2.2.3
numpy==2.2.4
scipy==1.15.2
scikit-learn==1.6.1
jupyterlab==4.3.4
```

## 🛠 Setup & Run

1. **Clone the repo**
   ```bash
   git clone git@github.com:Cos229-239/2025_08_Team3.git 
   cd 2025_08_Team3
   pip install -r requirements.txt
   python app.py
   ```

2. Open your browser and go to:  
   http://127.0.0.1:5000