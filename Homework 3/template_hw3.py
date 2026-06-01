'''
Homework 3: HL7 Parsing and Modification
'''

'''
Before you start coding, you should use www.hl7inspector.com to interrogate the HL7 file.
Load the message on www.hl7inspector.com to figure out the indices with which to access the fields.
Experiment a bit to get the correct component and sub-component for the fields.
'''

'''
You might have to install certain packages using the command 'pip install package_name' on your system.
'''
# TODO: Import necessary packages
import hl7
import json

# TODO: Read the HL7 message file 'sample-hl7.txt'.
with open('sample-hl7.txt', 'r') as f:
    message_str = f.read()

# TODO: Convert the newlines to carriage returns to properly parse the HL7 message
message_str = message_str.replace('\n', '\r')

# TODO: Parse the message
message = hl7.parse(message_str)


'''
To retrieve any value, the convention is Message[segment][field][repetition][component][sub-component]
Here segment is the name, e.g., PID, PV1, OBX and field is the numeric index of the value from hl7inspector.com
'''

############# Retreiving the fields #############

pid = message['PID'][0]
pv1 = message['PV1'][0]
obr = message['OBR'][0]

# TODO: Find the patient's ID
patient_id = str(pid[2])

# TODO: Find the patient's name
patient_name = str(pid[5])

# TODO: Find the patient's DOB
patient_dob = str(pid[7])

# TODO: Find the name of the referring doctor
referring_doctor = str(pv1[8])

# TODO: Find the patient's administrative sex
patient_sex = str(pid[8])

# TODO: Find the reason for study
reason_for_study = str(obr[31])

# TODO: Find the procedure code
procedure_code = str(obr[44])

'''
The diagnosis information is contained in multiple fields.  Therefore, the value will be an array.
'''
# TODO: Find lines of the diagnosis description
diagnosis_description = [str(dg1[4]) for dg1 in message['DG1']]

'''
The impression information is contained in multiple fields.  Therefore, the value will be an array.
'''
# TODO: Find lines of the impression
impression = []
in_impression = False
for obx in message['OBX']:
    line = str(obx[5])
    stripped = line.strip()
    if stripped.startswith('IMPRESSION'):
        in_impression = True
        continue
    if in_impression:
        if stripped.startswith('FOCAL_MASS_SUMMARY'):
            break
        if stripped:
            impression.append(line)

'''
Make sure you follow the json structure provided in the homework instructions.
The keys for the fields are given below.  Please use the exact spelling in your output.

Patient ID
Patient Name
Patient DOB
Referring Doctor Name
Patient Sex
Reason For Study
Procedure Code
Diagnosis Description
Impression

'''
# TODO: Create the output data dictionary
output_data = {
    "Patient ID": patient_id,
    "Patient Name": patient_name,
    "Patient DOB": patient_dob,
    "Referring Doctor Name": referring_doctor,
    "Patient Sex": patient_sex,
    "Reason For Study": reason_for_study,
    "Procedure Code": procedure_code,
    "Diagnosis Description": diagnosis_description,
    "Impression": impression,
}

# TODO: Store the data dictionary in a file as specified in the homework instructions.
with open('output.json', 'w') as f:
    json.dump(output_data, f, indent=4)


############# Modifying the fields #############

'''
As per the homework instructions, modify the following fields and
output the modified file.
Make sure each field is formatted as defined for the hl7 file format.
'''

# TODO: Change the patient's ID
pid[2] = '99999999'

# TODO: Change the patient's name
pid[5] = 'FRANKLIN^BENJAMIN'

# TODO: Change the patient's DOB
pid[7] = '19780101'

# TODO: Change the patient's sex
pid[8] = 'O'

# TODO: Change the name and NPI number of the referring doctor in the patient visit segment
pv1[8] = '0987654321^SPOCK^THOMAS^^^^^^NPI'

# TODO: Change the reason for study
obr[31] = '^nonspecific abdominal pain'

############# Saving the modified file #############


# TODO: Write the modified message as specified in the homework instructions
with open('modified-hl7.txt', 'w', newline='') as f:
    f.write(str(message))



############# ALL THE BEST :) #############
