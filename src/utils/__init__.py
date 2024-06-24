def pretty_print_program(program, indent=0):
    def _format_object(obj, level=0):
        if isinstance(obj, (str, int, float, bool, type(None))):
            return repr(obj)

        class_name = obj.__class__.__name__

        if hasattr(obj, '__dict__'):
            attrs = obj.__dict__
        elif isinstance(obj, (list, tuple)):
            return _format_sequence(obj, level)
        else:
            return repr(obj)

        # For (simple objects OR a list with 1 arg) with 3 or fewer attributes
        if len(attrs) <= 3 and all(isinstance(v, (str, int, float, bool, type(None))) for v in attrs.values()):
            attr_str = ", ".join(f"{k}={_format_object(v)}" for k, v in attrs.items())
            return f"{class_name}({attr_str})"

        lines = [f"{class_name}("]
        for attr, value in attrs.items():
            formatted_value = _format_object(value, level + 1)
            if '\n' in formatted_value:
                lines.append(f"{'  ' * (level + 1)}{attr}={formatted_value},")
            else:
                lines.append(f"{'  ' * (level + 1)}{attr}={formatted_value},")

        if lines[-1].endswith(','):
            lines[-1] = lines[-1][:-1]  # Remove trailing comma
        lines.append(f"{'  ' * level})")
        return '\n'.join(lines)

    def _format_sequence(seq, level):
        if len(seq) == 0:
            return '[]' if isinstance(seq, list) else '()'
        elif len(seq) == 1:
            formatted = _format_object(seq[0], level)
            return f'[{formatted}]' if isinstance(seq, list) else f'({formatted},)'

        seq_type = '[]' if isinstance(seq, list) else '()'
        lines = [seq_type[0]]
        for item in seq:
            formatted = _format_object(item, level + 1)
            lines.append(f"{'  ' * (level + 1)}{formatted},")
        if lines[-1].endswith(','):
            lines[-1] = lines[-1][:-1]  # Remove trailing comma
        lines.append(f"{'  ' * level}{seq_type[1]}")
        return '\n'.join(lines)

    print(_format_object(program))