#loading flask libraries
import flask
import hashlib

from flask import jsonify
from flask import request, make_response

import sql
from sql import create_connection
from sql import execute_read_query
from sql import execute_update_query

import creds


#create application with configuration
app = flask.Flask(__name__)
app.config["DEBUG"]=True #to show errors in browser

masterPassword = "c9f60108ce2cf9d828075088235383616d7586cbe9ee31a7032218ed434240ee"  # Hash value of Password 'password' 
masterUsername = 'username'

# basic http authentication, prompts username and password upon contacting the endpoint

# 'password' as plaintext should not be used to verify authorization to access. 
# the password should be hashed and the hash should be compared to the stored password hash in the database
@app.route('/authenticatedroute', methods=['GET'])
def auth_test():
    if request.authorization:
        encoded = request.authorization.password.encode() #unicode encoding
        hasedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hasedResult.hexdigest() == masterPassword:
            return '<h1> Authorized user access </h1>'
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

#create an endpoint to run default home page request
@app.route('/', methods=['GET'])
def home():
    return "<h1> Welcome </h1>"

#//////////////////////////////FACILITY///////////////////////////////////////////////////////
#get one facility
@app.route('/api/facility', methods=['GET'])
def api_facility_by_id():
   
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error: No ID is provided!'
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from facility"
    facilitylist = execute_read_query(myconn, mysqlst)
    results = []
    for facility in facilitylist:
        if facility['id']== id:
            results.append(facility)
    return jsonify(results)

#get all facilities
@app.route('/api/faciliy/all', methods=['GET'])
def all_facility_info():
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from facility"
    facilitylist = execute_read_query(myconn, mysqlst)
    return jsonify(facilitylist)

#add a facility
@app.route('/api/facility', methods=['POST'])
def api_add_facility():
    request_data = request.get_json()
    newFacname = request_data['name']
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "insert into facility(name) values ('%s')" % (newFacname)

    execute_update_query(myconn, sql)
    return 'Add facility request successful!'

#update at id#
@app.route('/api/facility', methods=['PUT'])
def api_update_facility_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    newFacname = request_data['name']
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "UPDATE facility SET name = '%s' WHERE id = '%s'" % (newFacname, idtoupdate)

    execute_update_query(myconn, sql)
        
    return "Update request successful!"

#delete at id#
@app.route('/api/facility', methods=['DELETE'])
def api_delete_facility_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "DELETE FROM facility where id = '%s'" % (idtoupdate)

    execute_update_query(myconn, sql)
        
    return "Delete request successful!"

#/////////////////////////////////////CLASSROOM////////////////////////////////////////////////
#get one classroom
@app.route('/api/classroom', methods=['GET'])
def api_classroom_by_id():
   
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error: No ID is provided!'
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from classroom"
    classroomlist = execute_read_query(myconn, mysqlst)
    results = []
    for classes in classroomlist:
        if classes['id']== id:
            results.append(classes)
    return jsonify(results)

#get all classrooms
@app.route('/api/classroom/all', methods=['GET'])
def all_classroom_info():
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from classroom"
    classlist = execute_read_query(myconn, mysqlst)
    return jsonify(classlist)

#add a classroom
@app.route('/api/classroom', methods=['POST'])
def api_add_classroom():
    request_data = request.get_json()
    newcapa = request_data['capacity']
    newname = request_data['name']
    newfaca = request_data['facility']

    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "insert into classroom(capacity, name, facility) values ('%s','%s','%s')" % (newcapa, newname, newfaca)

    execute_update_query(myconn, sql)
    return 'Add classroom request successful!'

#update at id#
@app.route('/api/classroom', methods=['PUT'])
def api_update_classroom_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    newcapa = request_data['capacity']
    newname = request_data['name']
    newfaca = request_data['facility']
    
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "UPDATE classroom SET capacity = '%s', name = '%s', facility = '%s' WHERE id = '%s'" % (newcapa, newname, newfaca, idtoupdate)

    execute_update_query(myconn, sql)
        
    return "Update request successful!"

#delete at id#
@app.route('/api/plants', methods=['DELETE'])
def api_delete_plant_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "DELETE FROM plants where id = '%s'" % (idtoupdate)

    execute_update_query(myconn, sql)
        
    return "Delete request successful!"

#////////////////////////////////////////TEACHER//////////////////////////////////////////////////
#get one teacher
@app.route('/api/teacher', methods=['GET'])
def api_teacher_by_id():
   
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error: No ID is provided!'
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from teacher"
    teacherlist = execute_read_query(myconn, mysqlst)
    results = []
    for teacher in teacherlist:
        if teacher['id']== id:
            results.append(teacher)
    return jsonify(results)

#get all teachers
@app.route('/api/teacher/all', methods=['GET'])
def all_teachers_info():
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from teacher"
    plantslist = execute_read_query(myconn, mysqlst)
    return jsonify(plantslist)

#add a teacher
@app.route('/api/teacher', methods=['POST'])
def api_add_teacher():
    request_data = request.get_json()
    newfname = request_data['firstname']
    newlname = request_data['lastname']
    newroom = request_data['room']

    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "insert into teacher(firstname, lastname, room) values ('%s','%s','%s')" % (newfname, newlname, newroom)

    execute_update_query(myconn, sql)
    return 'Add teacher request successful!'

#update at id#
@app.route('/api/teacher', methods=['PUT'])
def api_update_teacher_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    newfname = request_data['firstname']
    newlname = request_data['lastname']
    newroom = request_data['room']
    
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "UPDATE teacher SET firstname = '%s', lastname = '%s', room = '%s' WHERE id = '%s'" % (newfname, newlname, newroom, idtoupdate)

    execute_update_query(myconn, sql)
        
    return "Update teacher request successful!"

#delete at id#
@app.route('/api/teacher', methods=['DELETE'])
def api_delete_teacher_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "DELETE FROM teacher where id = '%s'" % (idtoupdate)

    execute_update_query(myconn, sql)
        
    return "Delete request successful!"

#//////////////////////////////////////////CHILD////////////////////////////////////////////////////



#run the application to listen for user requests
app.run()

