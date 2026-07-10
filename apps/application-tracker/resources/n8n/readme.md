# N8N Workflow

The `n8n_workflow.json` file contains the N8N workflow for processing incoming emails and forwarding them to the classification API.

## Import

1. Open N8N at `http://localhost:5678`
2. Go to **Workflows** → **Import from file**
3. Select `n8n_workflow.json`

## Flow

1. **Email Trigger** – polls the configured mailbox for new messages
2. **HTTP Request** – posts the email to `POST /api/classify_email`
3. The API classifies the email and stores relevant entries in the database
