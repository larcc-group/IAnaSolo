import { Request, Response } from 'express'
import { Report } from '../schemas/Report'
import PythonImageAnalyze from '../process/PythonImageAnalyze'
import fs from 'fs'
import path from 'path'

class ReportsController {
    public async store (req: Request, res: Response): Promise<Response> {
        let options = {
            mode: 'text',
            scriptPath: '/home/alisson-ap/Projetos/TCC/tcc-si-ad/ProcessamentoDeImagens/',
            args: [ '/home/alisson-ap/Projetos/TCC/tcc-si-ad/ProcessamentoDeImagens/',
                'images/AnaliseSoloNova.jpeg'
            ]
        }
        PythonImageAnalyze.analyze('mainAPI.py', options).then(rs => {
            let reqPath = path.join(__dirname, '../')
            fs.readFile(reqPath + '/result.json', 'utf8', function (err, data) {
                if (err) throw err
                res.json(JSON.parse(data))
            })
        })
    }
}

export default new ReportsController()
