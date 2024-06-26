const express = require('express');
const router = express.Router();
const User = require('../models/User');
const bcrypt = require('bcrypt');

// Rota de cadastro
router.post('/users', async (req, res) => {
    const { nome, email, senha, confirmar_senha } = req.body;

    if (!nome || !email || !senha || !confirmar_senha) {
        return res.status(422).json({ message: 'Todos os campos devem ser preenchidos' });
    }

    if (senha !== confirmar_senha) {
        return res.status(422).json({ message: 'As senhas não coincidem' });
    }

    try {
        // Verifica se o e-mail já está em uso
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(409).json({ message: 'Este e-mail já está em uso' });
        }

        const hashedPassword = await bcrypt.hash(senha, 10);
        const user = new User({ nome, email, senha: hashedPassword });

        await user.save();
        res.status(201).json({ message: 'Usuário criado com sucesso', redirectTo: '/Page/tela_obrigado/obrigado.html' });
    } catch (error) {
        res.status(500).json({ error: 'Erro ao criar usuário', details: error.message });
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

        // Aqui você poderia gerar e enviar um token JWT
        res.status(200).json({ message: 'Login bem-sucedido', redirectTo: '/Page/home/home.html' });
    } catch (error) {
        res.status(500).json({ error: 'Erro ao fazer login', details: error.message });
    }
});

module.exports = router;