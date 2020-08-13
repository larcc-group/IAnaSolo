/* eslint-disable @typescript-eslint/explicit-member-accessibility */
import express from 'express'
import mongoose from 'mongoose'
import cors from 'cors'
import sys from './config/sys'
import routes from './routes'

class App {
    public express: express.Application

    constructor () {
        this.express = express()
        this.middlewares()
        this.database()
        this.routes()
    }

    private middlewares (): void{
        this.express.use(express.json())
        this.express.use(cors())
    }

    private database (): void{
        mongoose.connect(`${sys.db.HOST}:${sys.db.PORT}/${sys.db.DBNAME}`, {
            useNewUrlParser: true
        })
    }

    private routes (): void {
        this.express.use(routes)
    }
}

export default new App().express
