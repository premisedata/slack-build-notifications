# slack-build-notifcations
Github Action for build notifications to Slack

## Parameters

The parameters will be passed to the action through `with`

| Name  | Description  | Required?  |
|---|---|---|
| outcome  | build outcome  | Required  |
| project  | GCP project  | Required  |
| build  | build number - passed as github-provided env var  | Required  |
| webhook  | webhook url for slack app  | Required  |
| repo  | name of github repo  | Required  |
| version  | release version of the service  | Optional  |
| notes  | release description | Optional  |

## Usage

1. Create a directory named `.github/workflow/`

2. Create a YAML file, e.g. action_workflow.yml, and place it in the created directory above

3. Example content of the YAML file:

```
on:
  push:
    branches:
      - main
name: Deploy to GCP
jobs:
  deploy:
    name: deploy
    runs-on: ubuntu-latest
    env:
      GCLOUD_PROJECT: GCLOUD_PROJECT
    steps:
    - name: checkout
      uses: actions/checkout@v2
    - name: Setup Cloud SDK
      uses: google-github-actions/setup-gcloud@v0.2.0
      with:
        project_id: ${{ env.GCLOUD_PROJECT }}
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        export_default_credentials: true
    - name: Deploy to Cloud Run
      id: deploy
      uses: google-github-actions/deploy-cloudrun@v0.6.0
      with:
        service: ${{ env.SERVICE }}
        region: ${{ env.REGION }}
        suffix: ${{ github.sha }}
    - name: send slack message
      uses: premisedata/slack-build-notifications@v1.0
      if: always()
      with:
        outcome: ${{ steps.deploy.outcome }}
        project: ${{ env.GCLOUD_PROJECT }}
        build: ${{ github.run_id }}
        webhook: https://hooks.slack.com/services/your_slack_webhook
        repo: ${{ env.GITHUB_REPOSITORY }}
        version: ${{ env.VERSION }}
        notes: ${{ github.GITHUB_REF_NAME }}
```
