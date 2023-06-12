path = ''

lineno_header_data = 0
no_headerlines_ignore = 1
x_axis_field="time"
delimiter=","
unwanted_keys=[]
lineskipper = lambda file: (line for line in file)

lambdadict={
    'key1': lambda x: -x
}