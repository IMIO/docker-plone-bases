from Products.CMFPlone.Portal import PloneSite
# get users count, only keep users that are in a group
def main(app):
    for child in app.listDAVObjects():
        if child.id != 'standard' and isinstance(child, PloneSite):
            users = child.portal_membership.searchForMembers()  # ok with wca
            count = 0
            for user in users:
                user_groups = user.getGroups()
                if user_groups and user_groups != ['AuthenticatedUsers']:
                    count = count + 1
    with open("nb_users.txt", "w") as file:
        file.write(str(count))

if "app" in locals():
    main(app)

