from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# Create an instance of flask
app = Flask(__name__)
# Creating an API object
api = Api(app)
# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Sqlalchemy Mapper
db = SQLAlchemy(app)

# add a class
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(88), nullable=False)
    lastname = db.Column(db.String(88), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    salary = db.Column(db.Float)

    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.gender} - {self.salary}" 

with app.app_context():
    emp = Employee(firstname="Saif", lastname="AlHarmi", gender="Male", salary=60000)
    db.session.add(emp)
    db.session.commit()
    print(emp.query.all())


# For GET request to http://127.0.0.1:5000/
class GetEmployee(Resource):
    def get(self):
        employees = Employee.query.all()
        emp_list = []
        for emp in employees:
            emp_data = {'Id': emp.id, 'FirstName': emp.firstname, 'LastName': emp.lastname,
                        'Gender': emp.gender, 'Salary': emp.salary}
            emp_list.append(emp_data)
        return emp_list


# For POST request to http:127.0.0.1:5000/employee
class AddEmployee(Resource):
    def post(self):
        if request.is_json:
            emp = Employee(firstname=request.json['FirstName'], lastname=request.json['LastName'],
                        gender=request.json['Gender'], salary=request.json['Salary'])
            db.session.add(emp)
            db.session.commit()

            #returning a json response
            return make_response(jsonify({'Id': emp.id, 'FirstName': emp.firstname,
                                        'LastName': emp.lastname,'Gender': emp.gender,
                                        'Salary': emp.salary}),201)
        else:
            return {'error': 'Request must be JSON'}, 400
        

# For PUT request to http://127.0.0.1:5000/update/?
class UpdateEmployee(Resource):
    def put(self, id):
        if request.is_json:
            emp = Employee.query.get(id)
            if emp is None:
                return {'error': 'not found'}, 484
            else:
                emp.firstname = request.json['FirstName']
                emp.lastname = request.json['LastName']
                emp.gender = request.json['Gender']
                emp.salary= request.json['Salary']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400
        
# For delete request to http://127.0.0.1:500/delete/?
class DeleteEmployee(Resource):
    def delete(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'error': 'not found'}, 484
        db.session.delete(emp)
        db.session.commit()
        return f'{id} is deleted', 200
    
api.add_resource(GetEmployee, '/')
api.add_resource(AddEmployee, '/add')
api.add_resource(UpdateEmployee, '/update/<int:id>')
api.add_resource(DeleteEmployee, '/delete/<int:id>')

#
if __name__ == '__main__':
    app.run(debug=True)