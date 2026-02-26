def attach_links_to_projects(parsed_data, links):
    github_links = []
    demo_links = []

    for link in links:
        link_lower = link.lower()

        if "github.com" in link_lower:
            github_links.append(link)
        else:
            demo_links.append(link)

    for i, project in enumerate(parsed_data.get("projects", [])):
        if i < len(github_links):
            project["github_url"] = github_links[i]

        if i < len(demo_links):
            project["live_url"] = demo_links[i]

    return parsed_data