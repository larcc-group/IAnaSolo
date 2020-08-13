import { PythonShell } from 'python-shell'

class PythonImageAnalyze {
    public analyze (script, args): Promise<object> {
        return new Promise(function (resolve, reject) {
            PythonShell.run(script, args, function (err, data) {
                if (err) reject(err)
                resolve(data)
            })
        })
    }
}

export default new PythonImageAnalyze()
