PROJECTNAME = 'intranett.policy'
ADD_PERMISSIONS = {'MembersFolder': '%s: Add MembersFolder' % PROJECTNAME,
                   'ProjectRoom': '%s: Add ProjectRoom' % PROJECTNAME,}
MEMBERS_FOLDER_ID = 'users'
PERSONAL_FOLDER_ID = 'personal'

from plutonian import Configurator

config = Configurator('intranett.policy')
