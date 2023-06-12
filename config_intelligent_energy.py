path=''

lineno_header_data=0
no_headerlines_ignore=1
x_axis_field="Time [s]"
delimiter=","
unwanted_keys=["D Type", "Stack Temperature #2 (mean) [degC]", "OVOC Fault DI High [-]","DCDC Fault DI High [-]","Fault Code (word1)","Button #1 + #2","Safety Circuit Safety #1 + #2"]

def lineskipper(file):
    for line in file:
        if line[0] == 'E' or line[0] == 'N':
            continue
        yield line

lambdadict={}