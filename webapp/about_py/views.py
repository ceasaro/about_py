import logging

from django.views.generic import TemplateView

from about_py.core.vcs import get_vcs_info
from utils.exceptions import AboutPyException

LOG = logging.getLogger(__name__)


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context_data = super(AboutView, self).get_context_data(**kwargs)
        context_data['vcs'] = self.get_vcs()
        return context_data

    def get_vcs(self):
        try:
            return get_vcs_info()
        except AboutPyException as e:
           LOG.warn('no vcs detected. cause: {}'.format(e.message))
           return {}