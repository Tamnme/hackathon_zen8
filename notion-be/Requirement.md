# 📘 API Requirement Document

## 🌟 Purpose
This API set will enable secure storage of third-party secrets (Notion & Slack), manage analytics trigger processes, schedule automatic triggers based on time, and retrieve historical results for review.

---

## 📌 Database Schema Design

### Summary Histories Table
| Field Name          | Type        | Description                           |
|----------------------|-------------|---------------------------------------|
| `email`              | String (PK) | User's email (Primary Key)            |
| `status`             | Enum        | start, in_progress, success, failed   |
| `start_time`         | Timestamp   | When the summary process started      |
| `end_time`           | Timestamp   | When the summary process ended        |
| `channels`           | String      | Slack channel or notification path    |
| `notion_page_url`    | String      | URL of the Notion page                |

### App Settings Table
| Field Name           | Type        | Description                           |
|-----------------------|-------------|---------------------------------------|
| `email`               | String (PK) | User's email (Primary Key)            |
| `schedule_period`     | String      | Schedule expression or period         |
| `default_channels`    | String      | Default Slack channel or other targets|
| `get_notion_page`     | String      | Method or static URL to get Notion    |
| `slack_token`         | String      | Slack API token                       |
| `notion_secret`       | String      | Notion secret token                   |
| `notion_page_id`      | String      | Notion Page ID                        |

### Trigger Settings Table
| Field Name           | Type        | Description                           |
|-----------------------|-------------|---------------------------------------|
| `email`               | String      | User's email                          |
| `channels`            | String      | Target channels for notification      |
| `start_date`          | Date        | Start date for automated triggers     |
| `end_date`            | Date        | End date for automated triggers       |

---

## 🚀 App Flow

1. **Create App Settings & Trigger Settings**
    - Input Email, Tokens, Page IDs, Schedule, Channels into the database.
2. **Trigger Summary**
    - Call manual trigger which creates a record in Summary Histories table.
3. **Insert Summary Result**
    - On process completion, update the Summary History entry with status, end time, and Notion page URL.

---

## 💡 Required APIs

### 1. Get Summary Histories
**GET** `/api/summary-histories`
- Query: `email`, `limit`, `page`
- Returns a paginated list of history entries.

### 2. Get App Setting by Email
**GET** `/api/app-settings`
- Query: `email`
- Returns app setting object for the email.

### 3. Get Trigger Settings by Email
**GET** `/api/trigger-settings`
- Query: `email`
- Returns trigger setting object for the email.

### 4. Create App Settings
**POST** `/api/app-settings`
- Body: Full JSON object for the App Settings table.

### 5. Create Trigger Settings
**POST** `/api/trigger-settings`
- Body: Full JSON object for the Trigger Settings table.

### 6. Trigger Summary (Draft Function)
**POST** `/api/summary/trigger`
- Body: `{ "email": "string", "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD" }`
- Response: `202 Accepted` with `trigger_id`.

### 7. Insert/Update Summary Result
**POST** `/api/summary-histories`
- Body: Full Summary History data, including `email`, `status`, `channels`, `notion_page_url`, `start_time`, `end_time`.

### Additional Suggested APIs:
- `/api/summary-histories/{id}` - GET a single summary by ID.
- `/api/app-settings/{email}` - PUT to update app settings.
- `/api/trigger-settings/{email}` - PUT to update trigger settings.

---

## 🔢 Test Cases Document

### 1. Test Case: Create App Settings
- **Input:** Valid JSON body.
- **Expected Result:** `201 Created`, database entry is saved.

### 2. Test Case: Create Trigger Settings
- **Input:** Valid JSON body.
- **Expected Result:** `201 Created`, settings saved in DB.

### 3. Test Case: Trigger Summary
- **Input:** Valid email, start date, end date.
- **Expected Result:** `202 Accepted`, entry in Summary Histories with status `start`.

### 4. Test Case: Insert Summary History
- **Input:** Valid JSON with status, start time, end time, notion URL.
- **Expected Result:** `200 OK` or `201 Created`, database entry updated or inserted.

### 5. Test Case: Get Summary Histories
- **Input:** Email filter, pagination params.
- **Expected Result:** List of histories for that email.

### 6. Test Case: Get App Setting by Email
- **Input:** Existing email.
- **Expected Result:** App setting JSON object.

### 7. Test Case: Get Trigger Setting by Email
- **Input:** Existing email.
- **Expected Result:** Trigger setting JSON object.

### 8. Negative Test: Invalid Email Format
- **Input:** Bad email syntax.
- **Expected Result:** `400 Bad Request`.

### 9. Negative Test: Empty Required Field
- **Input:** Missing `email`.
- **Expected Result:** `400 Bad Request`.

---

🚀 Now you can pass this document to AI Coding Assistant to generate code, test cases, and DB migration scripts! Let me know if you want help generating the OpenAPI JSON or YAML file too.

