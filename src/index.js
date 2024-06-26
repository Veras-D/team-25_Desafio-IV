const express = require('express');
const bodyParser = require("body-parser");
const mongoose = require('mongoose');
const path = require('path');
const port = process.env.PORT || 3000;

const app = express();

// Configurando o Express para servir arquivos estáticos da pasta "Page"
app.use(express.static(path.join(__dirname, 'Page')));

// Configurando o Body-Parser para lidar com dados JSON e codificados em URL
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Configurando o MongoDB
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

// Importando e utilizando as rotas de API
app.use('/api/users', require('../api/users'));
app.use('/api/login', require('../api/login'));

// Iniciando o servidor
app.listen(port, () => {
    console.log('SERVER IS UP');
});
