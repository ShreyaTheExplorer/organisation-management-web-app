from flask import Flask, jsonify, request
from extensions import db
from models import Department, Designation, Employee, Project, ProjectEmployee
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///organisation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# --- Root Route ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Welcome to the Employee Management API',
        'endpoints': {
            'departments': '/departments',
            'designations': '/designations',
            'employees': '/employees',
            'projects': '/projects'
        }
    })

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# --- Department Routes ---
@app.route('/departments', methods=['POST'])
def create_department():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    dept = Department(name=data['name'], description=data.get('description'))
    db.session.add(dept)
    db.session.commit()
    return jsonify(dept.to_dict()), 201

@app.route('/departments', methods=['GET'])
def get_departments():
    depts = Department.query.all()
    return jsonify([d.to_dict() for d in depts])

# --- Designation Routes ---
@app.route('/designations', methods=['POST'])
def create_designation():
    data = request.json
    required = ['class', 'salary', 'department_id']
    if not data or not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields: class, salary, department_id'}), 400
    
    desig = Designation(
        class_level=data['class'],
        salary=data['salary'],
        department_id=data['department_id']
    )
    db.session.add(desig)
    db.session.commit()
    return jsonify(desig.to_dict()), 201

@app.route('/designations', methods=['GET'])
def get_designations():
    desigs = Designation.query.all()
    return jsonify([d.to_dict() for d in desigs])

# --- Employee Routes ---
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    required = ['user_id', 'position', 'hire_date', 'department_id', 'designation_id']
    if not data or not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    emp = Employee(
        user_id=data['user_id'],
        position=data['position'],
        hire_date=hire_date,
        department_id=data['department_id'],
        designation_id=data['designation_id']
    )
    db.session.add(emp)
    db.session.commit()
    return jsonify(emp.to_dict()), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([e.to_dict() for e in employees])

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    emp = Employee.query.get_or_404(id)
    return jsonify(emp.to_dict())

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    emp = Employee.query.get_or_404(id)
    data = request.json
    
    if 'position' in data:
        emp.position = data['position']
    if 'department_id' in data:
        emp.department_id = data['department_id']
    if 'designation_id' in data:
        emp.designation_id = data['designation_id']
    if 'hire_date' in data:
        try:
             emp.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        except ValueError:
             return jsonify({'error': 'Invalid date format'}), 400

    db.session.commit()
    return jsonify(emp.to_dict())

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'})

# --- Project Routes ---
@app.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    if not data or 'name' not in data:
         return jsonify({'error': 'Name is required'}), 400
         
    start_date = None
    end_date = None
    if 'start_date' in data:
         try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
         except ValueError:
            pass # Or handle error
    if 'end_date' in data:
         try:
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
         except ValueError:
            pass

    proj = Project(
        name=data['name'],
        description=data.get('description'),
        start_date=start_date,
        end_date=end_date,
        status=data.get('status', 'Planned'),
        team_lead_employee_id=data.get('team_lead_employee_id')
    )
    db.session.add(proj)
    db.session.commit()
    return jsonify(proj.to_dict()), 201

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects])

@app.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    proj = Project.query.get_or_404(id)
    data = request.json
    
    if 'name' in data: proj.name = data['name']
    if 'description' in data: proj.description = data['description']
    if 'status' in data: proj.status = data['status']
    if 'team_lead_employee_id' in data: proj.team_lead_employee_id = data['team_lead_employee_id']
    if 'start_date' in data:
        try:
            proj.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            pass
    if 'end_date' in data:
        try:
            proj.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            pass
        
    db.session.commit()
    return jsonify(proj.to_dict())

@app.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    proj = Project.query.get_or_404(id)
    db.session.delete(proj)
    db.session.commit()
    return jsonify({'message': 'Project deleted'})

# --- Assignments ---
@app.route('/projects/<int:project_id>/assign', methods=['POST'])
def assign_employee(project_id):
    data = request.json
    employee_id = data.get('employee_id')
    if not employee_id:
        return jsonify({'error': 'employee_id is required'}), 400
        
    # Check existence
    Project.query.get_or_404(project_id)
    Employee.query.get_or_404(employee_id)
    
    # Check if already assigned
    existing = ProjectEmployee.query.filter_by(project_id=project_id, employee_id=employee_id).first()
    if existing:
        return jsonify({'message': 'Already assigned', 'id': existing.id}), 200
        
    assignment = ProjectEmployee(project_id=project_id, employee_id=employee_id)
    db.session.add(assignment)
    db.session.commit()
    return jsonify(assignment.to_dict()), 201

@app.route('/projects/<int:project_id>/remove/<int:employee_id>', methods=['DELETE'])
def remove_employee(project_id, employee_id):
    assignment = ProjectEmployee.query.filter_by(project_id=project_id, employee_id=employee_id).first_or_404()
    db.session.delete(assignment)
    db.session.commit()
    return jsonify({'message': 'Employee removed from project'})

if __name__ == '__main__':
    app.run(debug=True)
