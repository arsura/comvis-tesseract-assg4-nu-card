def read_line_to_list(src_path):
    with open(src_path) as fp:  
        lines = list(filter(None, (line.rstrip() for line in fp)))
    return lines

def write_line(dst_path, file_name, data):
    with open(dst_path + file_name, 'a') as fp:  
        for line in data:
            fp.write(line + "\n")
