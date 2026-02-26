# import re

# def normalize(text):
#     return re.sub(r'[^a-z0-9]', '', text.lower())

# def attach_links_by_position(parsed_data, links, lines):

#     projects = parsed_data.get("projects", [])
#     if not projects or not lines:
#         return parsed_data

#     # Step 1: Build anchor positions using LLM project titles
#     anchors = []

#     for project in projects:
#         title = project.get("title", "")
#         title_tokens = title.lower().split()

#         for line in lines:
#             line_text = line["text"].lower()

#             # Match if all title words exist in the line
#             if all(token in line_text for token in title_tokens):
#                 anchors.append({
#                     "project": project,
#                     "y_top": line["y_top"],
#                     "y_bottom": line["y_bottom"]
#                 })
#                 break

#     if not anchors:
#         return parsed_data

#     # Step 2: Sort anchors vertically
#     anchors = sorted(anchors, key=lambda x: x["y_top"])

#     # Step 3: Build vertical sections
#     for i in range(len(anchors)):
#         if i < len(anchors) - 1:
#             anchors[i]["section_bottom"] = anchors[i + 1]["y_top"]
#         else:
#             anchors[i]["section_bottom"] = float("inf")

#     # Step 4: Assign links inside each section
#     for link in links:
#         url = link["url"]
#         link_y = link["y"]

#         if not url.lower().startswith("http"):
#             continue

#         for anchor in anchors:
#             if anchor["y_top"] <= link_y <= anchor["section_bottom"]:
#                 project = anchor["project"]

#                 if "github.com" in url.lower():
#                     project["github_url"] = url
#                 else:
#                     project["live_url"] = url

#                 break

#     return parsed_data