import { Router } from 'express'
import UserController from './controllers/UserController'
import ReportsController from './controllers/ReportsController'

const routes = Router()

routes.get('/users', UserController.index)
routes.post('/users', UserController.store)
routes.post('/reports/analyze', ReportsController.store)

export default routes
