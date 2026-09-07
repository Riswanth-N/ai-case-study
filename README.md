# Case Study API

A Flask-based REST API that accepts user questions, retrieves a prompt template from MongoDB, sends the final prompt to OpenAI, and stores the request and response history.

## Technologies

- Python
- Flask
- MongoDB
- PyMongo
- OpenAI API
- python-dotenv

## Project Structure

```text
ai-case-study/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── ask_routes.py
│   │   └── multiple_routes.py
│   └── services/
│       ├── __init__.py
│       ├── openai_service.py
│       └── multiple_service.py
├── database.py
├── run.py
├── seed_prompt.py
├── test_openai.py
├── requirements.txt
└── .gitignore
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file named `.env` in the project root directory.

Add the following:

```text
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=ai_case_study
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholder values with your actual MongoDB connection string and OpenAI API key.

Do not commit the `.env` file to GitHub.

### 5. Seed the prompt into MongoDB

Run:

```bash
python seed_prompt.py
```

This creates the `Education_Prompt` document in the `prompts` collection.

## Run the Application

Start the Flask application:

```bash
python run.py
```

The API runs on:

```text
http://localhost:5000
```

## API Endpoints

### POST /ask

Accepts a single user input.

#### Request

```json
{
  "userInput": "What is Python?"
}
```

#### Response

```json
{
  "response": "..."
}
```

The API:

1. Receives the user input.
2. Retrieves the `Education_Prompt` template from MongoDB.
3. Replaces `{{userInput}}` with the user's question.
4. Sends the final prompt to the OpenAI API.
5. Stores the request and response in the `history` collection.
6. Returns the AI response in JSON format.

### POST /ask-multiple

Accepts multiple user inputs in a single request.

#### Request

```json
{
  "userInputs": [
    "What is Python?",
    "What is MongoDB?",
    "What is Flask?"
  ]
}
```

#### Response

```json
{
  "responses": [
    "...",
    "...",
    "..."
  ]
}
```

The API:

1. Receives a list of user inputs.
2. Retrieves the prompt template from MongoDB.
3. Applies the prompt template to each input.
4. Processes the OpenAI requests concurrently using asynchronous calls.
5. Stores each request and response in the `history` collection.
6. Returns the responses in the same order as the input list.

## MongoDB Collections

### prompts

The `prompts` collection stores prompt templates.

#### Example Document

```json
{
  "_id": "Education_Prompt",
  "template": "You are an expert in education domain. Answer the following: {{userInput}}"
}
```

### history

The `history` collection stores every request and its corresponding OpenAI response.

Each history record contains:

- `userInput`
- `response`
- `createdAt`

## How It Works

### Single Request Flow

```text
Client
  ↓
POST /ask
  ↓
Fetch prompt from MongoDB
  ↓
Replace {{userInput}}
  ↓
Call OpenAI API
  ↓
Store request/response in history
  ↓
Return JSON response
```

### Multiple Request Flow

```text
Client
  ↓
POST /ask-multiple
  ↓
Receive list of inputs
  ↓
Create asynchronous OpenAI requests
  ↓
Process requests concurrently
  ↓
Store each request/response in history
  ↓
Return responses in the same order
```

## Asynchronous Processing

The `/ask-multiple` endpoint uses asynchronous OpenAI requests with `AsyncOpenAI` and `asyncio.gather()`.

This allows multiple OpenAI requests to be processed concurrently instead of waiting for each request to finish before starting the next one.

`asyncio.gather()` returns the results in the same order as the input tasks, so the response order matches the original input order.

## Error Handling

The API validates incoming request data and returns appropriate HTTP status codes for:

- Missing request body
- Missing `userInput`
- Missing `userInputs`
- Invalid `userInputs` format
- Empty input strings
- Missing prompt templates
- Server-side errors

## Environment Variables

The application uses the following environment variables:

```text
MONGO_URI
MONGO_DB_NAME
OPENAI_API_KEY
```

These values are loaded from the `.env` file using `python-dotenv`.

## Notes

- MongoDB Atlas is used as the database.
- OpenAI API is used to generate responses.
- The `.env` file contains sensitive credentials and should not be committed to the repository.
- The project is designed to run locally.