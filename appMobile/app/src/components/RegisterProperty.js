import React, { Component } from 'react'
import { Text, View } from 'react-native'
import { Input, Button } from 'react-native-elements';

export default class RegisterProperty extends Component {
  render() {
    return (
      <View>
        <Text> Cadastro de nova propriedade </Text>
        
        <Input placeholder="Nome da propriedade"></Input>
        <Input placeholder="Localização"></Input>
        
        <Text>Culturas</Text>
        <CheckBox
            title='Soja'
            checked={this.state.sojaChecked}
            />
              <CheckBox
            title='Milho'
            checked={this.state.milhoChecked}
            />
        <Button title="Cadastrar"></Button>
      </View>
    )
  }
}
