import os
import pathlib
import json
from dotenv import load_dotenv
from jira import JIRA
from jira.resources import Issue

load_dotenv()

global EXPORT_EXTS
global project_key
global export_ext_key

if 'jira' not in globals():
  raise Exception('jira is not defined')

jira: JIRA = globals()['jira']

with open(f'./system-issueviews-plugin.json', mode='r') as f:
  EXPORT_EXTS = json.load(f)

project_key = os.getenv('JIRA_PROJECT_KEY')
export_ext_key = os.getenv('JIRA_EXPORT_EXT', 'doc')

if project_key is None:
  raise Exception('JIRA_PROJECT_KEY is not defined')
if export_ext_key not in EXPORT_EXTS:
  raise Exception('JIRA_EXPORT_EXT is not defined')

def main():
  export_ext = EXPORT_EXTS[export_ext_key]

  issue_container: set[Issue] = set()

  # list issues.
  while True:
    print('issues: ' + str(len(issue_container)))

    startAt = len(issue_container)

    issues = jira.search_issues(f'project={project_key}', startAt=startAt, properties='key', maxResults=1000)

    if len(issues) == 0:
      break

    issue_container.update(set(issues))

    # download.
    for issue in issue_container:
      print(issue.key)

      file_path = f"./tmp/{project_key}/{export_ext['ext']}/{issue.key}.{export_ext['ext']}"

      if os.path.exists(file_path):
        continue

      # makesure dir exists
      os.makedirs(os.path.dirname(file_path), exist_ok=True)

      with open(file_path, mode='wb') as f:
        response = jira._session.get(
          f"{jira.server_url}/si/jira.{export_ext['handler']}:{export_ext['key']}/{issue.key}/{issue.key}.{export_ext['ext']}",
          params={'downloadformat': export_ext['ext']},
          stream=True,
        )
        for chunk in response.iter_content(chunk_size=10 * 1024):
          f.write(chunk)

main()
