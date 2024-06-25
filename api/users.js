const express = require('express');
const router = express.Router();
const User = require('../models/User');
const bcrypt = require('bcrypt');

router.post('/', async (req, res) => {
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

module.exports = router;
