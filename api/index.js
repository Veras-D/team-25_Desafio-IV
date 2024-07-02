const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const path = require("path");
const port = process.env.PORT || 3000;
const User = require("./models/User");
const bcrypt = require("bcrypt");

const app = express();
app.use(express.static("Page"));
app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);

const url_db = "mongodb+srv://pgsilva2002:_trilhas_inova_desafio_25@cluster0.nsscd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

mongoose.set("strictQuery", true);
mongoose
  .connect(url_db)
  .then(() => {
    console.log("Connected to DB");
  })
  .catch((error) => {
    console.error("Connection to DB Failed");
    console.error(error.message);
    process.exit(-1);
  });

app.listen(port, () => {
  console.log("SERVER IS UP");
});

app.get('/', (req,res) => {
  res.redirect('index.html')
});

app.post("/users", async (req, res) => {
  const { nome, email, senha, confirmar_senha } = req.body;

  if (!nome || !email || !senha || !confirmar_senha) {
    return res
      .status(422)
      .json({ message: "Todos os campos devem ser preenchidos" });
  }

  if (senha !== confirmar_senha) {
    return res.status(422).json({ message: "As senhas não coincidem" });
  }

  const hashedPassword = await bcrypt.hash(senha, 10);

  const user = { nome, email, senha: hashedPassword };

  try {
    await User.create(user);
    res.status(201).redirect("/tela_obrigado/obrigado.html");
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Rota de login
app.post("/login", async (req, res) => {
  const { email, senha } = req.body;

  if (!email || !senha) {
    return res.status(422).json({ message: "E-mail e senha são obrigatórios" });
  }

  try {
    const user = await User.findOne({ email });

    if (!user) {
      return res.status(404).json({ message: "Usuário não encontrado" });
    }

    const isPasswordValid = await bcrypt.compare(senha, user.senha);

    if (!isPasswordValid) {
      return res.status(401).json({ message: "Senha incorreta" });
    }

    res.status(200).redirect("/home/home.html");
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = app;