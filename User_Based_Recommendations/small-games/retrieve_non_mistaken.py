source_filename = 'corrected_objects_links.txt'
dest_filename = 'actual_objects_links.txt'
source = open(source_filename, 'r')
dest = open(dest_filename, 'w')
links = []
for line in source:
    if not line in links and len(line.split('info')) == 2:
        links.append(line)
        dest.write(line)
source.close()
dest.close()
