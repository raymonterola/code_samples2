def list_organizations(access_token, page_size=50, page=1):
	"""Retrieve list of organizations the Github user belongs to.

	Args:
		access_token (str): OAuth token.
		page_size (int, optional): Page size per request, defaults to 50.
		page (int, optional): Page to retrieve, defaults to 1.

	Returns:
		List of organizations.

	Raises:
		Exception: If request fails or error occurs.

	"""
	exception = Exception("Error retrieving Github organizations.")
	try:
		response = requests.get("https://api.github.com/user/orgs", timeout=10, headers={"Accept":"vnd.github.v3+json","Authorization":"token "+str(access_token)},
																	params={"page":page, "per_page":page_size})
		orgs_json = response.json()
		if response.status_code != 200:
			raise Exception("Error listing organizations: "+str(orgs_json["message"]))
		orgs = []
		for org in orgs_json:
			orgs.append({"id":org["login"], "name":org["login"]})

		if len(orgs) == page_size:
			next_orgs = list_organizations(access_token, page_size, page+1)
			orgs = orgs + next_orgs
		return orgs
	except requests.exceptions.Timeout as e:
		logger.error(f"Request timed out. {e}")
		raise exception
	except requests.exceptions.TooManyRedirects as e:
		logger.error(f"Too many redirects. {e}")
		raise exception
	except requests.exceptions.RequestException as e:
		logger.error(f"Request error occurred. {e}")
		raise exception
	except Exception as e:
		logger.error("Error listing Github organizations: " + str(e))
		raise Exception(e)


def list_user_repos(access_token, page_size=50, page=1):
	"""Retrieve user's Github repositories.

	Args:
		access_token (str): OAuth token.
		page_size (int, optional): Page size per request, defaults to 50.
		page (int, optional): Page to retrieve, defaults to 1.

	Returns:
		List of repositories.

	Raises:
		Exception: If request fails or error occurs.

	"""
	exception = Exception("Error retrieving Github repositories for user.")
	try:
		response = requests.get("https://api.github.com/user/repos", timeout=10, headers={"Accept":"vnd.github.v3+json","Authorization":"token "+str(access_token)},
																	params={"page":page, "sort":"full_name","per_page":page_size, "type":"all"})
		repos_json = response.json()
		if response.status_code != 200:
			raise Exception("Error listing repositories: "+str(repos_json["message"]))
		repos = []
		for repo in repos_json:
			repos.append({"id":repo["name"], "name":repo["name"]})

		if len(repos) == page_size:
			next_repos = list_user_repos(access_token, page_size, page+1)
			repos = repos + next_repos
		return repos
	except requests.exceptions.Timeout as e:
		logger.error(f"Request timed out. {e}")
		raise exception
	except requests.exceptions.TooManyRedirects as e:
		logger.error(f"Too many redirects. {e}")
		raise exception
	except requests.exceptions.RequestException as e:
		logger.error(f"Request error occurred. {e}")
		raise exception
	except Exception as e:
		logger.error("Error listing Github Repositories: " + str(e))
		raise Exception(e)


def list_org_repos(access_token, org_id, page_size=50, page=1):
	"""Retrieve list of repositories in an organization.

	Args:
		access_token (str): OAuth token.
		org_id (str): Organization ID.
		page_size (int, optional): Page size per request, defaults to 50.
		page (int, optional): Page to retrieve, defaults to 1.

	Returns:
		List of repositories.

	Raises:
		Exception: If request fails or error occurs.

	"""
	exception = Exception("Error retrieving Github repositories for org.")
	try:
		response = requests.get("https://api.github.com/orgs/"+str(org_id)+"/repos", timeout=10, headers={"Accept":"vnd.github.v3+json","Authorization":"token "+str(access_token)},
																	params={"page":page, "sort":"full_name", "per_page":page_size, "type":"all"})
		repos_json = response.json()
		if response.status_code != 200:
			raise Exception("Error listing repositories: "+str(repos_json["message"]))
		repos = []
		for repo in repos_json:
			repos.append({"id":repo["name"], "name":repo["name"]})

		if len(repos) == page_size:
			next_repos = list_org_repos(access_token, org_id, page_size, page+1)
			repos = repos + next_repos
		return repos
	except requests.exceptions.Timeout as e:
		logger.error(f"Request timed out. {e}")
		raise exception
	except requests.exceptions.TooManyRedirects as e:
		logger.error(f"Too many redirects. {e}")
		raise exception
	except requests.exceptions.RequestException as e:
		logger.error(f"Request error occurred. {e}")
		raise exception
	except Exception as e:
		logger.error("Error listing Github Organization Repositories: " + str(e))
		raise Exception(e)