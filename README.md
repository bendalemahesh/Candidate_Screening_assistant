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

- Python 3.14.6
- Streamlit (Frontend UI)
- Pandas / NumPy (Data handling)
- Scikit-learn (ML model / similarity matching)
- NLP (spaCy)
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
git clone https://github.com/bendalemahesh/Candidate_Screening_assistant.git
cd Candidate_Screening_assistant
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
streamlit run App/app.py
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

## 📌 Future Enhancements

* Integration with APIs
* Advanced AI ranking model
* Email automation for shortlisted candidates
* Multi-job role comparison dashboard

---

## 👨‍💻 Author

Developed by **Mahesh Chandrakant Bendale and Team AI Developers**
- 1. Team Lead: Mahesh Chandrakant Bendale
- 2. Team Member 1: Riddhi Pravin Sarode
- 3. Team Member 2: Purva Nilesh Chaudhari
- 4. Team Member 3: Vishwaja Kishor Mahajan
```
