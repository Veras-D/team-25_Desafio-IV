const express = require('express');
const mongoose = require('mongoose');
const usersRouter = require('./users');
const loginRouter = require('./login');

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Conecte-se ao MongoDB (use uma variável de ambiente para a string de conexão)
mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Conectado ao MongoDB'))
  .catch(err => console.error('Erro ao conectar ao MongoDB:', err));

app.use('/api/users', usersRouter);
app.use('/api/login', loginRouter);

// Tratamento de erros
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ message: 'Algo deu errado!' });
});

module.exports = app;