import regex as re
import pandas as pd
import numpy as np
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
class_dict = {}
answer_key_list = np.array(answer_key.split(','))
filename = input("Enter a class to grade (i.e. class1 for class1.txt): ").strip()
def count_value(array,value):
    counter = 0
    for item in array:
        if item == value:
            counter += 1
    return counter #Hàm đếm số lần xuất hiện của một giá trị

try:
    file1 = open(f'{filename}.txt', 'r')
except:
    print('File cannot be found.')
else:
    with open(f'{filename}_grade.txt','w') as grade_file:
        print(f'Successfully opened file')
        print('**** ANALYZING ****')
        valid_data = 0
        lines = file1.readlines()
        for line in lines:
            student_answer_list = line.strip().split(',') #Nạp câu trả lời của sinh viên vào một list
            if len(student_answer_list) == 26 and re.search('N\d{8}', student_answer_list[0]): #Kiểm tra tính hợp lệ của câu trả lời và mã sinh viên
                valid_data += 1
                student_score = []
                for index in range(0, len(answer_key_list)):
                    if student_answer_list[index + 1] == '':
                        student_score.append(0)
                    elif student_answer_list[index + 1] == answer_key_list[index]:
                        student_score.append(4)
                    else:
                        student_score.append(-1) #nạp điểm của sinh viên vào list student_answer_list
                grade_file.write(f'{student_answer_list[0]}, {sum(student_score)} \n') #ghi điểm của sinh viên ra file classname_grade.txt
                class_dict[student_answer_list[0]] = student_score #lưu lại điểm của các sinh viên trả lời hợp lệ vào dict  class_dict
            elif len(student_answer_list) != 26:
                print('Invalid line of data: does not contain exactly 26 values:')
                print(f'{line}') #in ra các sinh viên trả lời không đủ 26 câu
            elif not re.search('N\d{8}', student_answer_list[0]) :
                print('Invalid line of data: N# is invalid')
                print(f'{line}') #in ra các sinh viên có mã sinh viên không hợp lệ
        if valid_data == len(lines):
            print('No errors found!')
        invalid_lines = len(lines) - valid_data
        print('**** REPORT ****')
        print(f'Total valid lines of data: {valid_data}')
        print(f'Total invalid lines of data: {invalid_lines}')
        df = pd.DataFrame(class_dict)
        df.loc["Total"] = df.sum()
        highscore = (df.loc['Total']>80).sum()  # Trả về series boolean, tổng các giá trị True sẽ bằng số học sinh được trên 80đ
        print(f'Total student of high scores: {highscore}')
        mean = (df.loc['Total']).mean()
        print(f'Mean (average) score: {mean}')
        max = (df.loc['Total']).max()
        print(f'Highest score: {max}')
        min = (df.loc['Total']).min()
        print(f'Lowest score: {min}')
        print(f'Range of scores: {max - min}')
        med = (df.loc['Total']).median()
        print(f'Median score: {med}')
        df['Skip_Counter'] = df.apply(lambda x: count_value(x,0), axis = 1) #đếm số lượng câu trả lời được bỏ qua của mỗi sinh viên
        df['Incorrect_Counter'] = df.apply(lambda x: count_value(x, -1), axis=1) #đếm số lượng câu trả lời sai của mỗi sinh viên
        df2 = df.loc[df['Skip_Counter'] == df['Skip_Counter'].max()] #liệt kê những câu hỏi skip nhiều câu hỏi nhất
        df3 = df.loc[df['Incorrect_Counter'] == df['Incorrect_Counter'].max()] #liệt kê những câu hỏi bị sinh viên trả lời sai nhiều nhất
        most_skipped_index = df2.index.tolist()
        most_incorrect_counter = df3.index.tolist()
        string = 'Question that most people skip: '
        for question in most_skipped_index: #loop qua list những câu hỏi bị skip nhiều nhất để in ra màn hình (+1 vào index để đưa về đúng số thứ tự câu hỏi trong bài)
            string += str(question + 1) + ' - ' + str(df['Skip_Counter'].max()) + ' - ' + str(round(df['Skip_Counter'].max() / valid_data, 2)) + ', '
        print(string[:-2] + '.')
        string1 = 'Question that most people answer incorrectly: '
        for question in most_incorrect_counter:
            string1 += str(question + 1) + ' - ' + str(df['Incorrect_Counter'].max()) + ' - ' + str(round(df['Incorrect_Counter'].max() / valid_data, 2)) + ', '
        print(string1[:-2] + '.')