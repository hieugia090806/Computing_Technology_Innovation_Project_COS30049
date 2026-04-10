# TruthGuard – Full-Stack AI Cybersecurity Web Application

## Assignment Name
**Full-Stack Web Development for AI Application in Cybersecurity Scenarios**

## Unit
COS30049 – Introduction to Artificial Intelligence

---

## 1. Project Overview

**TruthGuard** is a full-stack web application that demonstrates the integration of machine learning models into a modern web-based cybersecurity system.  

The application allows users to submit textual content or URLs, which are then analyzed by AI models on the server side to detect potential cybersecurity threats such as:

- Fake news and misinformation
- Spam content
- Malware-related indicators

Prediction results are returned in real time and visualized through interactive charts on the front-end, providing users with clear and meaningful insights into the AI model’s output.

This project represents the final and most significant assessment of the unit, focusing on full-stack integration, AI deployment, and user-focused data visualization.

---

## 2. System Architecture

The system follows a **client–server architecture** consisting of three major components:

### 2.1 Front-End (React.js)
- Built using **React.js** with **TypeScript**
- Designed as a responsive, single-page application
- Handles user input validation and UI state management
- Communicates with the backend via RESTful APIs
- Displays AI prediction results using interactive charts

### 2.2 Back-End (FastAPI)
- Implemented using **FastAPI**
- Exposes RESTful endpoints for data analysis
- Handles request validation and error handling
- Integrates trained machine learning models from Assignment 2
- Returns structured prediction results for visualization

### 2.3 AI Models
- Machine learning models trained in Assignment 2
- Models are loaded using `joblib`
- Text preprocessing and vectorization handled on the backend
- Supports real-time inference with confidence and risk scores

---

## 3. Technologies Used

### Front-End
- React.js
- TypeScript
- Vite
- Tailwind CSS
- Recharts (for data visualization)
- lucide-react (icons)

### Back-End
- Python 3.12
- FastAPI
- Uvicorn
- Scikit-learn
- Joblib

---

## 4. Key Features

- ✅ Full-stack integration between React.js and FastAPI
- ✅ Real-time AI predictions
- ✅ Detection of cybersecurity threats (fake news, spam, malware)
- ✅ Interactive data visualizations:
  - Bar Chart
  - Line Chart
  - Radar Chart
- ✅ Robust error handling and input validation
- ✅ Responsive UI with dark and light themes

---

## 5. Project Structure
```text
Website/
├── Backend/
│   ├── app.py
│   ├── classifier.py
│   ├── models_handler.py
│   ├── Datasets/
│   ├── Processed/
│   ├── Test Data/
│   └── Model/
│       ├── NewsModel.pkl
│       ├── SpamScanner.pkl
│       ├── MalwareModel.pkl
│       └── SpamVectorizers.pkl
│
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FakeNewsDetector.tsx
│   │   │   ├── SpamMalwareDetector.tsx
│   │   │   └── ThreatDetectionDashoard.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── styles/
│   │   ├── public/
│   │   └── App.tsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```
---

## 6. Data Visualization
The front-end visualizes AI prediction outputs using Recharts, ensuring clarity and interactivity:

Bar Chart: Displays confidence and risk scores
Line Chart: Shows threat trends over time
Radar Chart: Visualizes multi-dimensional analysis of prediction metrics

All charts update dynamically after each prediction.

---

## 7. Setup and Running Instructions
### 7.1 Backend Setup

Navigate to the backend directory:

*cd Backend*

Install dependencies:

*pip install fastapi uvicorn scikit-learn joblib*

Run the server:

*uvicorn app:app --reload*

Backend will be available at:
**http://127.0.0.1:8000**

Swagger UI:
**http://127.0.0.1:8000/docs**


## 7.2 Frontend Setup

Navigate to the frontend directory:

*cd Frontend*

Install dependencies:

*npm install*

Run the development server:

*npm run dev*

Frontend will be available at:
**http://localhost:3000**

---

## 8. Conclusion and Future Improvements
TruthGuard demonstrates a practical and scalable approach to deploying AI-powered cybersecurity solutions through a full-stack web application.
The system successfully integrates machine learning models with modern front-end technologies to provide meaningful, interactive insights for users.

Potential future enhancements include:
- Additional AI models and threat categories
- Real-time streaming analysis
- Exportable reports and logs
- Enhanced visualization interactivity

---

## 9. Academic Integrity Notice
This project was developed as part of COS30049.
While generative AI tools were used for learning support and debugging assistance, all core logic, implementation, and explanations were written, reviewed, and understood by the authors.
All external references are acknowledged in the project report as required.

---

## 10. Group Information
Project Name: Lowkenuinely
Unit: COS30049
Assignment: Assignment 3 – Full-Stack Web Development for AI Applications

---