import React, { Component } from 'react'
import { Text, View, Input, Button } from 'react-native-elements'

export default class ResetPassword extends Component {
  render() {
    return (
      <View>
        <Text> Recuperação de senha </Text>
        <Input placeholder="Endereço de e-mail"></Input>
        <Button title="Recuperar a senha"></Button>
      </View>
    )
  }
}
