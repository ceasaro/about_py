import logging
import os

from datetime import datetime
from git import Repo

from utils.bunch import Bunch
from utils.exceptions import AboutPyException

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
    repo = Repo(locate_git())
    assert not repo.bare

    vcs_bunch = Bunch()
    last_commit = repo.commit()
    vcs_bunch.commit_id = last_commit.hexsha
    vcs_bunch.committed_date = last_commit.committed_date
    vcs_bunch.message = last_commit.message
    vcs_bunch.committer = last_commit.committer.name
    vcs_bunch.committer_email = last_commit.committer.email
    return vcs_bunch


try:
    vcs_data = get_vcs_info()
    print "id: {0}, date: {1}, committer: {2}".format(vcs_data.commit_id,
                                                      datetime.fromtimestamp(vcs_data.committed_date),
                                                      vcs_data.committer)
except AboutPyException as e:
   LOG.warn('no vcs detected. cause: {}'.format(e.message))

