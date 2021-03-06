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

try :
	# create an auth object
	tableau_auth = TSC.TableauAuth(thisCi.username, thisCi.password)
	# create an instance for your server
	server = TSC.Server(thisCi.server)
	# call the sign-in method with the auth object
	server.auth.sign_in(tableau_auth)
	print "Successful authentication to tableau for user [ %s ]" % thisCi.username

except ServerResponseError as e: 
	raise Exception(e.message)

try:
	# query the sites
	all_sites, pagination_item = server.sites.get()
	
	# print all the site names and ids
	for site in all_sites:
		print "Found Site [ %s ] " % site.name
		siteType = Type.valueOf("tableau.Site")
		siteCI = metadataService.findDescriptor(siteType).newInstance("%s/%s" % (thisCi.id, site.name))
		siteCI.contentURL = site.content_url
		siteCI.siteId = site.id
		siteCI.state = site.state
		siteCI = repositoryService.update(siteCI.id, siteCI) if repositoryService.exists(siteCI.id)  else repositoryService.create(siteCI.id, siteCI)
		
		# reauth with this site to pull projects
		server.auth.sign_out()
		tableau_auth = TSC.TableauAuth(thisCi.username, thisCi.password, "" if site.name == "Default" else site.name)
		server.auth.sign_in(tableau_auth)
		all_project_items, pagination_item = server.projects.get()
		for proj in all_project_items:
			print "Found project [ %s ] for Site : %s" % (proj.name, site.name)
			projType = Type.valueOf("tableau.Project")
			projCI = metadataService.findDescriptor(projType).newInstance("%s/%s" % (siteCI.id, proj.name))
			projCI.projectId = proj.id
			projCI = repositoryService.update(projCI.id, projCI) if repositoryService.exists(projCI.id)  else repositoryService.create(projCI.id, projCI)

except ServerResponseError as e: 
	raise Exception(e.message)
