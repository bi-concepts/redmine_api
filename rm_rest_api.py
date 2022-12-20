#/** 
  # Python Skript für Redmine API-Aufruf
  #
  # @author BI-Concepts GmbH
  # @param t -> task as string
  # @param i -> id as integer
  # @param v -> value as integer
  # @return
  #/


import sys
from redminelib import Redmine

task = sys.argv[1]
ids = sys.argv[2]
value = sys.argv[3]

redmine = Redmine('http://localhost:3001', username='admin', password='Open9893@q')
project = redmine.project.get(1)

#gii-getissueinfo
if task == 'gii': 
  issue = redmine.issue.get (ids, include=['children'])
#gid-getissuedetails
if task == 'gid': 
  issue = redmine.issue.get (ids, include=['children', 'journals', 'watchers'])
#uis-updateissuestatus value 1-Neu 2-inBearbeitung 3-Geloest 4-Feedback 5-erledigt 6-abgewiesen
if task == 'uis':
  issue = redmine.issue.update (ids, status_id=value)
#uip-updateissueprogress value progress in %
if task == 'uip':
  issue = redmine.issue.update (ids, done_ratio=value)
#sin-setissuenumber value AlbakomTicketNummer
if task == 'sin':
  issue = redmine.issue.update (ids, custom_fields=[{'id':4, 'value':value}])  
issue
#for eachArg in issue:
#  print(eachArg)
print(issue)
