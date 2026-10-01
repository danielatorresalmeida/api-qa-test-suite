# API QA Test Suite

Automated API testing project built with **Python, Requests and pytest**, with HTML reporting and GitHub Actions CI.

The project exercises the ReqRes API and demonstrates reusable API clients, positive and negative test scenarios, parametrized tests and automated reporting.

## ✨ Highlights

- 🐍 Python + pytest test automation
- 🌐 HTTP requests with Requests
- ✅ Positive and negative API scenarios
- 🔁 Parametrized tests
- 🧩 Reusable API client
- 🔐 API key configuration through environment variables
- 📊 HTML test reports with pytest-html
- ⚙️ GitHub Actions CI
- 🌍 Published report through GitHub Pages

## 🧪 Current Test Coverage

The current suite collects **5 test scenarios**.

### User list

`GET /users?page=2`

Checks:

- HTTP `200`
- response is valid JSON
- expected page is returned
- `data` is a non-empty list
- each user contains the expected fields
- essential field types are validated
- email values contain `@`

### Existing users

`GET /users/{id}`

The test is parametrized for:

- user `1`
- user `2`
- user `3`

Checks:

- HTTP `200`
- `data` exists
- returned user structure is valid
- returned ID matches the requested ID

### Unknown user

`GET /users/23`

Checks:

- HTTP `404`

## 🛠️ Tech Stack

- Python
- pytest
- Requests
- pytest-html
- GitHub Actions
- GitHub Pages

## 📂 Project Structure

```text
api-qa-test-suite/
├── .github/
│   └── workflows/
├── config/
├── docs/
├── tests/
│   ├── conftest.py
│   └── test_reqres_smoke.py
├── utils/
│   └── api_client.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## ▶️ Running Locally

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Set the ReqRes API key as an environment variable.

### PowerShell

```powershell
$env:REQRES_API_KEY="your-api-key"
```

Run the tests:

```bash
python -m pytest -q
```

Generate the HTML report:

```bash
python -m pytest --html=docs/assets/reports/api-qa/index.html --self-contained-html --css=config/pytest-html.css
```

## 🔐 API Configuration

The default API target is:

```text
https://reqres.in/api
```

The API key must not be committed to the repository.

It is read from:

```text
REQRES_API_KEY
```

When running locally without an API key, live API tests are skipped.

In GitHub Actions, missing API configuration causes the workflow to fail rather than producing a misleading successful result.

## ⚙️ Continuous Integration

GitHub Actions runs the suite on:

- pull requests
- pushes to `main`
- manual workflow dispatch

The workflow:

1. installs Python and project dependencies;
2. runs the API tests;
3. generates an HTML report;
4. uploads the report as a workflow artifact;
5. updates the published report on `main`.

## 📊 Test Report

[View the published API QA report](https://danielatorresalmeida.github.io/api-qa-test-suite/assets/reports/api-qa/)

The result shown there reflects the latest published workflow execution.

## 🎯 Purpose

This repository is a portfolio project focused on API quality assurance and test automation.

It demonstrates:

- API test design
- positive and negative testing
- parametrization
- reusable test infrastructure
- HTTP and JSON validation
- environment-based configuration
- automated reporting
- CI integration

---

Built and maintained by **Daniela Torres Almeida**.