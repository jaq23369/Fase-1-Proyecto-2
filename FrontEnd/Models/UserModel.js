import { session as _session } from 'FrontEnd\Conf\neo4j.js';
import { hash } from 'bcrypt';

class UserModel {
  static async findByUsername(username) {
    const session = _session();
    try {
      const result = await session.run('MATCH (u:User {username: $username}) RETURN u', { username });
      return result.records[0]?.get('u').properties;
    } finally {
      session.close();
    }
  }

  static async create(username, password) {
    const hashedPassword = await hash(password, 10);
    const session = _session();
    try {
      await session.run('CREATE (u:User {username: $username, password: $password})', {
        username,
        password: hashedPassword,
      });
    } finally {
      session.close();
    }
  }
}

export default UserModel;
