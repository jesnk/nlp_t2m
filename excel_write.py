import openpyxl
import os

#저장 할 파일 이름


def save_result_to_excel(testResult) :
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
    ''' 
    result_list = []
    result_list.append(("f","g","h"))
    result_list.append(("i","j","k","a"))
    '''
    result_list = testResult
    sheet1.append(["#########", "TESTIFY"])
    sheet1.append( ["Title", "Predict Precision", "Actual  Genre", "Predict G #1", "Predict G #2", "Predict G #3" ])
    # sheet1에 list추가.
    for result in result_list:
    # Result :
    # [ '타이틀' ' 범위 이내 맞춘 빈도', 실제 장르, '정확도 예측값', '맞춘 것만' ]
        sheet1.append( [result[0], result[1]/len(result[2]), str(result[2]), result[3][0][0], result[3][1][0], result[3][2][0] ] )
    sheet1.append(["#########", "#########"])

    # excel 저장.
    wb.save(filename=file_name)
