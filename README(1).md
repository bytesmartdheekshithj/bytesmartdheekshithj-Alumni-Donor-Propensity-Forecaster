# Alumni Donor Propensity Forecaster

## Project Overview

The Alumni Donor Propensity Forecaster is a machine learning project designed to estimate the likelihood of an alumnus making a donation in the next donation period.

The system uses alumni information such as demographic details, graduation information, communication availability, wealth and income indicators, event participation, email engagement, and previous donation history.

The trained machine learning model produces a donation probability and converts it into an easy-to-understand propensity score and category.

## Problem Statement

Educational institutions need to identify alumni who are more likely to donate so that their fundraising teams can plan alumni engagement and outreach activities effectively.

Instead of treating every alumnus in the same way, this project uses historical alumni information to estimate the likelihood of donation.

The system helps answer:

"How likely is this alumnus to donate?"

## Objective

- Predict whether an alumnus is likely to donate.
- Calculate the probability of donation.
- Convert the probability into a propensity score from 0–100.
- Categorize alumni into High, Medium, or Low propensity.
- Provide predictions through a REST API.
- Use Redis for fast repeated predictions.
- Use RabbitMQ for asynchronous event messaging.
- Provide a structure that can later be deployed using Docker.

## Dataset

Dataset: `alumni_donor_dataset_2025.csv`

| Property | Details |
|---|---|
| Number of Records | 10,000 |
| Number of Columns | 18 |
| Prediction Year | 2025 |
| Target Variable | `Is_Donor_2025` |
| Target Type | Binary Classification |

### Dataset Columns

| # | Feature | Description |
|---|---|---|
| 1 | `Alumni_ID` | Unique identifier for each alumnus |
| 2 | `Age` | Current age of the alumnus |
| 3 | `Gender` | Gender information |
| 4 | `Graduation_Year` | Year of graduation |
| 5 | `Degree_Level` | Degree level completed |
| 6 | `Major` | Academic major |
| 7 | `Alumni_Status` | Current alumni status |
| 8 | `Email_Available` | Whether email contact is available |
| 9 | `Phone_Available` | Whether phone contact is available |
| 10 | `Wealth_Rating` | Wealth rating information |
| 11 | `Income_Bracket` | Income category |
| 12 | `Event_Attendance` | Alumni event participation |
| 13 | `Email_Open_Rate` | Email engagement rate |
| 14 | `Location` | Alumni location |
| 15 | `Consecutive_Giving_Years` | Number of consecutive years of giving |
| 16 | `Donation_Last_Year_2024` | Donation amount in 2024 |
| 17 | `Total_Lifetime_Giving` | Total historical donation amount |
| 18 | `Is_Donor_2025` | Target indicating whether the alumnus donated in 2025 |

## Machine Learning Approach

The project uses a binary classification approach.

The model learns patterns from alumni information and predicts the likelihood of donation.

### Target Variable

`Is_Donor_2025`

- `1` / `Yes` → Donated in 2025
- `0` / `No` → Did not donate in 2025

`Alumni_ID` is used only as an identifier and is not used as a machine learning feature.

## Data Processing

### Numerical Features

- Age
- Graduation Year
- Event Attendance
- Email Open Rate
- Consecutive Giving Years
- Donation Last Year 2024
- Total Lifetime Giving

### Categorical Features

- Gender
- Degree Level
- Major
- Alumni Status
- Email Available
- Phone Available
- Wealth Rating
- Income Bracket
- Location

The model pipeline handles these two types of data separately before passing them to the machine learning model.

## Machine Learning Model

The project uses Logistic Regression as the trained classification model.

The model is stored as:

`alumni_donor_propensity_model_2025.pkl`

The complete preprocessing and prediction pipeline is saved so that the same data preparation process can be used during API prediction.

## Prediction Output

The model generates a donation probability.

Example:

- Donation Probability: `0.9341`
- Propensity Score: `93.41`
- Category: `High`
- Interpretation: `Likely to Donate`

The probability is converted into a score between 0 and 100.

### Propensity Categories

| Score | Category | Interpretation |
|---|---|---|
| 80–100 | High | Likely to Donate |
| 50–79 | Medium | Moderate Donation Likelihood |
| 0–49 | Low | Lower Donation Likelihood |

The propensity score represents the model's estimated likelihood and should not be treated as a guarantee of future donation.

## System Architecture

```text
                 Alumni Data
                     |
                     v
              Flask REST API
                     |
                     v
              /predict Endpoint
                     |
                     v
                Redis Cache
                /          \
             HIT            MISS
              |               |
              v               v
       Cached Result       ML Model
                              |
                              v
                       Prediction Result
                         /          \
                        /            \
                       v              v
                    Redis         RabbitMQ
                       |              |
                       v              v
                  API Response   Event Message
```

## Flask API

Flask acts as the main API layer between the client and the machine learning model.

Main prediction endpoint:

`POST /predict`

Health endpoint:

`GET /`

The health endpoint is used to check whether the application, Redis, RabbitMQ, and model services are running correctly.

## Redis Cache

Redis is used to store previously generated predictions.

For a first request, the system checks Redis. If the result is not available, the ML model generates the prediction and the result is stored in Redis.

For a repeated request, Redis returns the cached result without unnecessarily running the prediction again.

Example cache key:

`alumni:ALM000001`

The cache expiry is configured for a limited period so that old predictions are not stored indefinitely.

## RabbitMQ

RabbitMQ is used as a messaging system for prediction-related events.

After a new prediction is generated, an event can be published to the RabbitMQ queue.

Queue:

`alumni_donation_queue`

Example event information:

```text
Event: donor_prediction_created
Alumni ID: ALUM001
Propensity Score: 82.84
Category: High
```

RabbitMQ allows other services or background processes to consume these events without directly depending on the prediction API.

## Project Workflow

```text
1. Alumni Dataset
       |
       v
2. Data Preprocessing
       |
       v
3. Model Training
       |
       v
4. Model Serialization
       |
       v
5. Flask API
       |
       v
6. Redis Cache
       |
       v
7. RabbitMQ Messaging
       |
       v
8. Prediction Response
```

## Project Components

| Component | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Dataset handling |
| Scikit-learn | Machine learning and preprocessing |
| Logistic Regression | Donation propensity classification |
| Joblib | Model serialization |
| Flask | REST API |
| Redis | Prediction caching |
| RabbitMQ | Asynchronous messaging |
| Docker | Application packaging and deployment |
| Google Colab | Model development and testing |
| VS Code | Application development and integration |

## Model Testing

The trained model was tested using the 2025 alumni dataset.

Different alumni profiles were passed through the same trained pipeline to verify that the model could generate predictions for different records.

Example predictions:

| Alumni ID | Propensity Score | Category | Interpretation |
|---|---:|---|---|
| `ALM000002` | 84.68 | High | Likely to Donate |
| `ALM000003` | 93.41 | High | Likely to Donate |

These are individual prediction examples and are not overall model accuracy measurements.

## API and Infrastructure Testing

| Component | Status |
|---|---|
| Dataset | Completed |
| Model Training | Completed |
| Model Serialization | Completed |
| Flask API | Working |
| `/predict` Endpoint | Working |
| Redis Connection | Working |
| Redis Cache HIT/MISS | Verified |
| RabbitMQ Connection | Verified |
| RabbitMQ Message Publish/Receive | Verified |
| Dockerization | Next Stage |
| Public API using ngrok | Next Stage |
| Frontend Integration | Next Stage |

## Example System Flow

```text
Client
  |
  v
POST /predict
  |
  v
Check Redis
  |
  +---- Cache HIT ------> Return Existing Prediction
  |
  +---- Cache MISS
           |
           v
       ML Model
           |
           v
   Generate Probability
           |
           v
   Calculate Propensity Score
           |
           +--------> Store in Redis
           |
           +--------> Publish RabbitMQ Event
           |
           v
      Return JSON
```

## Project Structure

```text
Alumni-Donor-Propensity-Forecaster/
│
├── data/
│   └── alumni_donor_dataset_2025.csv
│
├── model/
│   └── alumni_donor_propensity_model_2025.pkl
│
├── app/
│   └── Flask API files
│
├── notebooks/
│   ├── Data Generation & Preprocessing
│   ├── Model Training & Evaluation
│   └── Model Testing
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Current Status

The core machine learning and API workflow has been completed.

The project currently supports:

- 2025 alumni dataset with 10,000 records.
- Trained Logistic Regression pipeline.
- Saved machine learning model.
- Donation probability prediction.
- Propensity score generation.
- High, Medium, and Low classification.
- Flask REST API.
- Redis caching.
- RabbitMQ event messaging.
- API health checking.
- Prediction testing with different alumni records.

## Future Improvements

1. Connect a frontend dashboard to the Flask API.
2. Make the API publicly accessible for testing.
3. Dockerize the complete application.
4. Add monitoring and logging.
5. Improve model evaluation and compare additional classification models.
6. Add authentication and API security.
7. Use real institutional alumni data with appropriate privacy and governance controls.
8. Add dashboards for analyzing alumni propensity groups.

## Important Note

This project is an ML-based propensity forecasting system. The prediction represents an estimated probability based on the information provided to the model. It does not guarantee that an alumnus will or will not donate.

For real-world deployment, appropriate data privacy, security, fairness, consent, and institutional governance practices should be followed.

## Conclusion

The Alumni Donor Propensity Forecaster provides a machine learning based approach for estimating alumni donation propensity.

The system combines a trained classification model with Flask, Redis, and RabbitMQ to create an API-based prediction workflow. Redis improves repeated prediction response time through caching, while RabbitMQ provides an asynchronous mechanism for distributing prediction events.

The project establishes a foundation for future alumni intelligence and fundraising-support applications.
