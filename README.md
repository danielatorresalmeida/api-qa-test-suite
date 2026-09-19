# API QA smoke test

A small Python / Requests / pytest project with a pytest-html report and GitHub Actions workflow.

## Actual coverage

One smoke test requests `GET /users` from the configured ReqRes API and checks:

- HTTP status is 200;
- the JSON response is an object;
- the response contains a `data` key.

This is not schema validation, business-rule coverage, a regression suite or a release-readiness assessment. The reusable client exposes other HTTP methods, but those methods do not imply additional test coverage.

## Run

Install Python and run `python -m pip install -r requirements.txt` in this directory. Set `REQRES_API_KEY` in your local environment (never commit a real key to `config/settings.json`), then run:

```sh
python -m pytest --html=docs/assets/reports/api-qa/index.html --self-contained-html --css=config/pytest-html.css
```

Without a key, a local run skips the smoke test: **skipped is not passed**. In GitHub Actions, missing configuration fails the test instead of producing a misleading green run. Configure the `REQRES_API_KEY` repository Actions secret to execute against ReqRes. An invalid key or unexpected response also fails the test.

## CI and report

Test failures keep the workflow failed. The report is uploaded as an artifact when generated, including on failed test runs; on `main`, the workflow also commits the generated report for Pages. Pull requests never commit reports back to the repository. Do not infer success from the existence of an HTML report: read its date, target, mode and results.

[Published report](https://danielatorresalmeida.github.io/api-qa-test-suite/assets/reports/api-qa/) — the audited report from 28 February 2026 contained **0 passed / 1 skipped** and did not validate the live endpoint. The current result depends on the latest workflow and configured key.

There is no separate build or lint command configured.
