const UserModel = require('FrontEnd\Models\UserModel.js');
const bcrypt = require('bcrypt');

class AuthController {
  static async login(req, res) {
    const { username, password } = req.body;
    const user = await UserModel.findByUsername(username);

    if (user && await bcrypt.compare(password, user.password)) {
      req.session.user = user;
      res.redirect('/dashboard');
    } else {
      res.status(401).send('Invalid credentials');
    }
  }

  static async register(req, res) {
    const { username, password } = req.body;
    await UserModel.create(username, password);
    res.redirect('/');
  }
}

module.exports = AuthController;
