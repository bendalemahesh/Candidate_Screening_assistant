# Candidate Screening Assistant
this is a recruiter platform to assist recruiters to automate HR Recruiter works

# 🤖 AI Recruiter Assistant

An AI-powered recruitment assistant that helps automate resume screening, candidate matching, and job description analysis using Natural Language Processing and Machine Learning.

---

## 🚀 Features

- 📄 Resume parsing and analysis (PDF/DOCX support)
- 🎯 Candidate-job role matching using AI scoring
- 🧠 Smart skill extraction from resumes
- 📊 Ranking candidates based on job description
- 🔍 Keyword-based filtering and search
- 🌐 Simple and interactive web UI (Streamlit)

---


## Note

- This is only UI interface and project required file structure not fully functional agent now 
- It will updated in next week with next update

## 🛠️ Tech Stack

- Python 3.x
- Streamlit (Frontend UI)
- Pandas / NumPy (Data handling)
- Scikit-learn (ML model / similarity matching)
- NLP (spaCy / NLTK)
- PyPDF2 / docx (Resume parsing)

---

## 📂 Project Structure

```

AI-Recruiter-Assistant/
│
├── app.py                # Main Streamlit app
├── utils.py              # Helper functions (NLP, parsing, scoring)
├── requirements.txt      # Dependencies
├── data/                 # Sample resumes / datasets
├── models/               # ML models (if any)
└── README.md             # Project documentation

````

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-recruiter-assistant.git
cd ai-recruiter-assistant
````

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## 🧠 How It Works

1. User uploads resumes
2. System extracts text using NLP
3. Job description is compared with resumes
4. AI generates a match score
5. Candidates are ranked automatically

---

## 📊 Example Output

* Candidate A → 89% Match
* Candidate B → 76% Match
* Candidate C → 64% Match

---

## 📌 Future Improvements

* Integration with LinkedIn API
* Advanced AI ranking model (BERT-based)
* Email automation for shortlisted candidates
* Multi-job role comparison dashboard

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed by **Mahesh Bendale**

```

---

If you want, I can also:
✔ Make it look more “hackathon submission ready”  
✔ Add badges (Streamlit / Python / License)  
✔ Customize it exactly to your Week 1 submission format  
✔ Or generate a GitHub-ready repo structure for you  

Just tell me 👍
```
