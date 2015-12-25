import logging
import os

from git import Repo, InvalidGitRepositoryError

from about_py.utils.bunch import Bunch
from about_py.utils.exceptions import AboutPyException

join = os.path.join

LOG = logging.getLogger(__name__)


def locate_git(path=None):
    if not path:
        path = os.path.abspath('.')

    git_dir = os.path.join(path, '.git')
    if os.path.isdir(git_dir):
        return path

    else:
        parent_path = os.path.abspath(os.path.join(path, os.pardir))
        if parent_path == path:
            raise AboutPyException('No git repository found.')
        else:
            return locate_git(parent_path)


def get_vcs_info():
    # rorepo is a a Repo instance pointing to the git-python repository.
    # For all you know, the first argument to Repo is a path to the repository
    # you want to work with
    try:
        vcs_bunch = Bunch()
        repo = Repo(locate_git())
        assert not repo.bare

        vcs_bunch.name = 'Git'
        vcs_bunch.origin = repo.remotes['origin']
        vcs_bunch.last_commit = {
            'message': repo.commit().message,
            'url': '{0}/commit/{1}'.format(vcs_bunch.origin.url, repo.commit().hexsha)
        }
        return vcs_bunch
    except InvalidGitRepositoryError:
        return
