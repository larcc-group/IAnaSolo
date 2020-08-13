import React, { Component } from 'react'
import { Text, View, Input, Button } from 'react-native-elements'

export default class RegisterReviews extends Component {
  render() {
    return (
      <View>
        <Text> Cadastro de análises de solo </Text>

        <Input placeholder="Nome da análise"></Input>
        <Input placeholder="Data da análise"></Input>
        <Input placeholder="Localização do ponto de coleta"></Input>

        <Text> Componentes químicos </Text>

        <Input placeholder="Potássio"></Input>
        <Input placeholder="Cálcio"></Input>
        <Input placeholder="Fósforo"></Input>
        <Input placeholder="Zinco"></Input>

        <Button title="Salvar análise"></Button>
        <Button title="Salvar e avaliar"></Button>

      </View>
    )
  }
}
