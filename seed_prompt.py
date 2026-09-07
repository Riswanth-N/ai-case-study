from database import db

prompt = {
    "_id": "Education_Prompt",
    "template": "You are an expert in education domain. Answer the following: {{userInput}}"
}

try:
    db.prompts.insert_one(prompt)
    print("Education prompt inserted successfully!")
except Exception as error:
    print("Error inserting prompt:")
    print(error)