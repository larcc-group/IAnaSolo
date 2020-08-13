import React, { Component } from 'react'
import { Text, View } from 'react-native'
import { Input, Divider, Button } from 'react-native-elements'
import Icon from 'react-native-vector-icons/FontAwesome';

export default class Login extends Component {
  render() {
    return (
      <View>
        <Text h2>Leiva Nela</Text>
        <Input
          placeholder='Nome do usuário'
          leftIcon={
            <Icon
              name='user'
              size={24}
              color='black'
            />
          }
        />
        <Input
          placeholder='Senha'
          leftIcon={
            <Icon
              name='password'
              size={24}
              color='black'
            />
          }
        />
        <Divider style={{ backgroundColor: 'blue' }} />
        <Button
          icon={{
            name: 'arrow-right',
            size: 15,
            color: 'white'
          }}
          title='Login'
        />
        <Button
          icon={{
            name: 'arrow-right',
            size: 15,
            color: 'white'
          }}
          title='Esqueceu sua senha?'
        />
        <Button
          icon={{
            name: 'arrow-right',
            size: 15,
            color: 'white'
          }}
          title='Cadastre-se'
        />

       <Button
          icon={{
            name: 'arrow-right',
            size: 15,
            color: 'white'
          }}
          title='Abrir câmera'
        />

      </View>
    )
  }
}
