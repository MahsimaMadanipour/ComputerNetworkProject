"""
Computer Networks Project: Error Control Functions (Check-Sum, Hamming-Code)

Author: Mahsima Madanipour - 9813011030
"""
import random

#Add an 8bit EDC data at the end of the raw data by using check-sum method.
def checksum_sender(the_data):
    subdatas_8bit = [the_data[i : i + 8] for i in range(0, len(the_data), 8)]
    b_sum = "00000000"

    for i in range(len(subdatas_8bit)):
        b_sum = binary_sum(b_sum, subdatas_8bit[i])
        
    edc = binary_complement(b_sum)
    data_with_edc = the_data + edc

    return data_with_edc

#Check if the recieved data is correct or not(having an error bit) by using check-sum method.
def checksum_reciever(the_data):
    subdatas_8bit = [the_data[i : i + 8] for i in range(0, len(the_data), 8)]
    b_sum = "00000000"

    for i in range(len(subdatas_8bit)):
        b_sum = binary_sum(b_sum, subdatas_8bit[i])

    complement = binary_complement(b_sum)
    if complement == "00000000":
        return True
    else:
        return False
    
#Calculate the complement of a binary data
def binary_complement(the_binary):
    b_complement = ""

    for i in range(len(the_binary)):
        if the_binary[i] == "0":
            b_complement += "1" 
        else:
            b_complement += "0"

    return b_complement

#Calculate Sum of two binary datas in 8bit(ignoring the overflow)
def binary_sum(first_binary, second_binary):
    result = ""
    holder = "0"
    for i in range(0, 8):
        if first_binary[7 - i] == "0" and second_binary[7 - i] == "0" and holder == "0":
            result = "0" + result
            holder = "0"
        elif first_binary[7 - i] == "1" and second_binary[7 - i] == "0" and holder == "0":
            result = "1" + result
            holder = "0"
        elif first_binary[7 - i] == "0" and second_binary[7 - i] == "1" and holder == "0":
            result = "1" + result
            holder = "0"
        elif first_binary[7 - i] == "1" and second_binary[7 - i] == "1" and holder == "0":
            result = "0" + result
            holder = "1"
        elif first_binary[7 - i] == "0" and second_binary[7 - i] == "0" and holder == "1":
            result = "1" + result
            holder = "0"
        elif first_binary[7 - i] == "1" and second_binary[7 - i] == "0" and holder == "1":
            result = "0" + result
            holder = "1"
        elif first_binary[7 - i] == "0" and second_binary[7 - i] == "1" and holder == "1":
            result = "0" + result
            holder = "1"
        elif first_binary[7 - i] == "1" and second_binary[7 - i] == "1" and holder == "1":
            result = "1" + result
            holder = "1"

    return result

#Add some bits of EDC data(number of EDC depends of length of raw data) in the middle(power of two indexes) of the raw data 
##by using hamming code method.
def hammingcode_sender(the_data):
    data_list = [the_data[i] for i in range(len(the_data))]

    min_edc_bit = 0
    for num in range(0, len(the_data)):
        if 2 ** num > len(the_data) + num + 1:
            min_edc_bit = num
            break

    data_with_edc_length = len(the_data) + min_edc_bit
    edc_positions = [2 ** number for number in range(0, int(data_with_edc_length / 3))]
    data_with_edc = [0 for i in range(data_with_edc_length)]

    for index in range(data_with_edc_length):
        if (index + 1) not in edc_positions:
            data_with_edc[index] = data_list[0]
            data_list.remove(data_list[0])
    
    for index in range(data_with_edc_length):
        if (index + 1) in edc_positions:
            data_with_edc[index] = parity_bit(data_with_edc, index + 1)
    
    return "".join(data_with_edc)           

#Check if the recieved data is correct or not(having an error bit) by using hamming code method.
def hammingcode_reciever(the_data):
    data_list = [the_data[i] for i in range(len(the_data))]
    edc_positions = [2 ** number for number in range(0, int(len(data_list) / 3))]

    error_position = 0

    for index in range(len(data_list)):
        if (index + 1) in edc_positions:
            if parity_bit(data_list, index + 1) != data_list[index]:
                error_position += index + 1
    
    if error_position == 0:
        return True, error_position
    else:
        return False, error_position

#Calculate the parity bit of data
def parity_bit(the_data_list, edc_position):
        temp_data = []

        while edc_position <= len(the_data_list):
            temp_data.extend(the_data_list[edc_position : edc_position + edc_position])
            edc_position += 2 * edc_position
        
        temp_data.remove(temp_data[0])
        if temp_data.count("1") % 2 == 0:
            return "0"
        else:
            return "1"

#At first, the user choose the method for adding EDC data and then after generating the data + EDC with "generate_error" 
##function change one bit of the data with weight of 0.3 and change it (e.g.: if the choosen bit is 1, it will turn to 0)
def random_error_generator(the_data):

    def generate_error(the_data):
        options = [number + 1 for number in range(len(the_data))]
        weights = [0.3 for i in range(len(options))]

        random_position = random.choices(options, weights)[0]

        error_data = the_data[0:random_position - 1]
        if the_data[random_position - 1] == "0":
            error_data += "1"
        else:
            error_data += "0"
        error_data += the_data[random_position:]

        return error_data

    print("0. Check-Sum")
    print("1. Hamming-Code")
    method = int(input("Enter The Number: "))

    while method not in [0, 1]:
        method = int(input("Enter The Correct Number: "))
        
    if method == 0:
        print("Data (Before Adding EDC): {}".format(the_data))
        data = checksum_sender(the_data)
        print("Data (After Adding EDC): {}".format(data))
        data = generate_error(data)
        print("Data with an Error Bit: {}".format(data))
        return data, "check-sum"
    else:
        print("Data (Before Adding EDC): {}".format(the_data))
        data = hammingcode_sender(the_data)
        print("Data (After Adding EDC): {}".format(data))
        data = generate_error(data)
        print("Data with an Error Bit: {}".format(data))
        return data, "hamming-code"

#The running part, first get a data from user in terminal and then if the data length was not divisible by 8, will make it 
##divisible by 8 by adding meaningless 0s at the begining of data. And then check the returned data from "random_error_generator"
##function has error or not.
if __name__ == "__main__":
    print("--> Computer Networks Extra Project")

    raw_data = input("Enter Binary Data: ")
    if len(raw_data) % 8:
        raw_data = "0"*(((int(len(raw_data) / 8) + 1) * 8) - len(raw_data)) + raw_data

    print("Raw Data: {}".format(raw_data))
    data, method = random_error_generator(raw_data)

    if method == "check-sum":
        checking_data = checksum_reciever(data)
        if checking_data:
            #never comes here =)
            pass
        else:
            print("This Data Has Errors!!!")
    else:
        checking_data, error_position = hammingcode_reciever(data)
        if checking_data:
            #never comes here =)
            pass
        else:
            print("This Data Has Errors!!!")