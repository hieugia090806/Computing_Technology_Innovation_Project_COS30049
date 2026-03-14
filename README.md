🛡️ Intelligent Multi-Layered Threat Detection System

A. Course Introduction
   The project was developed as a core component of the Computing Technology Innovation Project (COS30049) unit. Besides, the curriculum focuses on the intersection of data science and digital security which emphasizes the transition from traditional rule-based filters to adaptive, AI-driven defense mechanisms.

B. Project Overview
   Our project introduces a comprehensive, multi-layered security framework designed to identify and mitigate three of the most prevalent digital threats today: Spam, Malware, and Fake News/Deceptive Links.

   By leveraging the E-M-B-T (Entity, Model, Benign, Threat) logical framework, the system provides a centralized "Brain" that orchestrates specialized detection modules. Unlike static security tools, this system internalizes underlying data patterns to proactively flag risks before they can impact the end-user.

   🎯 Core Objectives   
       - Spam Detection: Filtering communication channels by identifying linguistic patterns in SMS and email data.
       - Malware Identification: Analyzing file behavior and structural signatures to distinguish malicious code from safe software.    
       - Newspaper Link Verification: Combatting misinformation and typosquatting by validating the reputation and structure of news URLs.
    
    🚀 Key Features
       - Intelligent Driven Engine: Powered by the LinearSVC algorithm for high-speed, high-accuracy classification.
       - Optimized Performance: Utilizes Joblib for model persistence, allowing near-instant analysis without repetitive training.
       - Visual Analytics: Generates automated Cluster Maps and Confusion Matrices to provide transparency in the decision-making process.

C. Technical Python Libraries
The system leverages the powerful Python ecosystem to handle data processing and machine learning. The primary libraries used include:
    - Pandas & NumPy: The core engines for data manipulation, used to structure and clean the 26 datasets to ensure input accuracy.
    - Scikit-learn: The primary machine learning library providing the LinearSVC algorithm for classification and TfidfVectorizer for text feature extraction.
    - Joblib: Used for system optimization by persisting (saving) trained models, allowing for instant responses without retraining.
    - Matplotlib & Seaborn: Specialized for data visualization, generating the Cluster Maps and Confusion Matrices used to evaluate system performance.
    - OS Module: Handles system directory management and coordinates file I/O operations between different modules.

D. Project Workflow: Data Path Analysis
The system follows a sequential data pipeline where information flows from raw input to specialized processing, and finally to result generation: Datasets (.csv) ➔ Loader.py ➔ Brain.py ➔ Detector (.py) ➔ Results (.png)

E. How to Run (Local Installation)
    - Step 1: Environment Setup (pip install pandas scikit-learn matplotlib seaborn joblib)
    - Step 2: Directory Structure (Ensure your files are organized as follows):
        1. Test.py (Main execution file)
        2. Brain.py & Loader.py (Core logic)
        3. Training/ (Directory containing specialized detectors)
        4. Backend/Datasets/ (Directory containing Dataset01 to Dataset26)
    - Step 3: Run the main script from your Terminal or Command Prompt: python Test.py
    - Step 4: Verify Results
        1. The classification results will be displayed directly in the terminal output.
        2. Analytical visuals (Cluster Maps and Confusion Matrices) will be automatically saved in the following directory: Backend/Results/.
    
F. Closing
The Intelligent Multi-Layered Threat Detection System represents a significant step toward an automated, AI-driven security ecosystem. By successfully integrating three distinct defensive pillars—Spam, Malware, and Newspaper verification—this project demonstrates that machine learning is not just a tool for analysis, but a vital shield in the modern digital landscape.

Final Takeaways
    - Adaptability: The system's ability to learn from evolving datasets ensures it remains effective against "zero-day" threats and modern misinformation tactics.
    - Performance: Through architectural optimizations like model persistence, we have proven that sophisticated security doesn't have to come at the cost of speed.
    - Vision: This project serves as a proof-of-concept for future autonomous security agents capable of protecting users across all communication platforms.

As cyber threats continue to grow in complexity, our commitment to refining the E-M-B-T logic and exploring deeper neural architectures remains the priority. This project is a testament to the power of intelligent automation in building a safer, more transparent, and more resilient internet for everyone.

Thank you for exploring our project! For any inquiries regarding the technical implementation or data methodology, please feel free to reach out to the project team.