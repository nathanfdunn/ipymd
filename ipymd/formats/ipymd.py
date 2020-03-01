
from .markdown import MarkdownReader, MarkdownWriter

class IpymdReader(MarkdownReader):
	def parse_fences(self, m):
		lang = m.group(2)
		code = m.group(3).rstrip()
		if lang == 'jupyter':
			return self._code_cell(code)
		else:
			# # Test the first line of the cell.
			# first_line = code.splitlines()[0]
			# if self._prompt.is_input(first_line):
			# 	return self._code_cell(code)
			# else:
			# 	return self._markdown_cell_from_regex(m)
			return self._markdown_cell_from_regex(m)

class IpymdWriter(MarkdownWriter):
	def append_code(self, input, output=None, metadata=None):
		# code = self._prompt.from_cell(input, output)
		code = input + '\n' + output
		wrapped = '```jupyter\n{code}\n```'.format(code=code.rstrip())
		self._output.write(self.meta(metadata) + wrapped)


IPYMD_FORMAT = dict(
    reader=IpymdReader,
    writer=IpymdWriter,
    file_extension='.ipymd',
    file_type='text',
)