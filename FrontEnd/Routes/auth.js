const express = require('express');
const router = express.Router();
const AuthController = require('FrontEnd\Controllers\UserControler.js');

router.post('/login', AuthController.login);
router.post('/register', AuthController.register);

module.exports = router;
