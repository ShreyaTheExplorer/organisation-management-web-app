import sys
import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:5000"

def req(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    req_data = json.dumps(data).encode('utf-8') if data else None
    
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            print(f"{method} {endpoint}: {response.status}")
            if response.status != 204:
                return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error {method} {endpoint}: {e.code} - {e.read().decode()}")
        return None
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

try:
    # 1. Create Department
    print("--- Creating Department ---")
    dept = req('/departments', 'POST', {'name': 'Engineering', 'description': 'Software Dev'})
    if not dept: sys.exit(1)
    print(dept)
    dept_id = dept['id']

    # 2. Create Designation
    print("\n--- Creating Designation ---")
    desig = req('/designations', 'POST', {'class': 1, 'salary': 50000, 'department_id': dept_id})
    if not desig: sys.exit(1)
    print(desig)
    desig_id = desig['id']

    # 3. Create Employee
    print("\n--- Creating Employee ---")
    emp = req('/employees', 'POST', {
        'user_id': 101, 
        'position': 'Developer', 
        'hire_date': '2023-01-01',
        'department_id': dept_id,
        'designation_id': desig_id
    })
    if not emp: sys.exit(1)
    print(emp)
    emp_id = emp['id']

    # 4. Create Project
    print("\n--- Creating Project ---")
    proj = req('/projects', 'POST', {
        'name': 'Alpha',
        'description': 'Top Secret',
        'start_date': '2024-01-01',
        'status': 'Active',
        'team_lead_employee_id': emp_id
    })
    if not proj: sys.exit(1)
    print(proj)
    proj_id = proj['id']

    # 5. Assign Employee to Project
    print("\n--- Assigning Employee ---")
    assign = req(f'/projects/{proj_id}/assign', 'POST', {'employee_id': emp_id})
    print(assign)

    # 6. List all verify
    print("\n--- Verification List ---")
    print("Projects:", req('/projects'))
    print("Employees:", req('/employees'))

except Exception as e:
    print(f"An unexpected error occurred: {e}")
