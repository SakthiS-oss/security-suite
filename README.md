# 🛡️ Security Suite: Multi-Threaded Audit & Penetration Tool

An interactive, multi-tabbed security application built with Python and Tkinter. This project implements real-time cryptographic analysis, information entropy modeling, and secure API communication to evaluate and crack credential sets.

## 📌 Project Overview
This application serves as a comprehensive **Security Exam** for user credentials, providing:
* **Real-time Entropy Auditing** (Strength detection)
* **K-Anonymity Leak Checks** (Privacy-preserving database lookup)
* **Secure Credential Generation** (Cryptographic randomness)
* **Multi-Threaded Batch Processing** (Large-scale data auditing)
* **Hash Cracker** (Dictionary-based penetration testing)

The goal was to combine system-level concurrency, cryptographic mathematics, and intuitive UI design into a complete end-to-end security utility.

## 🧠 Model & Methodology

### 1️⃣ Information Entropy Modeling
The application assesses password strength by calculating the bits of entropy ($E$), which represents the number of attempts a brute-force attacker would need to guess the password.

$$E = L \times \log_2(R)$$

* **$L$**: Password length
* **$R$**: Size of the character pool (Lower/Upper/Numbers/Symbols)



### 2️⃣ K-Anonymity Privacy Protocol
To check if a password has been leaked without actually sending the password to a third party, the suite uses the **k-Anonymity** model:
1. The password is hashed using **SHA-1**.
2. The app sends only the **first 5 characters** of the hash to the *Have I Been Pwned* API.
3. The API returns a list of all leaked hash suffixes matching that prefix.
4. The app performs a **local comparison** to find a match.

**Result:** Neither the password nor the full hash ever leaves the local machine.



### 3️⃣ System Concurrency (Threading)
To ensure the UI remains responsive during long-running tasks (like scanning a 10,000-word dictionary or calling an API), the project implements:
* **Background Worker Threads:** Handles all I/O and networking.
* **Stop Events:** Allows users to kill background processes gracefully.
* **UI Dispatching:** Uses `root.after()` to safely update the GUI from secondary threads.



---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone [https://github.com/SakthiS-oss/security-suite.git](https://github.com/SakthiS-oss/security-suite.git)
cd security-suite
2️⃣ Install dependencies
The app uses Python's standard library for almost everything, but requires requests for the leak check feature.

Bash
pip install requests
3️⃣ Run the app
Bash
python app.py
📊 Feature Breakdown
Single Auditor: Input a password to see live entropy updates and a color-coded strength bar. Toggle "Show/Hide" to mask sensitive data.

Batch Analysis: Upload a .txt file. The app processes each line and categorizes them into 🚨 LEAKED, ⚠️ WEAK, or ✅ Safe.

Hash Cracker: Paste a SHA-1, MD5, or SHA-256 hash. Select a dictionary file (like rockyou.txt) to attempt a recovery.

Generator: Set a length and generate a high-entropy string using the secrets module.

🛠 Tech Stack
Language: Python 3.x

GUI: Tkinter / ttk

Networking: Requests (REST API)

Cryptography: hashlib, secrets

Concurrency: threading

📈 Key Skills Demonstrated
Multithreaded Architecture: Managing separate execution flows to prevent UI hanging.

Cryptographic Implementation: Using one-way hashing and secure random number generation.

Data Visualization: Translating mathematical entropy into human-readable visual indicators.

API Security: Implementing privacy-preserving protocols (K-Anonymity).

Defensive & Offensive Design: Building both auditing (defensive) and cracking (offensive) modules.

⚠️ Disclaimer
This model is for educational and analytical purposes only. Never use this suite on credentials or hashes you do not have permission to audit.
