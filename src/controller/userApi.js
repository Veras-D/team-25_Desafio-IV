const router = require('express').Router();
const User = require('../models/User');

router.get('/', (req, res) => {
    res.redirect('/cadastro/tela_cadastro.html');
});

router.post('/users', async (req, res) => {
    const {nome, email, senha} = req.body;

    if (!nome || !email || !senha) {
        res.status(422)
        res.json({message: 'All camps must be filled'})
    };

    const user = {
        nome,
        email,
        senha,
    };
    
    try {
        await User.create(user);
        res.status(201).redirect('/tela_obrigado/obrigado.html');
    } catch (error) {
        res.status(500).json({error: error});
    }
});

module.exports = router;