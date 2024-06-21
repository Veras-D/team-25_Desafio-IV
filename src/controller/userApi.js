const express = require('express');
const router = express.Router();
const User = require('../models/User');
const bcrypt = require('bcrypt'); // Para verificar a senha hash

// Rota de cadastro
router.post('/users', async (req, res) => {
    const { nome, email, senha, confirmar_senha } = req.body;

    if (!nome || !email || !senha || !confirmar_senha) {
        return res.status(422).json({ message: 'Todos os campos devem ser preenchidos' });
    }

    if (senha !== confirmar_senha) {
        return res.status(422).json({ message: 'As senhas não coincidem' });
    }

    const hashedPassword = await bcrypt.hash(senha, 10);

    const user = { nome, email, senha: hashedPassword };

    try {
        await User.create(user);
        res.status(201).redirect('/Page/tela_obrigado/obrigado.html');
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Rota de login
router.post('/login', async (req, res) => {
    const { email, senha } = req.body;

    if (!email || !senha) {
        return res.status(422).json({ message: 'E-mail e senha são obrigatórios' });
    }

    try {
        const user = await User.findOne({ email });

        if (!user) {
            return res.status(404).json({ message: 'Usuário não encontrado' });
        }

        const isPasswordValid = await bcrypt.compare(senha, user.senha);

        if (!isPasswordValid) {
            return res.status(401).json({ message: 'Senha incorreta' });
        }

        res.status(200).redirect('/Page/home/home.html');
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
