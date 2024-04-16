#loading flask libraries
import flask
import hashlib
import math
from flask import jsonify
from flask import request, make_response
from functools import wraps
import sql
from sql import create_connection
from sql import execute_read_query
from sql import execute_update_query
import creds

#create application with configuration
app = flask.Flask(__name__)
app.config["DEBUG"]=True #to show errors in browser

masterPassword = "c9f60108ce2cf9d828075088235383616d7586cbe9ee31a7032218ed434240ee"  # Hash value of Password 'CIS3368Project' 
masterUsername = 'username'

# basic http authentication, prompts username and password upon contacting the endpoint
#information on wraps was learned from https://circleci.com/blog/authentication-decorators-flask/
def basic_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated
def check_auth(username, password):
    encoded = password.encode()
    hashedResult = hashlib.sha256(encoded).hexdigest()
    return username == masterUsername and hashedResult == masterPassword

#create an endpoint to run default home page request
@app.route('/', methods=['GET'])
#@basic_authentication
def home():
    return "<h1> Welcome </h1>"

#//////////////////////////////FACILITY///////////////////////////////////////////////////////
#get one facility
@app.route('/api/facility', methods=['GET'])
#@basic_authentication
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
@app.route('/api/facility/all', methods=['GET'])
#@basic_authentication
def all_facility_info():
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from facility"
    facilitylist = execute_read_query(myconn, mysqlst)
    return jsonify(facilitylist)

#add a facility
@app.route('/api/facility', methods=['POST'])
#@basic_authentication
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
#@basic_authentication
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
#@basic_authentication
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
#@basic_authentication
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
#@basic_authentication
def all_classroom_info():
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from classroom"
    classlist = execute_read_query(myconn, mysqlst)
    return jsonify(classlist)

#add a classroom
@app.route('/api/classroom', methods=['POST'])
#@basic_authentication
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
#@basic_authentication
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
@app.route('/api/classroom', methods=['DELETE'])
#@basic_authentication
def api_delete_plant_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "DELETE FROM classroom where id = '%s'" % (idtoupdate)
    execute_update_query(myconn, sql)
    return "Delete request successful!"

#////////////////////////////////////////TEACHER//////////////////////////////////////////////////
#get one teacher
@app.route('/api/teacher', methods=['GET'])
#@basic_authentication
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
#@basic_authentication
def all_teachers_info():
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from teacher"
    teacherlist = execute_read_query(myconn, mysqlst)
    return jsonify(teacherlist)

#add a teacher
@app.route('/api/teacher', methods=['POST'])
#@basic_authentication
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
#@basic_authentication
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
#@basic_authentication
def api_delete_teacher_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "DELETE FROM teacher where id = '%s'" % (idtoupdate)
    execute_update_query(myconn, sql)
    return "Delete request successful!"

#//////////////////////////////////////////CHILD////////////////////////////////////////////////////
#get one child
@app.route('/api/child', methods=['GET'])
#@basic_authentication
def api_child_by_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error: No ID is provided!'
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from child"
    childlist = execute_read_query(myconn, mysqlst)
    results = []
    for child in childlist:
        if child['id']== id:
            results.append(child)
    return jsonify(results)

#get all children
@app.route('/api/child/all', methods=['GET'])
#@basic_authentication
def all_child_info():
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from child"
    childlist = execute_read_query(myconn, mysqlst)
    return jsonify(childlist)

#add a child
@app.route('/api/child', methods=['POST'])
#@basic_authentication
def api_add_child():
    request_data = request.get_json()
    newfname = request_data['firstname']
    newlname = request_data['lastname']
    newage = request_data['age']
    newroom = request_data['room']
    newage = int(newage)
    newroom = int(newroom)

    #count all childs in a room
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from child"
    childlist = execute_read_query(myconn, mysqlst)
    childclasscount = 0
    for child in childlist:
        for key, value in child.items():
            if (key=='room') and (value== newroom):
                childclasscount = childclasscount + 1

    #count all teachers to a room
    mysqlst = "select * from teacher"
    teacherlist = execute_read_query(myconn, mysqlst)
    teacherclasscount = 0
    for teacher in teacherlist:
        for key, value in teacher.items():
            if (key=='room') and (value== newroom):
                teacherclasscount = teacherclasscount + 1

    #check capacity of a room
    mysqlst = "select * from classroom"
    classroomlist = execute_read_query(myconn, mysqlst)
    results = []
    for classroom in classroomlist:
        for key, value in classroom.items():
            if (key=='id') and (value==newroom):
                results.append(classroom)

    capacitycount = results[0]['capacity']

    #if all conditions met, then accept child into classroom
    if (childclasscount < capacitycount) and (math.ceil(childclasscount/10) <= teacherclasscount):
        sql = "insert into child(firstname, lastname, age, room) values ('%s','%s','%s','%s')" % (newfname, newlname, newage, newroom)
        execute_update_query(myconn, sql)
        return 'Add child request successful!'
    else:
        return 'Class full or something went wrong'

   
#update at id#
@app.route('/api/child', methods=['PUT'])
#@basic_authentication
def api_update_child_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    newfname = request_data['firstname']
    newlname = request_data['lastname']
    newage = request_data['age']
    newroom = request_data['room']
    idtoupdate = int(idtoupdate)
    newage = int(newage)
    newroom = int(newroom)
    
    

    #count all childs in a room
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    mysqlst = "select * from child"
    childlist = execute_read_query(myconn, mysqlst)
    childclasscount = 0
    sameRoomFlag = 0
    for child in childlist:
        print(type(child['room']))
        if child['room']== newroom:
            childclasscount = childclasscount + 1
        #check if the child being updated wil remain in the same class
        if (child['id'] == idtoupdate) and (child['room'] == newroom):
            sameRoomFlag = sameRoomFlag + 1


    #count all teachers to a room
    mysqlst = "select * from teacher"
    teacherlist = execute_read_query(myconn, mysqlst)
    teacherclasscount = 0
    for teacher in teacherlist:
        if teacher['room']== newroom:
            teacherclasscount = teacherclasscount + 1

    #check capacity of a room
    mysqlst = "select * from classroom"
    classroomlist = execute_read_query(myconn, mysqlst)
    results = []
    for classroom in classroomlist:
        if classroom['id']== newroom:
            results.append(classroom)
    capacitycount = results[0]['capacity']

    #if all conditions met, then accept child update
    #sameRoomFlag will check if the child will remain in the same room
    if sameRoomFlag == 1:
        sql = "UPDATE child SET firstname = '%s', lastname = '%s', age = '%s', room = '%s' WHERE id = '%s'" % (newfname, newlname, newage, newroom, idtoupdate)
        execute_update_query(myconn, sql)
        return 'Update child request successful!'
    elif (childclasscount < capacitycount) and (math.ceil(childclasscount/10) <= teacherclasscount):
        sql = "UPDATE child SET firstname = '%s', lastname = '%s', age = '%s', room = '%s' WHERE id = '%s'" % (newfname, newlname, newage, newroom, idtoupdate)
        execute_update_query(myconn, sql)
        return 'Update child request successful!'
    else:
        return 'Class full or something went wrong'

#delete at id#
@app.route('/api/child', methods=['DELETE'])
#@basic_authentication
def api_delete_child_byID():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    
    mycreds = creds.creds()
    myconn = create_connection(mycreds.myhostname, mycreds.uname, mycreds.passwd, mycreds.dbname)
    sql = "DELETE FROM child where id = '%s'" % (idtoupdate)

    execute_update_query(myconn, sql)
        
    return "Delete request successful!"

#run the application to listen for user requests
app.run()