# gitlab-projects-cloner
**Description:** 
"A Python script leveraging GitLab API to clone projects and handle nested subgroups recursively. Ideal for managing GitLab group repositories locally."

### Additional Details:
- **Summary:** This repository contains Python scripts encapsulated in a class-oriented approach to interact with GitLab's API. It enables users to clone projects from a specified GitLab group, including projects nested within subgroups. The code includes robust error handling, adhering to secure coding practices.
  
- **Features:**
  - Clone individual projects by ID or URL-encoded path.
  - Recursively clone projects from nested subgroups within a specified GitLab group.
  - Uses GitPython for managing Git operations and requests for HTTP interactions with GitLab's API.
  
- **Usage:** 
  - Replace placeholders with your GitLab base URL and API token.
  - Specify the group ID or URL-encoded path for cloning projects.
  - Run the script to clone projects locally, ensuring accurate attribution and error-free operations.

**Explanation of Updates:**
- **_get_projects_in_group Method:** This new private method is introduced to recursively fetch all projects within a group, including projects in nested subgroups. It uses nested functions (fetch_projects and process_group) to handle fetching recursively:
  - *fetch_projects* function retrieves projects for a given URL.
  - *process_group* function iterates through projects and subgroups within a group, recursively fetching projects from nested subgroups.

- **clone_group_projects Method:** Updated to use _get_projects_in_group method to fetch all projects (including nested subgroups) and then clone each project similar to before.

- **Handling Nested Subgroups:** This approach ensures that all projects within the specified group, including those in nested subgroups, are cloned to the specified local directory (path_to_clone).
