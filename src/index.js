const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const userApi = require('./controller/userApi');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.static(path.join(__dirname, '..', 'Page')));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Conexão com o MongoDB
const url_db = process.env.MONGODB_URI || "mongodb+srv://pgsilva2002:_trilhas_inova_desafio_25@cluster0.nsscd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
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

// Rotas da API
app.use('/api', userApi);

// Rota catch-all para SPA (se aplicável)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'index.html'));
});

// Tratamento de erros
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

// Iniciar o servidor apenas se não estiver em produção
if (process.env.NODE_ENV !== 'production') {
  app.listen(port, () => {
    console.log(`SERVER IS UP on port ${port}`);
  });
}

module.exports = app;