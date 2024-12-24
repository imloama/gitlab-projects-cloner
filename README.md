# GitLab Projects Cloner

## Overview

This Python script allows you to clone all projects within a GitLab group, including projects in nested subgroups, to a specified local path. It utilizes the GitLab API to fetch project information and GitPython library for cloning repositories.

## Features

- Recursively fetch projects from a specified GitLab group, including subgroups.
- Clone each project's repository to a local directory.
- Handle GitLab API authentication using a personal access token.

## Requirements

- Python 3.x
- GitPython library (`gitpython`), which can be installed via pip:
  ```
  pip install gitpython
  ```

## Usage

1. **Clone the Repository**

   Clone this repository to your local machine:
   ```
   git clone https://github.com/your-username/gitlab-projects-cloner.git
   cd gitlab-projects-cloner
   ```

2. **Configure GitLab API Token**

   Replace `YOUR_GITLAB_API_TOKEN` in `gitlab_projects_cloner.py` with your GitLab personal access token. Ensure the token has sufficient permissions to read group and project information.

3. **Run the Script**

   Modify `gitlab_projects_cloner.py` to specify the GitLab base URL (`gitlab_base_url`) and the group ID or URL-encoded path (`group_id`) of the group you want to clone. Also, specify the local path (`group_clone_path`) where projects should be cloned.

   ```python
   if __name__ == "__main__":
       gitlab_base_url = 'https://gitlab.com/api/v4'
       gitlab_token = 'YOUR_GITLAB_API_TOKEN'

       gitlab = GitLabAPI(gitlab_base_url, gitlab_token)

       clone_path = '/path/to/clone'

       for item in groups:
          group_id = item["id"]
          web_url = item["web_url"]
          name = item["name"]
          group_clone_path = os.path.join(clone_path, name)
            if not os.path.exists(group_clone_path):
               os.mkdir(group_clone_path)
            gitlab.clone_group_projects(group_id, group_clone_path)
   ```

   **Explanation**:
   - `gitlab_base_url`: Specifies the base URL of your GitLab instance's API.
   - `gitlab_token`: Your GitLab API token for authentication.
   - `clone_path`: Local directory path where projects will be cloned.

4. **Execute the Script**

   Run the script to clone projects from the specified GitLab group:
   ```
   python gitlab_projects_cloner.py
   ```

   The script will clone each project into the `group_clone_path` directory on your local machine.

## Notes

- Make sure your GitLab API token (`gitlab_token`) has the necessary permissions to read group and project information.
- Adjust the GitLab base URL (`gitlab_base_url`) according to your GitLab instance's API version and configuration.
- Fetch projects of group contains pagination. set `per_page` is `100`, and max page is `99`. If you have many many projects in a group, you should modify the function in `line 114`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
