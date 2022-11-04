class NotFound(Exception):
    ...


class Satisfied(Exception):
    ...


class Account:
    __slots__ = ("username", "password", "email")

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email


class Repository:
    __slots__ = ("account", "project", "files")

    def __init__(self, account: Account, project=None):
        self.account = account
        self.project = project
        self.files = project.files if project is not None else None

    def connect_project(self, project):
        if self.project is None:
            self.project = project
            return self
        raise Satisfied("A project is already connected to this repository")

    def disconnect_project(self):
        if self.project is not None:
            self.project = None
            return self
        raise NotFound("No project is connected to this repository")


class Project:
    __slots__ = ("name", "files", "parent", "repository")

    def __init__(self, name: str = "New Project", files: list = ("main.py"), parent=None, repository: Repository = None):
        self.name = name
        self.files = files
        self.parent = parent
        self.repository = repository

    def connect_repository(self, repository: Repository):
        if self.repository is None:
            self.repository = repository
            return self
        raise Satisfied("There is already a repository connected to this project")

    def delete(self):
        if self.parent is not None:
            self.parent.delete_project(self)
            return
        raise NotFound("This project is not owned by any PyCharm instance")


class GitHub:
    __slots__ = ("account", "repositories")

    def __init__(self, account: Account = None, repositories: list = ()):
        self.account = account
        self.repositories = repositories if repositories is not () else []

    def create_account(self, username: str, password: str, email: str):
        if self.account is None:
            self.account = Account(username, password, email)
            return self.account
        raise Satisfied("You already have an account")

    def create_repository(self, project: Project):
        if self.account is not None:
            new = Repository(self.account, project)
            self.repositories.append(new)
            return new
        raise NotFound("Your github account was not found, please create an account")


class PyCharm:
    __slots__ = ("projects", "account")

    def __init__(self, account: Account = None):
        self.projects = []
        self.account = account

    def create_project(self, name: str = "New Project", files: list = ("main.py")):
        new = Project(name=name, files=files, parent=self)
        self.projects.append(new)
        return new

    def delete_project(self, project: Project):
        if project in self.projects:
            self.projects.remove(project)
            return self
        raise NotFound("Project is not owned by this PyCharm instance")

    def connect_account(self, account: Account):
        if self.account is None:
            self.account = account
            return self
        raise Satisfied("An account is already connected to this PyCharm instance")
