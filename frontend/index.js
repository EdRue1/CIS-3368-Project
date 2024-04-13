const express = require('express')
var path = require('path');
var bodyParser = require('body-parser');
const app = express();
const port = 3000;
var idSearch = 0;
var items = null

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

app.get('/',function (req, res) {
    res.render('pages/login')
});
app.get('/home',function (req, res) {
    res.render('pages/home')
});

app.post('/process_login', function(req, res){
    var user = req.body.username;
    var password = req.body.password;
    // This sample is showing how to validate user input with static username and password
    // If you want to validate database user data then you need to call REST API for it to get user data
    // Then validate user input with user data retrived from database.
    if(user === 'admin' && password === 'password')
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
  })

app.get('/facility',function (req, res) {
  
        axios.get('http://127.0.0.1:5000/api/facility/all')
        .then((response)=>{
            items = response.data;
            console.log(items);
            res.render('pages/facility',{
                facility:items
            });
        });

        

        

    
})

app.post('/s_facility', function (req, res) {
    var message = req.body.IdtoSearch;
    var initial_api = 'http://127.0.0.1:5000/api/facility?id='
    initial_api = initial_api + message;

    axios.get(initial_api)
        .then((response)=>{
            let s_items = response.data;
            console.log(s_items);
            res.render('pages/facility',{
                facility:items, 
                s_facility:s_items
            });
        });



})




app.get('/list',function (req, res) {
    //array with items to send
    var items = ['node.js','expressjs','ejs','javascript','bootstarp'];
    res.render('pages/list',{
        list:items
    })
});

app.get('/table',function (req, res) {
    //array with items to send
    var items = [
        {name:'node.js',url:'https://nodejs.org/en/'},
        {name:'ejs',url:'https://ejs.co'},
        {name:'expressjs',url:'https://expressjs.com'},
        {name:'vuejs',url:'https://vuejs.org'},
        {name:'nextjs',url:'https://nextjs.org'}];

    res.render('pages/table',{
        table:items
    })
});

//our alert message midleware
function messages(req,res,next){
    var message;
    res.locals.message = message;
    next();
}

app.get('/form',messages,function (req, res) {
    res.render('pages/form');
});

app.post('/form',function (req, res) {
    var message=req.body;
    res.locals.message = message;
    res.render('pages/form');
});

app.listen(port, () => console.log(`MasterEJS app Started on port ${port}!`));