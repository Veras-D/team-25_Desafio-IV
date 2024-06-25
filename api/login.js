const express = require('express');
const router = express.Router();
const User = require('../src/models/User');
const bcrypt = require('bcrypt');

router.post('/', async (req, res) => {
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
