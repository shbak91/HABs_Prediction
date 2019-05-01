# coding: utf-8

# 2019-04-29
# Code : S.H.Bak(PKNU Geoinfo. Marine RS/GIS/Drone Lab.)
# Program : DNN Model용 input data 생산

# import glob
import os
import numpy as np

# Target File : DailyFactor_TYGJ , DailyFactor_YS
# Path : ./2019xxxx/TYGJ/DailyFactor_TYGJ.csv

# Path
# HOME_DIR =  '/home/marinersgis/Redtide' # For Linux
HOME_DIR = 'G:/내 드라이브/대학원 관련 자료/연구실(PKNU)/(2017-2019년)KIOST 적조실증화과제/2019 적조실증화사업/04.모델개발/2019_0418 입력자료 생산 프로그램(Python)' # For Windows
# DATASET_DIR = HOME_DIR + '/Result' # For Linux
DATASET_DIR = HOME_DIR + '/모델 입력자료 생산 프로그램(python)' # For Windows



# print('예측 결과를 생산할 날짜(yyyymmdd)를 입력하시오. : ')
# PREDICT_DATE = input()

PREDICT_DATE = '20190410' # For Test

# Part 1 : 기본인자 생성

# step 0 : 폴더 리스트 생성
list_dir = os.listdir(DATASET_DIR)

# step 1 : 사용자에게 입력받은 날짜(PREDICT_DATE)가 폴더 리스트에서 몇 번째에 존재하는지 탐색한다.
for i in range(len(list_dir)):
    
    if list_dir[i] == PREDICT_DATE:
        
        fid = i

# AreaInfo : 결과를 출력시킬 지역의 리스트
AreaInfo = ['TYGJ', 'YS']

# AreaInfo 내에 저장된 지역마다 반복 작업 수행
for A in AreaInfo:

    # step 2 : 사용자에게 입력받은 날짜(D-Day)로부터 D-5까지의 폴더 내에 존재하는 DailyFactor_xx.csv를 불러온다.
    Factor_D1 = np.loadtxt(DATASET_DIR + '/' + list_dir[fid] + '/' + A + '/DailyFactor_' + A + '.csv',
                           skiprows=1,
                           delimiter=',')
    Factor_D2 = np.loadtxt(DATASET_DIR + '/' + list_dir[fid - 1] + '/' + A + '/DailyFactor_' + A + '.csv',
                           skiprows=1,
                           delimiter=',')
    Factor_D3 = np.loadtxt(DATASET_DIR + '/' + list_dir[fid - 2] + '/' + A + '/DailyFactor_' + A + '.csv',
                           skiprows=1,
                           delimiter=',')
    Factor_D4 = np.loadtxt(DATASET_DIR + '/' + list_dir[fid - 3] + '/' + A + '/DailyFactor_' + A + '.csv',
                           skiprows=1,
                           delimiter=',')
    Factor_D5 = np.loadtxt(DATASET_DIR + '/' + list_dir[fid - 4] + '/' + A + '/DailyFactor_' + A + '.csv',
                           skiprows=1,
                           delimiter=',')
    Factor_D6 = np.loadtxt(DATASET_DIR + '/' + list_dir[fid - 5] + '/' + A + '/DailyFactor_' + A + '.csv',
                           skiprows=1,
                           delimiter=',')

    # step 3 : 기본인자 출력
    # 기본인자의 Data Frame Size :
    # len(Factor_D1) , 2(lat, lon) + 30(강수량, 일사량, 풍속, 풍향, 수온) + 6(기온)
    BasicFactor = np.zeros((len(Factor_D1), 38))

    # Location Info.
    BasicFactor[:, 0] = Factor_D1[:, 0]  # lat
    BasicFactor[:, 1] = Factor_D1[:, 1]  # lon

    # Rain : ncpcp
    # Factor_Dx[:, 3]
    BasicFactor[:, 2] = Factor_D1[:, 3]  # D4Rain
    BasicFactor[:, 3] = Factor_D2[:, 3]  # D5Rain
    BasicFactor[:, 4] = Factor_D3[:, 3]  # D6Rain
    BasicFactor[:, 5] = Factor_D4[:, 3]  # D7Rain
    BasicFactor[:, 6] = Factor_D5[:, 3]  # D8Rain
    BasicFactor[:, 7] = Factor_D6[:, 3]  # D9Rain

    # Sun : swdir
    # Factor_Dx[:, 2]
    BasicFactor[:, 8] = Factor_D1[:, 2]  # D4Sun
    BasicFactor[:, 9] = Factor_D2[:, 2]  # D5Sun
    BasicFactor[:, 10] = Factor_D3[:, 2]  # D6Sun
    BasicFactor[:, 11] = Factor_D4[:, 2]  # D7Sun
    BasicFactor[:, 12] = Factor_D5[:, 2]  # D8Sun
    BasicFactor[:, 13] = Factor_D6[:, 2]  # D9Sun

    # Wind : wspd
    # Factor_Dx[:, 4]
    BasicFactor[:, 14] = Factor_D1[:, 4]  # D4Wind
    BasicFactor[:, 15] = Factor_D2[:, 4]  # D5Wind
    BasicFactor[:, 16] = Factor_D3[:, 4]  # D6Wind
    BasicFactor[:, 17] = Factor_D4[:, 4]  # D7Wind
    BasicFactor[:, 18] = Factor_D5[:, 4]  # D8Wind
    BasicFactor[:, 19] = Factor_D6[:, 4]  # D9Wind

    # WindD : wdir
    # Factor_Dx[:, 5]
    BasicFactor[:, 20] = Factor_D1[:, 5]  # D4WindD
    BasicFactor[:, 21] = Factor_D2[:, 5]  # D5WindD
    BasicFactor[:, 22] = Factor_D3[:, 5]  # D6WindD
    BasicFactor[:, 23] = Factor_D4[:, 5]  # D7WindD
    BasicFactor[:, 24] = Factor_D5[:, 5]  # D8WindD
    BasicFactor[:, 25] = Factor_D6[:, 5]  # D9WindD

    # WaterTemp : stmp
    # Factor_Dx[:, 7]
    BasicFactor[:, 26] = Factor_D1[:, 7]  # D4WaterTemp
    BasicFactor[:, 27] = Factor_D2[:, 7]  # D5WaterTemp
    BasicFactor[:, 28] = Factor_D3[:, 7]  # D6WaterTemp
    BasicFactor[:, 29] = Factor_D4[:, 7]  # D7WaterTemp
    BasicFactor[:, 30] = Factor_D5[:, 7]  # D8WaterTemp
    BasicFactor[:, 31] = Factor_D6[:, 7]  # D9WaterTemp

    # AirTemp : atmp
    # Factor_Dx[:, 6]
    # 요약인자와 파생인자 생산 이후 제거 대상
    BasicFactor[:, 32] = Factor_D1[:, 6]  # D4AirTemp
    BasicFactor[:, 33] = Factor_D2[:, 6]  # D5AirTemp
    BasicFactor[:, 34] = Factor_D3[:, 6]  # D6AirTemp
    BasicFactor[:, 35] = Factor_D4[:, 6]  # D7AirTemp
    BasicFactor[:, 36] = Factor_D5[:, 6]  # D8AirTemp
    BasicFactor[:, 37] = Factor_D6[:, 6]  # D9AirTemp

    # Export to csv
    np.savetxt(DATASET_DIR + '/' + list_dir[fid] + '/' + A + '/DailyInput_' + A +'.csv',
               BasicFactor,
               delimiter=',',
               fmt='%3.4f',
               header='lat,lon,D4Rain,D5Rain,D6Rain,D7Rain,D8Rain,D9Rain,'
                      'D4Sun,D5Sun,D6Sun,D7Sun,D8Sun,D9Sun,'
                      'D4Wind,D5Wind,D6Wind,D7Wind,D8Wind,D9Wind,'
                      'D4WindD,D5WindD,D6WindD,D7WindD,D8WindD,D9WindD,'
                      'D4WaterTemp,D5WaterTemp,D6WaterTemp,D7WaterTemp,D8WaterTemp,D9WaterTemp,'
                      'D4AirTemp,D5AirTemp,D6AirTemp,D7AirTemp,D8AirTemp,D9AirTemp',
               comments='')

# Part 2 : 요약 및 파생인자
# S
