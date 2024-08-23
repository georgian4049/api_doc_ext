# Data Extraction API

This API is designed to process images of invoices and convert the data into a structured JSON format. The API utilizes a machine learning model (Gemini AI) to comprehend receipts and extract relevant information.

## Features

- **Image Upload**: Upload an image of an invoice or receipt.
- **Data Extraction**: Convert the invoice data into a JSON format and returns.

## Prerequisites

Before setting up and running the API, make sure you have the following installed:

- Python 3.8 or higher
- Flask
- Required Python libraries (listed in `requirements.txt`)
- Also, you need to create your own GOOGLE_API_KEY for accessing services of Gemini AI and set it in your env.

## Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
