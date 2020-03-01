
from .markdown import MarkdownReader, MarkdownWriter

class IpymdReader(MarkdownReader):
	pass

class IpymdWriter(MarkdownWriter):
	pass


IPYMD_FORMAT = dict(
    reader=IpymdReader,
    writer=IpymdWriter,
    file_extension='.ipymd',
    file_type='text',
)