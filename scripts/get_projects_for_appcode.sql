SELECT p.project_id
FROM `rbsee-sandbox-asdf001.testreg.projects` p
JOIN `rbsee-sandbox-asdf001.testreg.project_codes` pc
ON p.project_code = pc.project_code
WHERE pc.appcode = 'APP0'
and service_tier = 'prod'


There's two different workflows that you need to cover.

Workflow 1: you need to create a new project record for an existing project code and a service tier. 
Workflow 2: you need to create a new project record for a service tier and an app code. This means you will need to determine the next available project_code that is not in_use, allocate it under that appcode in project_codes and then insert the new project.

Write all required sql queries for both workflows.