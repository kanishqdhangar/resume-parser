def normalize(text):
    return (
        text.lower()
        .replace(" ", "")
        .replace("&", "")
        .replace("-", "")
        .replace(".", "")
        .strip()
    )


def attach_links_by_position(parsed_data, links, project_positions):

    projects = parsed_data.get("projects", [])

    # Map normalized title -> (project object, y position)
    pdf_projects = {
        normalize(p["title"]): p["y"]
        for p in project_positions
    }

    # Create mapping for quick lookup
    llm_projects = {
        normalize(p.get("title", "")): p
        for p in projects
    }

    print("PDF Titles:", pdf_projects.keys())
    print("LLM Titles:", llm_projects.keys())

    # 🔥 KEY FIX: strict Y-alignment instead of closest-above logic
    for link in links:
        url = link["url"]
        link_y = link["y"]

        if not url.lower().startswith("http"):
            continue

        for pdf_title_norm, pdf_y in pdf_projects.items():

            # Only match if Y distance is small (same line)
            if abs(link_y - pdf_y) < 15:  # adjust threshold if needed

                # Find matching LLM project
                for llm_title_norm, project in llm_projects.items():
                    if (
                        llm_title_norm in pdf_title_norm
                        or pdf_title_norm in llm_title_norm
                    ):

                        if "github.com" in url.lower():
                            project["github_url"] = url
                        else:
                            project["live_url"] = url

    return parsed_data