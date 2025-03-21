# PDF Chat Assistant

A web application that allows users to upload PDF documents, manage chat sessions, and interact with an AI assistant to answer questions based on the uploaded content.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Session Management:** Create, select, and delete chat sessions with unique timestamps.
- **PDF Upload:** Upload multiple PDFs and process their content for querying.
- **AI-Powered Chat:** Ask questions about the uploaded documents and receive detailed, context-aware responses.
- **Persistent Storage:** Chat history and PDF metadata stored in a SQLite database.
- **Responsive UI:** Built with React for a clean, user-friendly interface.

## Prerequisites

Before installing, ensure you have:

- **Python 3.8+:** [Download](https://www.python.org/downloads/)
- **Node.js 18+ and npm:** [Download](https://nodejs.org/)
- **Git:** Optional, for cloning the repository ([Install Guide](https://git-scm.com/downloads)).

Verify installations:
```bash
python3 --version  # or python --version
node --version
npm --version
```

## Installation

Follow these steps to set up the project:

1. Clone the Repository

```bash
git clone https://github.com/yourusername/pdf-chat-assistant.git
cd pdf-chat-assistant
```

Replace yourusername with your GitHub username.

2. Set Up the Backend

Navigate to the Backend Directory:

```bash
cd backend
```

Create and Activate a Virtual Environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install Python Dependencies:

```bash
pip install flask flask-cors PyPDF2 langchain langchain-community langchain-google-genai faiss-cpu google-generativeai python-dotenv sqlite3
```

Configure Environment Variables:

Create a .env file:

```bash
touch .env
```

Add your Google API key:

```text
GOOGLE_API_KEY=your_google_api_key_here
```

Replace your_google_api_key_here with your key from Google Cloud. This is required for AI functionality.

3. Set Up the Frontend

Navigate to the Frontend Directory:

```bash
cd ../frontend
```

Install Node.js Dependencies:

```bash
npm install
```

4. Run the Application

Start the Backend

In one terminal, from backend/:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

The backend runs on http://localhost:5001.

Start the Frontend

In another terminal, from frontend/:

```bash
npm start
```

The frontend runs on http://localhost:3000 and opens in your browser.

## Usage

Create a Session:

On the homepage (http://localhost:3000), click "Create New Session" to generate a unique session ID.

Upload PDFs:

Select a session, upload PDF files using the "Upload Documents" section, and click "Process Documents".

Chat with Documents:

In the chat interface, type a question about the uploaded PDFs and press "Send" to get an AI response.

Manage Sessions:

Use the dropdown to switch sessions or click "Delete Session" to remove the current one.

## Troubleshooting

Backend Not Starting:

Port Conflict: If 5001 is in use, change port=5001 in app.py and update axios.defaults.baseURL in frontend/src/App.js.

Missing API Key: Ensure .env contains a valid GOOGLE_API_KEY.

Dependencies: Re-run pip install if errors occur.

Frontend Network Errors:

Verify the backend is running before starting the frontend.

Check browser console (F12) for detailed errors. If CORS-related, ensure flask-cors is installed and configured in app.py.

CSS Not Applying:

Confirm App.css and index.css are imported in App.js and index.js, respectively.

Clear cache: rm -rf frontend/node_modules frontend/package-lock.json && npm install.

Database Issues:

If pdf_chat_sessions.db doesn’t create, run:

```bash
cd backend
python -c "from database import init_db; init_db()"
```

## Contributing

Contributions are welcome! To contribute:

Fork the repository.
Create a branch: git checkout -b feature/your-feature.
Commit changes: git commit -m "Add your feature".
Push to your fork: git push origin feature/your-feature.
Open a Pull Request.

Please include tests and update documentation as needed.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
