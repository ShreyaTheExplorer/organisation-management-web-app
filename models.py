from extensions import db
from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.Text)
    google_id = db.Column(db.String(255), unique=True)
    profile_pic = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'profile_pic': self.profile_pic
        }

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Designation(db.Model):
    __tablename__ = 'designation'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    class_level = db.Column(db.Integer, nullable=False) # Maps to 'class'
    salary = db.Column(db.Numeric(10, 2), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    
    department = db.relationship('Department', backref='designations')

    def to_dict(self):
        return {
            'id': self.id,
            'class': self.class_level,
            'salary': float(self.salary) if self.salary else 0.0,
            'department_id': self.department_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    user_id = db.Column(db.Integer, nullable=False) 
    position = db.Column(db.Text, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    designation_id = db.Column(db.Integer, db.ForeignKey('designation.id'), nullable=False)

    department = db.relationship('Department', backref='employees')
    designation = db.relationship('Designation', backref='employees')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'position': self.position,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'department_id': self.department_id,
            'designation_id': self.designation_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.Text)
    team_lead_employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    team_lead = db.relationship('Employee', backref='projects_led')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'team_lead_employee_id': self.team_lead_employee_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProjectEmployee(db.Model):
    __tablename__ = 'project_employee'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    
    project = db.relationship('Project', backref='assignments')
    employee = db.relationship('Employee', backref='assignments')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'employee_id': self.employee_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
