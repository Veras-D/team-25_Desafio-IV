const express = require('express');
const bodyParser = require("body-parser");
const mongoose = require('mongoose');
const path = require('path');
const port = process.env.PORT || 3000;

const app = express();
app.use(express.static('public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended:true
}));

const url_db = "mongodb://127.0.0.1:27017/trilhas_inova";
mongoose.set('strictQuery', true);
mongoose.connect(url_db)
        .then(() => {
          console.log('Connected to DB');
        })
        .catch(error => {
          console.error('Connection to DB Failed');
          console.error(error.message);
          process.exit(-1);
        });

app.listen(port, () => {
    console.log('SERVER IS UP');
});

app.use('/', require('./controller/userApi'));