import openpyxl
import os

#저장 할 파일 이름


def saveResult(testResult) :
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
    result_list = []
    result_list.append(testResult)

    #sheet1에 list추가.
    for row_index in range(len(result_list)):
        sheet1.append(result_list[row_index])

    # excel 저장.
    wb.save(filename=file_name)
