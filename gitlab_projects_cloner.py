import requests
import os
import git

class GitLabAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip('/')  # Ensure base_url does not end with '/'
        self.headers = {'PRIVATE-TOKEN': token}

    def fetch_group_info(self, group_id):
        """
        Fetch details of a GitLab group.

        Args:
        - group_id (str or int): The ID or URL-encoded path of the group.

        Returns:
        - dict: Dictionary containing group information.
        """
        try:
            url = f"{self.base_url}/groups/{group_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch group information for group ID {group_id}: {e}")
            return {}

    def fetch_subgroups(self, group_id):
        """
        Fetch subgroups of a GitLab group.

        Args:
        - group_id (str or int): The ID or URL-encoded path of the group.

        Returns:
        - list: List of dictionaries, each containing subgroup information.
        """
        try:
            url = f"{self.base_url}/groups/{group_id}/subgroups"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch subgroups for group ID {group_id}: {e}")
            return []

    def fetch_all_group_ids(self, group_id):
        """
        Recursively fetch all group IDs within a specified group, including subgroups.

        Args:
        - group_id (str or int): The ID or URL-encoded path of the group.

        Returns:
        - list: List of integers representing group IDs.
        """
        group_ids = []

        def process_group(group_info):
            group_ids.append(group_info['id'])

            subgroups = self.fetch_subgroups(group_info['id'])
            for subgroup in subgroups:
                subgroup_info = self.fetch_group_info(subgroup['id'])
                if subgroup_info:
                    process_group(subgroup_info)

        try:
            main_group_info = self.fetch_group_info(group_id)
            if main_group_info:
                process_group(main_group_info)
        except Exception as e:
            print(f"Failed to retrieve groups information: {e}")

        return group_ids

    def fetch_projects_in_group(self, group_id):
        """
        Fetch all projects within a group, including projects in subgroups.

        Args:
        - group_id (str or int): The ID or URL-encoded path of the group.

        Returns:
        - list: A list of dictionaries, each containing information about a project.
        """
        projects = []

        def fetch_projects(url):
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch projects from {url}: {e}")
                return []

        def process_group_projects(group_id):
            try:
                url = f"{self.base_url}/groups/{group_id}/projects"
                group_projects = fetch_projects(url)
                if group_projects:
                    projects.extend(group_projects)

                subgroups = self.fetch_subgroups(group_id)
                for subgroup in subgroups:
                    subgroup_projects = fetch_projects(f"{self.base_url}/groups/{subgroup['id']}/projects")
                    if subgroup_projects:
                        projects.extend(subgroup_projects)
            except Exception as e:
                print(f"Error processing group {group_id}: {e}")

        try:
            # Fetch projects for the main group and its subgroups
            process_group_projects(group_id)

        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve projects: {e}")

        return projects

    def clone_group_projects(self, group_id, path_to_clone):
        """
        Clone all projects within a GitLab group to a specified local path.

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
            projects = self.fetch_projects_in_group(group_id)

            if not projects:
                print(f"No projects found in group {group_id}.")
                return

            for project in projects:
                project_name = project.get('name', 'Unnamed Project')
                project_id = project.get('id', 'Unknown ID')
                clone_url = project.get('ssh_url_to_repo')
                if not clone_url:
                    print(f"Project '{project_name}' has no SSH URL to repo.")
                    continue

                project_path = os.path.join(path_to_clone, project_name)

                try:
                    git.Repo.clone_from(clone_url, project_path)
                    print(f"Successfully cloned project '{project_name}' to '{project_path}'.")
                except git.exc.GitCommandError as e:
                    print(f"Failed to clone project '{project_name}': {e}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve group information: {e}")

        except Exception as e:
            print(f"An error occurred during cloning: {e}")

# Example usage:
if __name__ == "__main__":
    gitlab_base_url = 'https://gitlab.com/api/v4'
    gitlab_token = 'YOUR_GITLAB_API_TOKEN'

    gitlab = GitLabAPI(gitlab_base_url, gitlab_token)

    group_id = 'group-name'  # Replace with your group ID or URL-encoded path
    group_ids = gitlab.fetch_all_group_ids(group_id)

    print(f"All group IDs within group '{group_id}': {group_ids}")

    group_clone_path = '/path/to/group/clone'
    gitlab.clone_group_projects(group_id, group_clone_path)
