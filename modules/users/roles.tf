#
# Description:  
# Maps a user (e.g. Sheldon Cooper) to the agent and user role.  In org, this allows you to login and then also go on queue for assigned queues.
# 
# Since the roles exist and are not being managed by Terraform, I lookup the roles into data sources so that I can use them below. 
# 
data "genesyscloud_auth_role" "employee" {
  name = "employee"
}

data "genesyscloud_auth_role" "user" {
  name = "User"
}

#Assigning Ricky Bobby the agents and user
resource "genesyscloud_user_roles" "sheldoncooper_roles" {
  user_id = genesyscloud_user.sheldoncooper_agent.id
  roles {
    role_id = data.genesyscloud_auth_role.employee.id
  }

  roles {
    role_id = data.genesyscloud_auth_role.user.id
  }
}
