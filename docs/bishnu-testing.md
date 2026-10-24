# StudyBuddy AI – Ollama Connection Testing Report

**Contributor:** Bishnu Chaudhary  
**Project:** StudyBuddy AI  
**Role:** Application Review and Testing

## 1. Objective

The objective of this task was to create and test a Python script that checks whether the Ollama server and required AI model are available before running StudyBuddy AI.

## 2. Implementation

I developed a standalone Python script named `check_ollama.py`.

The script checks the Ollama server connection, displays the installed AI models, verifies the required model, and provides error messages when the server is unavailable.

## 3. Testing Results

| Test ID | Test Description | Result |
|---|---|---|
| TC01 | Check connection to Ollama on port 11434 | PASS |
| TC02 | Verify the required Llama 3.2 model | PASS |
| TC03 | Display available AI models | PASS |
| TC04 | Detect connection failure on port 11435 | PASS |

## 4. Observations

During the normal connection test, the script successfully connected to the Ollama server. It detected two installed models: `llama3.2:latest` and `llama3.2:3b`.

During the negative test, I changed the API port from 11434 to 11435. The script correctly identified the connection failure and displayed an error message.

## 5. Conclusion

The Ollama Connection Checker successfully completed all four checks. It provides a simple way to identify local Ollama configuration problems.

The tool runs independently and does not require changes to the main StudyBuddy AI application.