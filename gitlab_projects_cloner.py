import os
import git
import requests

class GitLabAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url.strip('/')  # Ensure base_url does not end with '/'
        self.headers = {'PRIVATE-TOKEN': token}

    def _get_projects_in_group(self, group_id):
        """
        Recursively fetch all projects within a group, including projects in nested subgroups.

        Args:
        - group_id (str or int): The ID or URL-encoded path of the group.

        Returns:
        - list: A list of dictionaries, each containing information about a project.
        """
        projects = []

        def fetch_projects(url):
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

        def process_group(group_info):
            for project in group_info['projects']:
                projects.append(project)

            for subgroup in group_info.get('subgroups', []):
                subgroup_projects = fetch_projects(f"{self.base_url}/groups/{subgroup['id']}/projects")
                process_group(subgroup_projects)

        group_info = fetch_projects(f"{self.base_url}/groups/{group_id}/projects")
        process_group(group_info)

        return projects

    def clone_group_projects(self, group_id, path_to_clone):
        """
        Clone all projects within a GitLab group, including projects in nested subgroups,
        to a specified local path.

        Args:
        - group_id (str or int): The ID or URL-encoded path of the group.
        - path_to_clone (str): Local directory where projects should be cloned.

        Raises:
        - requests.HTTPError: If the request to GitLab fails.
        - git.exc.GitCommandError: If Git command fails during cloning.

        Returns:
        - None
        """
        try:
            projects = self._get_projects_in_group(group_id)

            for project in projects:
                project_name = project['name']
                project_id = project['id']
                clone_url = project['ssh_url_to_repo']
                project_path = os.path.join(path_to_clone, project_name)

                git.Repo.clone_from(clone_url, project_path)
                print(f"Successfully cloned project '{project_name}' to '{project_path}'.")

        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve group information: {e}")

        except git.exc.GitCommandError as e:
            print(f"Failed to clone repository: {e}")


# Example usage:
if __name__ == "__main__":
    # Replace with your GitLab base URL and API token
    gitlab_base_url = 'https://gitlab.com/api/v4'
    gitlab_token = 'YOUR_GITLAB_API_TOKEN'

    gitlab = GitLabAPI(gitlab_base_url, gitlab_token)

    # Example: Clone all projects in a group (including nested subgroups)
    group_id = 'group-name'  # Replace with your group ID or URL-encoded path
    group_clone_path = '/path/to/group/clone'

    gitlab.clone_group_projects(group_id, group_clone_path)
