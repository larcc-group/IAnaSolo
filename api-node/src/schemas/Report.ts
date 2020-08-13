import { Schema, model } from 'mongoose'

const reportSchema = new Schema({
    Nome: String,
    Localidade: String,
    Municipio: String,
    DataRecebimento: Date,
    DataExpedicao: String,
    primeiraTabela: Array,
    segundaTabela: Array
})

export default model('Report', reportSchema)
