// copy the commands bellow and paste them in mongosh
// to create the admin user and worklog user
use admin
db.createUser(
  {
    user: "nsc",
    pwd: passwordPrompt(), // or cleartext password
    roles: [
      { role: "userAdminAnyDatabase", db: "admin" },
      { role: "readWriteAnyDatabase", db: "admin" }
    ]
  }
)

use worklog
db.createUser(
  {
    user: "worklog",
    pwd: passwordPrompt(), // or cleartext password
    roles: [
      { role: "readWrite", db: "worklog" }
    ]
  }
)
