import app from './app'
import sys from './config/sys'

app.listen(sys.server.PORT, sys.server.HOST, (): void => {
    console.log('Server listen on', sys.server.HOST, sys.server.PORT)
})
