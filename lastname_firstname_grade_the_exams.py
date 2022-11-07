import regex as re
skipped_answer = []
incorrect_answer = []
class_score = []
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_key_list = answer_key.split(',')
def find_max_count(list): #define hàm tìm số lượng nhiều nhất
    item_with_max_count = []
    max_count = 0
    for item in list:
        item_count = list.count(item)
        if  item_count > max_count:
            max_count = item_count
    for item1 in list:
        if list.count(item1) == max_count:
            if item1 in item_with_max_count:
                continue
            else: item_with_max_count.append(item1)
    item_with_max_count.sort()
    return item_with_max_count
def find_mean(list): #define hàm tìm trung bình
    Sum = sum(list)
    mean = Sum / len(list)
    return round(mean,2)
def find_median(list): #define hàm tìm trung vị
    list.sort()
    if len(list) % 2 == 0:
        median = (list[len(list)//2] + list[len(list)//2 - 1]) / 2
    else: median = list[len(list) // 2]
    return round(median,2)
filename = input("Enter a class to grade (i.e. class1 for class1.txt): ").strip()
try:
    file1 = open(f'{filename}.txt, 'r')
except:
    print('File cannot be found.')
else:
    print(f'Successfully opened {filename}')
    with open(f'{filename}_grade.txt','w') as grade_file:
        print('**** ANALYZING ****')
        valid_data = 0
        lines = file1.readlines()
        for line in lines:
            student_answer_list = line.split(',') #Nạp câu trả lời của sinh viên vào một list
            if len(student_answer_list) == 26 and re.search('N\d{8}', student_answer_list[0]): #Kiểm tra tính hợp lệ của câu trả lời và mã sinh viên
                valid_data += 1
                student_score = 0
                for index in range(0,len(answer_key_list)):
                    if student_answer_list[index + 1].replace('\n','') == '':
                        skipped_answer.append(index+1) #add số thứ tự các câu trả lời bị skip vào list
                    elif student_answer_list[index + 1].replace('\n','') == answer_key_list[index]:
                        student_score += 4
                    else:
                        student_score -= 1
                        incorrect_answer.append(index+1)  #add số thứ tự các câu trả lời bị sai vào list
                grade_file.write(f'{student_answer_list[0]}, {student_score} \n')
                class_score.append(student_score)
            elif len(student_answer_list) != 26: #Kiểm tra số lượng câu trả lời của mỗi sinh viên
                print('Invalid line of data: does not contain exactly 26 values:')
                print(f'{line}')
            elif not re.search('N\d{8}', student_answer_list[0]) : #Kiểm tra định dạng mã sinh viên
                print('Invalid line of data: N# is invalid')
                print(f'{line}')
        if valid_data == len(lines):
            print('No errors found!')
        invalid_lines = len(lines) - valid_data
        print('**** REPORT ****')
        print(f'Total valid lines of data: {valid_data}')
        print(f'Total invalid lines of data: {invalid_lines}')
        most_skipped_question = find_max_count(skipped_answer)
        most_incorrect_answer = find_max_count(incorrect_answer)
        high_score_count = 0
        for score in class_score:
            if score > 80:
                high_score_count += 1 #Đếm số lượng sinh viên trên 80đ
        print(f'Total student of high scores: {high_score_count}')
        mean = find_mean(class_score)
        print(f'Mean (average) score: {mean}')
        max_score = max(class_score)
        print(f'Highest score: {max_score}')
        min_score = min(class_score)
        print(f'Lowest score: {min_score}')
        print(f'Range of scores: {max_score - min_score}')
        med = find_median(class_score)
        print(f'Median score: {med}')
        string = 'Question that most people skip: '
        for question in most_skipped_question:
            string += str(question) + ' - ' + str(skipped_answer.count(question)) + ' - ' + str(round(skipped_answer.count(question)/valid_data,2)) + ', '
        print(string[:-2]+'.')
        string1= 'Question that most people answer incorrectly: '
        for question in most_incorrect_answer:
            string1 += str(question) + ' - ' + str(incorrect_answer.count(question)) + ' - ' + str(round(incorrect_answer.count(question)/valid_data,2)) + ', '
        print(string1[:-2]+'.')


    file1.close()