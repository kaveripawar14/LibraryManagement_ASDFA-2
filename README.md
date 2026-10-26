# Library Management System — CI/CD Mini Project

## Aim
Build a simple library application and demonstrate an Agile CI/CD workflow using GitHub Actions.

## Features
- View the book catalogue and availability.
- Add a book.
- Issue an available book.
- Return an issued book.

## Run locally (Python 3.10+)
```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

Run automated tests:
```bash
python -m unittest -v
```

## CI/CD pipeline
GitHub Actions runs on each push and pull request to `main`:
1. Checkout source code from GitHub.
2. Set up Python and install dependencies (Build/setup).
3. Run automated unit tests.
4. Run a code quality check using Ruff.
5. Deploy to Render using a deploy hook when the `RENDER_DEPLOY_HOOK_URL` repository secret is configured and the `main` branch workflow succeeds.

## Agile plan
### User stories
1. As a librarian, I want to view all books so I can check availability.
2. As a librarian, I want to add a book so the catalogue stays updated.
3. As a librarian, I want to issue an available book to a reader.
4. As a librarian, I want to mark an issued book as returned.
5. As a librarian, I want the system to show availability clearly.

### Sprint planning
- Sprint 1: View catalogue, add a book, and show book status.
- Sprint 2: Issue/return books, automated tests, and CI/CD workflow.

### Definition of Done (DoD)
- Feature works as expected.
- Automated tests pass.
- Code quality check passes.
- Code is pushed to GitHub.
- Workflow result is reviewed; deployment is successful when configured.

### Acceptance criteria — Issue a book
- Given a book is marked Available, when the librarian selects Issue, its status changes to Issued.
- An issued book cannot be issued again.
- The page displays the updated status after the action.

## Deployment to Render
Create a Render Web Service connected to this GitHub repository.
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Add `gunicorn` to `requirements.txt` before deploying.
- In Render, create a Deploy Hook and copy its URL.
- In GitHub repository: Settings → Secrets and variables → Actions → New repository secret.
- Name: `RENDER_DEPLOY_HOOK_URL`; value: the Render deploy hook URL.
- Push to `main`; after tests and Ruff pass, the workflow triggers deployment.

Note: this is a teaching demo and stores sample books in memory; it is not a production database.
