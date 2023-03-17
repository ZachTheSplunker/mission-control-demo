# Mission Control Remediation

Useful playbooks to be used with Mission Control

## How do I use these playbooks?

- [Add this repo as a Git source to Splunk SOAR](#add-this-repo-to-soar).
- [Add the "Protect Users and Assets" to the Encoded PowerShell Detection Response plan](#add-playbook-to-response-plan-in-mission-control).

### Add this repo to SOAR

1. In Splunk Soar, Navigate to Administration > Administration Settings > Source Control
2. From the "Repositories" drop down, select "Configure a new repository."
3. Repo URL: `https://github.com/ZachTheSplunker/mission-control-demo.git` 
4. Branch Name: `main`
5. Check (Enable) "Read Only"
6. Save Changes

![Source Control](img/soar_source_control.png)

### Add playbook to Response plan in Mission Control

1. In Mission Control, Navigate to Content.
2. Select the Response Plan "Encoded PowerShell Detection Response."
3. For the "Render Verdict" phase, Select the task "Take Remediation Action or Close Incident."
4. Add the Playbook `Protect Users and Assets` to the task. 

![Response Plan](img/mc_response_plan.png)