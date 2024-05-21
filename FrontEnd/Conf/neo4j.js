const neo4j = require('neo4j-driver');

const driver = neo4j.driver('FrontEnd\Vitafit.html', neo4j.auth.basic('your-username', 'your-password'));

module.exports = driver;
