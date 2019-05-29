import openpyxl
import os

#저장 할 파일 이름

def print_and_save_result_to_excel(testResult) :
    file_name = 'result.xlsx'

    if os.path.isfile(file_name):
    #file 있을시 load
        wb = openpyxl.load_workbook(file_name)
    # 데이터를 넣을 시트를 활성화합니다.
        sheet1 = wb.active
    else:
    #file 없을시 생성
        wb = openpyxl.Workbook()
    # 데이터를 넣을 시트를 활성화합니다.
        sheet1 = wb.active
    #시트의 이름을 정합니다.
        sheet1.title = 'resultSheet'


    # 넣을 list -> result_list
    result_list = testResult
    first_row = ["#########", "TESTIFY"]
    print(str(first_row))
    sheet1.append(first_row)
    
    second_row = ["Title", "Predict Precision", "Actual Genre", "Predict #1", "Predict #2", "Predict #3" ]
    print(str(second_row))
    sheet1.append(second_row)
    # sheet1에 list추가.
    for result in result_list:
    # Result :
    # [ '타이틀' ' 범위 이내 맞춘 빈도', 실제 장르, '정확도 예측값', '맞춘 것만' ]
        # 정확도 계산에 사용됨. 
        tmp_len = len(result[2]) 
        if tmp_len >=4 :
            tmp_len = 3
        result_row = [result[0], result[1]/tmp_len, str(result[2]), result[3][0][0], result[3][1][0], result[3][2][0] ]
        print(str(result_row))
        sheet1.append( result_row )
    last_row = ["#########", "#########"]
    print(str(last_row))
    sheet1.append(last_row)
    # excel 저장.
    wb.save(filename=file_name)
