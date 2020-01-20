#
# Copyright 2020 XebiaLabs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import tableauserverclient as TSC
from tableauserverclient.server.endpoint.exceptions import ServerResponseError
from tableauserverclient import ConnectionCredentials, ConnectionItem

try :
	# create an auth object
	tableau_auth = TSC.TableauAuth(deployed.container.site.server.username, deployed.container.site.server.password, "" if deployed.container.site.name == "Default" else deployed.container.site.name)
	# create an instance for your server
	server = TSC.Server(deployed.container.site.server.server)
	# call the sign-in method with the auth object
	server.auth.sign_in(tableau_auth)
	print "Successful authentication to tableau for user [ %s ]" % deployed.container.site.server.username

except ServerResponseError as e: 
	raise Exception(e.message)

try:
	all_project_items, pagination_item = server.projects.get()
	projectId = [proj.id for proj in all_project_items if proj.name == deployed.container.name][0]
	print "Found the Project [ %s ] under site [ %s ]" % ( projectId,deployed.container.site.name )
except ServerResponseError as e: 
	raise Exception(e.message)


try:
	# Creating all connections
	all_connections = list()
	for item in deployed.connections:	
		temp_connection = ConnectionItem()
		temp_connection.server_address = item.serverAddress
		temp_connection.server_port = item.serverPort
		temp_connection.connection_credentials = ConnectionCredentials(item.username, item.password, True)
		all_connections.append(temp_connection)
	
	wb_item = TSC.WorkbookItem(name=deployed.workbookName, project_id=projectId)
	wb_item._connections = all_connections
	# call the publish method with the workbook item
	wb_item = server.workbooks.publish(wb_item, deployed.file.path, deployed.publishMode)
	print "Successfully published workbook [%s] " % deployed.workbookName
except ServerResponseError as e: 
	raise Exception(e.message)

