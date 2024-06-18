

 4871  python ../load_data.py --project_id rbsee-sandbox-asdf001 --dataset_id testreg --mode all_schemas --folder_path /Users/nikos/workspace/python/bqregistry/schemas
 4872  python add_project_to_project_code.py "test" "APP0" "nonp"\n
 4873  python add_project.py "001" "napp0-006-test" "A description" "napp0-001-test-111" "lz_456" "nonp" "sol_789"\n
 4874  python add_project.py "001" "napp0-006-test" "A description" "napp0-001-test-111" "lz_456" "prod" "sol_789"\n
 4875  python add_project.py "001" "papp0-006-test" "A description" "papp0-001-test-111" "lz_456" "prod" "sol_789"\n
 4876  python add_project.py "001" "papp0-001-test" "A description" "papp0-001-test-111" "lz_456" "prod" "sol_789"\n
 4877  python add_project_to_project_code.py "secrets" "APP2" "nonp"\n
 4878  python add_project.py "002" "papp0-001-test" "A description" "papp0-001-test-111" "lz_456" "nonp" "sol_789"\n
 4879  python add_project.py "002" "papp0-001-test" "A description" "papp0-001-test-111" "lz_456" "prod" "sol_789"\n