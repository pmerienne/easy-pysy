from typing import ClassVar

from easy_pysy.plugins.ui.meta import ElementMetaInformation
from easy_pysy.plugins.ui.reactivity import ReactiveData
from easy_pysy.utils.naming import camel_to_kebab


class Element(ReactiveData):
    shadow_mode: ClassVar[str] = 'closed'

    @classmethod
    def get_tag(cls):
        return camel_to_kebab(cls.__name__)

    @classmethod
    def get_template_path(cls):
        return f'ui/elements/{cls.__name__}.html'

    @classmethod
    def get_template(cls):
        template_path = cls.get_template_path()
        with open(template_path, 'r') as template_file:
            return template_file.read()

    @classmethod
    def get_meta(cls) -> ElementMetaInformation:
        parent_meta = super(Element, cls).get_meta()
        return ElementMetaInformation(
            tag=cls.get_tag(),
            template=cls.get_template(),
            shadow_mode=cls.shadow_mode,
            **parent_meta.dict(),
        )
