from datetime import datetime

from notion_scripts.requests.read_tasks import read_tasks

a = datetime.now()
read_tasks()
b = datetime.now()
c = datetime.now()

print(b - a,
      c - b)
