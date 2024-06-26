const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const path = require('path');
const port = process.env.PORT || 3000;

const app = express();
app.use(express.static(path.join(__dirname, '..', 'Page')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const url_db = "mongodb+srv://pgsilva2002:_trilhas_inova_desafio_25@cluster0.nsscd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
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

const userApi = require('./controller/userApi');
app.use('/api', userApi);

app.listen(port, () => {
  console.log(`SERVER IS UP on port ${port}`);
});
