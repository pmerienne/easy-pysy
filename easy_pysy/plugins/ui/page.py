from easy_pysy.plugins.ui.element import Element


class Page(Element):
    @classmethod
    def get_template_path(cls):
        return f'ui/pages/{cls.__name__}.html'

    @classmethod
    def get_tag(cls):
        return super(Page, cls).get_tag() + '-page'
