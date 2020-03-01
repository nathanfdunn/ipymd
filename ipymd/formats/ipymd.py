
from markdown import BaseMarkdownReader, BaseMarkdownWriter

class IpymdReader(BaseMarkdownReader):
	pass

class IpymdWriter(BaseMarkdownWriter):
	pass


IPYMD_FORMAT = dict(
    reader=IpymdReader,
    writer=IpymdWriter,
    file_extension='.md',
    file_type='text',
)