def read_line_to_list(src_path):
    with open(src_path) as fp:  
        lines = list(filter(None, (line.rstrip() for line in fp)))
    return lines
