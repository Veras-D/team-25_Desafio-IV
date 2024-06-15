const mongoose = require('mongoose');
const moongoseSequence = require('mongoose-sequence');

const userSchema = new mongoose.Schema({
    nome: {type: String, required: true},
    email: {type: String, unique: true, required: true},
    senha: {type: String, required: true},
})

userSchema.plugin(moongoseSequence(mongoose), {inc_field: 'account_id'})

const User = mongoose.model('User', userSchema)

module.exports = User;