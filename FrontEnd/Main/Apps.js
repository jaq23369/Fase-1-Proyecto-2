const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const authRoutes = require('FrontEnd\Routes\auth.js');
const path = require('path');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true,
}));

app.use('/auth', authRoutes);

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

app.get('/dashboard', (req, res) => {
  if (!req.session.user) {
    return res.redirect('/');
  }
  res.send(`Welcome ${req.session.user.username}`);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
