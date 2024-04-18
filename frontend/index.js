//Template from class 11 template
//Login page from class 9 template

const express = require('express')
var path = require('path');
var bodyParser = require('body-parser');
const app = express();
const port = 3000;
var f_items = null;
var cl_items = null;
var t_items = null;
var ch_items = null;

const axios = require('axios');
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
//setup public folder
app.use(express.static('./public'));
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));
// parse application/json
app.use(bodyParser.json());

//login page
app.get('/',function (req, res) {
    res.render('pages/login')
});
//home page
app.get('/home',function (req, res) {
    res.render('pages/home')
});

//check login
app.post('/process_login', function(req, res){
    var user = req.body.username;
    var password = req.body.password;
    // This sample is showing how to validate user input with static username and password
    // If you want to validate database user data then you need to call REST API for it to get user data
    // Then validate user input with user data retrived from database.
    if(user === 'admin' && password === 'CIS3368Project')
    {
        res.render('pages/continue.ejs', {
            user: user,
            auth: true
        });
    }
    else
    {
        res.render('pages/continue.ejs', {
            user: 'UNAUTHORIZED',
            auth: false
        });
    }
  });
///////////////////////////////////////////FACILITY////////////////////////////////////////////////////////////////
// all facilities
app.get('/facility',function (req, res) {

    axios.get('http://127.0.0.1:5000/api/facility/all')
    .then((response)=>{
        f_items = response.data;
        console.log(f_items);
        res.render('pages/facility',{
            facility:f_items
        });
    });
})

// single facility
app.post('/s_facility', function (req, res) {
var message = req.body.IdtoSearch;
var initial_api = 'http://127.0.0.1:5000/api/facility?id='
initial_api = initial_api + message;

axios.get(initial_api)
    .then((response)=>{
        let s_items = response.data;
        console.log(s_items);
        res.render('pages/facility',{
            facility:f_items, 
            s_facility:s_items
        });
    });
})

// add facility
app.post('/a_facility', function (req, res) {
    var message2 = req.body.nametoadd;
    var initial_api = 'http://127.0.0.1:5000/api/facility'

    axios.post(initial_api, {
        name:message2
    })
    .then((response) => {
        let a_item = response.data;
        console.log(a_item);
        res.render('pages/facility', {
            facility: f_items, 
            a_facility: a_item
        });
    })

});

// update facility
app.post('/u_facility', function (req, res) {
    var message3 = req.body.idtoupdate;
    var message4 = req.body.nametoupdate;
    var initial_api = 'http://127.0.0.1:5000/api/facility'

    axios.put(initial_api, {
            id:message3, 
            name:message4
        
    })
    .then((response) => {
        let updatedItem = response.data;
        console.log(updatedItem);
        res.render('pages/facility', {
            facility: f_items, 
            u_facility: updatedItem
        });
    })

});

// delete facility
app.post('/d_facility', function (req, res) {
    var message5 = req.body.factodel;
    var initial_api = 'http://127.0.0.1:5000/api/facility'

    axios.delete(initial_api, {data: {
        id:message5
    }
    })
    .then((response) => {
        let d_item = response.data;
        console.log(d_item);
        res.render('pages/facility', {
            facility: f_items, 
            d_facility: d_item
        });
    })

});

//////////////////////////////////////////////CLASSROOM///////////////////////////////////////////
// all classrooms
app.get('/classroom',function (req, res) {

    axios.get('http://127.0.0.1:5000/api/classroom/all')
    .then((response)=>{
        cl_items = response.data;
        console.log(cl_items);
        res.render('pages/classroom',{
            classroom:cl_items
        });
    });
})

// single classroom
app.post('/s_classroom', function (req, res) {
var message = req.body.IdtoSearch;
var initial_api = 'http://127.0.0.1:5000/api/classroom?id='
initial_api = initial_api + message;

axios.get(initial_api)
    .then((response)=>{
        let s_items = response.data;
        console.log(s_items);
        res.render('pages/classroom',{
            classroom:cl_items, 
            s_classroom:s_items
        });
    });
})

// add classroom
app.post('/a_classroom', function (req, res) {
    var message5 = req.body.capatoadd;
    var message2 = req.body.nametoadd;
    var message6 = req.body.factoadd;
    var initial_api = 'http://127.0.0.1:5000/api/classroom'

    axios.post(initial_api, {
        capacity: message5, 
        name:message2, 
        facility:message6
    })
    .then((response) => {
        let a_item = response.data;
        console.log(a_item);
        res.render('pages/classroom', {
            classroom: cl_items, 
            a_classroom: a_item
        });
    })

});

// update classroom
app.post('/u_classroom', function (req, res) {
    var message3 = req.body.idtoupdate;
    var message5 = req.body.capatoupdate;
    var message2 = req.body.nametoupdate;
    var message6 = req.body.factoupdate;
    var initial_api = 'http://127.0.0.1:5000/api/classroom'

    axios.put(initial_api, {
            id:message3, 
            capacity:message5,
            name:message2,
            facility:message6
        
    })
    .then((response) => {
        let updatedItem = response.data;
        console.log(updatedItem);
        res.render('pages/classroom', {
            classroom: cl_items, 
            u_classroom: updatedItem
        });
    })

});

// delete classroom
app.post('/d_classroom', function (req, res) {
    var message5 = req.body.clatodel;
    var initial_api = 'http://127.0.0.1:5000/api/classroom'

    axios.delete(initial_api, {data: {
        id:message5
    }
    })
    .then((response) => {
        let d_item = response.data;
        console.log(d_item);
        res.render('pages/classroom', {
            classroom: cl_items, 
            d_classroom: d_item
        });
    })

});

/////////////////////////////////////////TEACHER////////////////////////////////////////////////
// all teachers
app.get('/teacher',function (req, res) {

    axios.get('http://127.0.0.1:5000/api/teacher/all')
    .then((response)=>{
        t_items = response.data;
        console.log(t_items);
        res.render('pages/teacher',{
            teacher:t_items
        });
    });
})

// single teacher
app.post('/s_teacher', function (req, res) {
var message = req.body.IdtoSearch;
var initial_api = 'http://127.0.0.1:5000/api/teacher?id='
initial_api = initial_api + message;

axios.get(initial_api)
    .then((response)=>{
        let s_items = response.data;
        console.log(s_items);
        res.render('pages/teacher',{
            teacher:t_items, 
            s_teacher:s_items
        });
    });
})

// add teacher
app.post('/a_teacher', function (req, res) {
    var message5 = req.body.fnamtoadd;
    var message2 = req.body.lnamtoadd;
    var message6 = req.body.clrmtoadd;
    var initial_api = 'http://127.0.0.1:5000/api/teacher'

    axios.post(initial_api, {
        firstname: message5, 
        lastname:message2, 
        room:message6
    })
    .then((response) => {
        let a_item = response.data;
        console.log(a_item);
        res.render('pages/teacher', {
            teacher: t_items, 
            a_teacher: a_item
        });
    })

});

// update teacher
app.post('/u_teacher', function (req, res) {
    var message3 = req.body.idtoupdate;
    var message5 = req.body.fnamtoupdate;
    var message2 = req.body.lnamtoupdate;
    var message6 = req.body.clrmtoupdate;
    var initial_api = 'http://127.0.0.1:5000/api/teacher'

    axios.put(initial_api, {
            id:message3, 
            firstname:message5,
            lastname:message2,
            room:message6
        
    })
    .then((response) => {
        let updatedItem = response.data;
        console.log(updatedItem);
        res.render('pages/teacher', {
            teacher: t_items, 
            u_teacher: updatedItem
        });
    })

});

// delete teacher
app.post('/d_teacher', function (req, res) {
    var message5 = req.body.teatodel;
    var initial_api = 'http://127.0.0.1:5000/api/teacher'

    axios.delete(initial_api, {data: {
        id:message5
    }
    })
    .then((response) => {
        let d_item = response.data;
        console.log(d_item);
        res.render('pages/teacher', {
            teacher: t_items, 
            d_teacher: d_item
        });
    })

});

////////////////////////////////////////////CHILD/////////////////////////////////////////////////
// all child
app.get('/child',function (req, res) {

    axios.get('http://127.0.0.1:5000/api/child/all')
    .then((response)=>{
        ch_items = response.data;
        console.log(ch_items);
        res.render('pages/child',{
            child:ch_items
        });
    });
})

// single child
app.post('/s_child', function (req, res) {
var message = req.body.IdtoSearch;
var initial_api = 'http://127.0.0.1:5000/api/child?id='
initial_api = initial_api + message;

axios.get(initial_api)
    .then((response)=>{
        let s_items = response.data;
        console.log(s_items);
        res.render('pages/child',{
            child:ch_items, 
            s_child:s_items
        });
    });
})

// add child
app.post('/a_child', function (req, res) {
    var message5 = req.body.fnamtoadd;
    var message2 = req.body.lnamtoadd;
    var message7 = req.body.chage;
    var message6 = req.body.clrmtoadd;
    var initial_api = 'http://127.0.0.1:5000/api/child'

    axios.post(initial_api, {
        firstname: message5, 
        lastname: message2, 
        age: message7, 
        room: message6
    })
    .then((response) => {
        let a_item = response.data;
        console.log(a_item);
        res.render('pages/child', {
            child: ch_items, 
            a_child: a_item
        });
    })

});

// update child
app.post('/u_child', function (req, res) {
    var message3 = req.body.idtoupdate;
    var message5 = req.body.fnamtoupdate;
    var message2 = req.body.lnamtoupdate;
    var message7 = req.body.chage;
    var message6 = req.body.clrmtoupdate;
    var initial_api = 'http://127.0.0.1:5000/api/child'

    axios.put(initial_api, {
            id:message3, 
            firstname:message5,
            lastname:message2,
            age: message7,
            room:message6
        
    })
    .then((response) => {
        let updatedItem = response.data;
        console.log(updatedItem);
        res.render('pages/child', {
            child: ch_items, 
            u_child: updatedItem
        });
    })

});

// delete child
app.post('/d_child', function (req, res) {
    var message5 = req.body.chitodel;
    var initial_api = 'http://127.0.0.1:5000/api/child'

    axios.delete(initial_api, {data: {
        id:message5
    }
    })
    .then((response) => {
        let d_item = response.data;
        console.log(d_item);
        res.render('pages/child', {
            child: ch_items, 
            d_child: d_item
        });
    })

});



app.listen(port, () => console.log(`MasterEJS app Started on port ${port}!`));