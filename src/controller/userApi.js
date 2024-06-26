const express = require('express');
const router = express.Router();
const User = require('./src/models/User');
const bcrypt = require('bcrypt');

router.post('/', async (req, res) => {
    try {
        const { nome, email, senha, confirmar_senha } = req.body;

        if (!nome || !email || !senha || !confirmar_senha) {
            return res.status(422).json({ message: 'Todos os campos devem ser preenchidos' });
        }

        if (senha !== confirmar_senha) {
            return res.status(422).json({ message: 'As senhas não coincidem' });
        }

        const hashedPassword = await bcrypt.hash(senha, 10);

        const user = new User({ nome, email, senha: hashedPassword });
        await user.save();

        res.status(201).json({ 
            message: 'Usuário criado com sucesso', 
            redirectUrl: '/Page/tela_obrigado/obrigado.html'
        });
    } catch (error) {
        console.error('Erro ao criar usuário:', error);
        res.status(500).json({ message: 'Erro interno do servidor' });
    }
});

module.exports = router;