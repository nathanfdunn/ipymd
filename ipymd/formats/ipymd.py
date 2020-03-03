
from .markdown import MarkdownReader, MarkdownWriter

class IpymdReader(MarkdownReader):
	def parse_fences(self, m):
		lang = m.group(2)
		code = m.group(3).rstrip()
		if lang == 'python-cell':
			return self._code_cell(code)
		else:
			return self._markdown_cell_from_regex(m)

	def _parse_output(self, cell):
		if cell is None or cell['cell_type'] != 'markdown':
			return False, None

		beginning = '```output-cell\n'
		if cell['source'].startswith(beginning):
			content = cell['source'].replace(beginning, '', 1).rstrip().rstrip('`').rstrip()
			return True, content
		elif cell['source'].startswith('![output:'):
			# Unfortunately, we can't translate back to jupyter format yet
			return True, ''
		else:
			return False, None

	def read(self, text, rules=None):
		raw_cells = super(MarkdownReader, self).read(text, rules)
		cells = []

		last_index = len(raw_cells) - 1

		for i, cell in enumerate(raw_cells):
			if cell['cell_type'] == 'cell_metadata':
				if i + 1 <= last_index:
					raw_cells[i + 1].update(metadata=cell['metadata'])
			else:
				cells.append(cell)

		outcells = []
		i = 0
		while i < len(cells):
			cell = cells[i]
			next = cells[i+1] if i + 1 < len(cells) else None
			is_output, output_content = self._parse_output(next)
			if cell['cell_type'] == 'code' and is_output:
				cell['output'] = output_content
				outcells.append(cell)
				i += 2		# skip the output block
			else:
				outcells.append(cell)
				i += 1

		return outcells


	def _code_cell(self, source):
		"""Split the source into input and output."""
		# input, output = self._prompt.to_cell(source)
		return {'cell_type': 'code',
				'input': source,
				'output': ''}			# Provide output on the second pass


class IpymdWriter(MarkdownWriter):
	def append_code(self, input, output=None, metadata=None):
		code = input
		wrapped = '```python-cell\n{code}\n```'.format(code=code.rstrip())
		# We have an image
		if '|' in output:
			caption, data = output.split('|')
			wrapped += '\n![output:{caption}](data:image/png;base64,{data})\n'.format(caption=caption, data=data)
		elif output:
			wrapped += '\n```output-cell\n{output}\n```'.format(output=output)
		self._output.write(self.meta(metadata) + wrapped)


IPYMD_FORMAT = dict(
    reader=IpymdReader,
    writer=IpymdWriter,
    file_extension='.ipymd',
    file_type='text',
)