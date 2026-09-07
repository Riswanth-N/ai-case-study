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

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=ai_case_study
OPENAI_API_KEY=your_openai_api_key
```

## Run the Application

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

**Request:**

```json
{
  "userInput": "What is Python?"
}
```

**Response:**

```json
{
  "response": "..."
}
```

The API retrieves the `Education_Prompt` template from MongoDB, replaces `{{userInput}}`, sends the final prompt to OpenAI, and stores the request and response in the `history` collection.

### POST /ask-multiple

Accepts multiple user inputs and processes them concurrently.

**Request:**

```json
{
  "userInputs": [
    "What is Python?",
    "What is MongoDB?",
    "What is Flask?"
  ]
}
```

**Response:**

```json
{
  "responses": [
    "...",
    "...",
    "..."
  ]
}
```

The responses are returned in the same order as the input list.

## MongoDB Collections

### prompts

Stores prompt templates.

**Example:**

```json
{
  "_id": "Education_Prompt",
  "template": "You are an expert in education domain. Answer the following: {{userInput}}"
}
```

### history

Stores each request and its OpenAI response along with a timestamp.

## Error Handling

The API validates request data and returns appropriate HTTP status codes for invalid requests, missing prompts, and server-side errors.