# coding: utf-8

import numpy as np
import pandas as pd
import tensorflow as tf
import os
import glob
import datetime
import netCDF4
import math

Predict_DATE = '20190613' # 예보를 생산할 날짜
# Step 1 : Raw Data
if os.path.isdir(Predict_DATE) == False:

    os.mkdir(Predict_DATE)

# 날짜 연산을 위해 Predict_DATE를 String to Time 변환
Predict_DATE = datetime.datetime.strptime(Predict_DATE, '%Y%m%d')

# D4 = Predict_DATE - 2Day
# D5 = Predict_DATE - 3Day
# D6 = Predict_DATE - 4Day
# D7 = Predict_DATE - 5Day
# D8 = Predict_DATE - 6Day
# D9 = Predict_DATE - 7Day
D4 = datetime.datetime.strftime(Predict_DATE + datetime.timedelta(days=-2), '%Y%m%d')
D5 = datetime.datetime.strftime(Predict_DATE + datetime.timedelta(days=-3), '%Y%m%d')
D6 = datetime.datetime.strftime(Predict_DATE + datetime.timedelta(days=-4), '%Y%m%d')
D7 = datetime.datetime.strftime(Predict_DATE + datetime.timedelta(days=-5), '%Y%m%d')
D8 = datetime.datetime.strftime(Predict_DATE + datetime.timedelta(days=-6), '%Y%m%d')
D9 = datetime.datetime.strftime(Predict_DATE + datetime.timedelta(days=-7), '%Y%m%d')

# 날짜 연산 후 Predict_DATE를 다시 Time to String 변환
Predict_DATE = datetime.datetime.strftime(Predict_DATE, '%Y%m%d')

# Ref. File
Grid_YS = np.loadtxt('Grid/YS_Grid_Sea.csv', delimiter=',', skiprows=1)
Grid_TYGJ = np.loadtxt('Grid/TYGJ_Grid_Sea2.csv', delimiter=',', skiprows=1)

# User Define Function
# Distance
def dist(x1, x2, y1, y2):

    d = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    return(d)

# 날짜별 인자 불러오기
list_DATE = [D4, D5, D6, D7, D8, D9]
# list_DATE = [D4]
# TARGET_DATE : 적조 예보에 활용될 D-4 ~ D-9 (실제 예보에 활용될 날짜보다 하루 전 파일을 불러옴, D-5 ~ D-10)
for TARGET_DATE in list_DATE:

    # TARGET_DATE 폴더 생성
    # TARGET_DATE는 불러오는 KOOS 파일의 날짜임
    # 실제로 활용되는 자료는 KOOS 파일 내 D+1 자료
    # 따라서 폴더명은 TARGET_DATE + 1
    if os.path.isdir(Predict_DATE + '/' + str(int(TARGET_DATE)+1)) == False:

        os.mkdir(Predict_DATE + '/' + str(int(TARGET_DATE)+1))

    # KOOS_AT : windu, windv, atemp, solar, rain, lat, lon
    # KOOS_OC : temp
    AT = netCDF4.Dataset('SS_AT_' + TARGET_DATE + '12.nc')
    OC = netCDF4.Dataset('SS_OC_' + TARGET_DATE + '12.nc')

    # 위치정보
    lat = AT.variables['lat']
    lon = AT.variables['lon']
    Mat_lat = np.zeros((len(lat), len(lon)))
    Mat_lon = np.zeros((len(lat), len(lon)))

    # 좌표 테이블 생성
    for i in range(len(lon)):
        Mat_lat[:, i] = np.array(lat)

    for i in range(len(lat)):
        Mat_lon[i, :] = np.array(lon)

    lat = Mat_lat.reshape(-1, 1)
    lon = Mat_lon.reshape(-1, 1)

    # KOOS_AT Variable
    raw_swdir = np.array(AT.variables['solar'])
    raw_ncpcp = np.array(AT.variables['rain'])
    raw_windu = np.array(AT.variables['windu'])
    raw_windv = np.array(AT.variables['windv'])
    raw_atemp = np.array(AT.variables['atemp'])

    # KOOS_OC
    raw_stemp = np.array(OC.variables['temp'])

    # Data Table : 시간별 자료 분리
    list_T = [12, 15, 18, 21, 24, 27, 30, 33]
    for t in list_T:

        swdir = raw_swdir[t, :, :]
        ncpcp = raw_ncpcp[t, :, :]
        windu = raw_windu[t, :, :]
        windv = raw_windv[t, :, :]
        atemp = raw_atemp[t, :, :]
        stemp = raw_stemp[t, :, :]

        swdir = swdir.reshape(-1, 1)
        ncpcp = ncpcp.reshape(-1, 1)
        windu = windu.reshape(-1, 1)
        windv = windv.reshape(-1, 1)
        atemp = atemp.reshape(-1, 1)
        stemp = stemp.reshape(-1, 1)

        table = np.c_[lat, lon, swdir, ncpcp, windu, windv, atemp, stemp]

        # table 중 불필요한 영역 제거
        table = table[(table[:, 0] > 34.3) & (table[:, 0] < 34.9) & (table[:, 1] > 127.3) & (table[:, 1] < 128.7), :]

        # 예보생산 대상 해역의 좌표 추출
        temp_YS = np.zeros((len(Grid_YS), 6))
        temp_TYGJ = np.zeros((len(Grid_TYGJ), 6))
        output_YS = np.c_[Grid_YS, temp_YS]
        output_TYGJ = np.c_[Grid_TYGJ, temp_TYGJ]

        # 여수
        for i in range(len(Grid_YS)):

            # Grid Centroid와 Data Location 간의 거리 계산
            d = np.zeros(len(table))

            for j in range(len(table)):

                d[j] = dist(Grid_YS[i, 0], table[j, 0], Grid_YS[i, 1], table[j, 1])

            # d(거리)에 저장된 거리 중 가장 작은 값이 존재하는 위치(min_location)
            min_location = np.where(d == np.min(d))

            close_data = table[min_location, 2:]
            output_YS[i, 2:] = close_data

        # 통영-거제
        for i in range(len(Grid_TYGJ)):

            d = np.zeros(len(table))

            for j in range(len(table)):

                d[j] = dist(Grid_TYGJ[i, 0], table[j, 0], Grid_TYGJ[i, 1], table[j, 1])

            min_location = np.where(d == np.min(d))

            close_data = table[min_location, 2:]
            output_TYGJ[i, 2:] = close_data

        Time = t-12
        if Time < 10:

            Time = '0' + str(Time)

        elif Time >= 10:

            Time = str(Time)

        # 여수, 통영-거제 폴더 생성
        if os.path.isdir(Predict_DATE + '/' + str(int(TARGET_DATE)+1) + '/' + 'YS') == False:

            os.mkdir(Predict_DATE + '/' + str(int(TARGET_DATE)+1) + '/' + 'YS')

        if os.path.isdir(Predict_DATE + '/' + str(int(TARGET_DATE)+1) + '/' + 'TYGJ') == False:

            os.mkdir(Predict_DATE + '/' + str(int(TARGET_DATE)+1) + '/' + 'TYGJ')

        # 여수
        np.savetxt(Predict_DATE + '/' + str(int(TARGET_DATE)+1) + '/' + 'YS' + '/' + 'rawdata_' + Time + '.csv', output_YS, delimiter=',', fmt='%3.4f')

        # 통영-거제
        np.savetxt(Predict_DATE + '/' + str(int(TARGET_DATE)+1) + '/' + 'TYGJ' + '/' + 'rawdata_' + Time + '.csv', output_TYGJ, delimiter=',', fmt='%3.4f')

# Step 2 : Daily Composite
# output_YS[lat, lon, swdir, ncpcp, windu, windv, atemp, stemp]
# output_TYGJ[lat, lon, swdir, ncpcp, windu, windv, atemp, stemp]

# Predict_DATE 폴더 내에 있는 TARGET_DATE 폴더 리스트 생성
list_TARGET = os.listdir(Predict_DATE)

# TARGET_DATE 폴더 내 rawdata를 이용하여 일합성자료 생산
# SAVE_DIR = TARGET_DATE
for TARGET_DATE in list_TARGET:

    # 해역별 반복 : YS, TYGJ
    study_area = ['YS', 'TYGJ']
    for area in study_area:

        # rawdata list 생성
        list_rawdata = glob.glob(Predict_DATE + '/' + TARGET_DATE + '/' + area + '/' + '*.csv')

        # rawdata csv 파일을 순차적으로 불러와서 요소(Component)별 변수 할당
        # temp_csv : 경위도 좌표 칼럼을 불러오기 위해 임시로 1개의 rawdata csv를 불러옴
        temp_csv = np.loadtxt(list_rawdata[0], delimiter=',')

        # Location Info
        location_info = temp_csv[:, 0:2]

        temp_SWDIR = np.zeros((temp_csv.shape[0], len(list_rawdata)))
        temp_NCPCP = np.zeros((temp_csv.shape[0], len(list_rawdata)))
        temp_UGRD = np.zeros((temp_csv.shape[0], len(list_rawdata)))
        temp_VGRD = np.zeros((temp_csv.shape[0], len(list_rawdata)))
        temp_ATMP = np.zeros((temp_csv.shape[0], len(list_rawdata)))
        temp_STMP = np.zeros((temp_csv.shape[0], len(list_rawdata)))

        # Daily Composite
        for i in range(len(list_rawdata)):

            temp_csv = np.loadtxt(list_rawdata[i], delimiter=',')

            # col1 : SWDIR(일사량)
            # col2 : NCPCP(강수량)
            # col3 : UGRD
            # col4 : VGRD
            # col5 : ATMP
            # col6 : STMP
            temp_SWDIR[:, i] = temp_csv[:, 2]
            temp_NCPCP[:, i] = temp_csv[:, 3]
            temp_UGRD[:, i] = temp_csv[:, 4]
            temp_VGRD[:, i] = temp_csv[:, 5]
            temp_ATMP[:, i] = temp_csv[:, 6]
            temp_STMP[:, i] = temp_csv[:, 7]

        # SWDIR (Daily Mean)
        SWDIR = np.mean(temp_SWDIR, axis=1)

        # NCPCP (Mean(hour) * 24)
        NCPCP = np.mean(temp_NCPCP, axis=1) * 24

        # WSPEED (sqrt(U평균 제곱 + V평균 제곱))
        UGRD = np.mean(temp_UGRD, axis=1)
        VGRD = np.mean(temp_VGRD, axis=1)

        WSPD = np.zeros([UGRD.shape[0], 1])
        for i in range(len(UGRD)):
            WSPD[i] = math.sqrt((UGRD[i] * UGRD[i]) + (VGRD[i] * VGRD[i]))

        # WDIR
        WDIR = np.zeros([WSPD.shape[0], 1])
        for i in range(len(WSPD)):
            if UGRD[i] == 0 and VGRD[i] == 0:
                WDIR[i] = 0
            elif UGRD[i] == 0 and VGRD[i] > 0:
                WDIR[i] = 180
            elif UGRD[i] == 0 and VGRD[i] < 0:
                WDIR[i] = 0
            elif UGRD[i] > 0 and VGRD[i] == 0:
                WDIR[i] = 270
            elif UGRD[i] < 0 and VGRD[i] == 0:
                WDIR[i] = 90
            elif UGRD[i] > 0 and VGRD[i] > 0:
                WDIR[i] = math.atan(UGRD[i] / VGRD[i]) * 180/math.pi + 180
            elif UGRD[i] > 0 and VGRD[i] < 0:
                WDIR[i] = math.atan(UGRD[i] / VGRD[i]) * 180/math.pi + 360
            elif UGRD[i] < 0 and VGRD[i] < 0:
                WDIR[i] = math.atan(UGRD[i] / VGRD[i]) * 180/math.pi
            elif UGRD[i] < 0 and VGRD[i] > 0:
                WDIR[i] = math.atan(UGRD[i] / VGRD[i]) * 180/math.pi + 180

        # ATMP
        ATMP = np.mean(temp_ATMP, axis=1)

        # STMP
        STMP = np.mean(temp_STMP, axis=1)

        # Composite
        Data_Merged = np.c_[location_info, SWDIR, NCPCP, WSPD, WDIR, ATMP, STMP]

        # export csv
        np.savetxt(Predict_DATE + '/' + TARGET_DATE + '/' + area + '/' + 'DailyFactor.csv',
                  Data_Merged,
                  delimiter=',',
                  fmt='%3.4f',
                  header='lat,lon,swdir,ncpcp,wspd,wdir,atmp,stmp',
                  comments='')

# Step 3 : Input Data
for area in study_area:

    DF_D9 = np.loadtxt(Predict_DATE + '/' + list_TARGET[0] + '/' + area + '/' + 'DailyFactor.csv', delimiter=',', skiprows=1)
    DF_D8 = np.loadtxt(Predict_DATE + '/' + list_TARGET[1] + '/' + area + '/' + 'DailyFactor.csv', delimiter=',', skiprows=1)
    DF_D7 = np.loadtxt(Predict_DATE + '/' + list_TARGET[2] + '/' + area + '/' + 'DailyFactor.csv', delimiter=',', skiprows=1)
    DF_D6 = np.loadtxt(Predict_DATE + '/' + list_TARGET[3] + '/' + area + '/' + 'DailyFactor.csv', delimiter=',', skiprows=1)
    DF_D5 = np.loadtxt(Predict_DATE + '/' + list_TARGET[4] + '/' + area + '/' + 'DailyFactor.csv', delimiter=',', skiprows=1)
    DF_D4 = np.loadtxt(Predict_DATE + '/' + list_TARGET[5] + '/' + area + '/' + 'DailyFactor.csv', delimiter=',', skiprows=1)

    # 각 Factor별로 변수 할당
    Location = DF_D9[:, 0:2]
    swdir = np.c_[DF_D4[:, 2], DF_D5[:, 2], DF_D6[:, 2], DF_D7[:, 2], DF_D8[:, 2], DF_D9[:, 2]]
    ncpcp = np.c_[DF_D4[:, 3], DF_D5[:, 3], DF_D6[:, 3], DF_D7[:, 3], DF_D8[:, 3], DF_D9[:, 3]]
    wspd = np.c_[DF_D4[:, 4], DF_D5[:, 4], DF_D6[:, 4], DF_D7[:, 4], DF_D8[:, 4], DF_D9[:, 4]]
    wdir = np.c_[DF_D4[:, 5], DF_D5[:, 5], DF_D6[:, 5], DF_D7[:, 5], DF_D8[:, 5], DF_D9[:, 5]]
    atmp = np.c_[DF_D4[:, 6], DF_D5[:, 6], DF_D6[:, 6], DF_D7[:, 6], DF_D8[:, 6], DF_D9[:, 6]]
    stmp = np.c_[DF_D4[:, 7], DF_D5[:, 7], DF_D6[:, 7], DF_D7[:, 7], DF_D8[:, 7], DF_D9[:, 7]]

    # 기본 인자
    BasicFactor = np.c_[Location, swdir, ncpcp, wspd, wdir, atmp, stmp]
    BasicFactor2 =np.c_[Location, swdir, ncpcp, wspd, wdir, stmp] # 최종 입력자료에는 기온이 없음

    # 기본인자 출력
    np.savetxt(Predict_DATE + '/' + 'BasicFactor_' + area + '.csv',
              BasicFactor,
              delimiter=',',
              fmt='%3.4f',
              header='lat,lon,d4swdir,d5swdir,d6swdir,d7swdir,d8swdir,d9swdir,d4ncpcp,d5ncpcp,d6ncpcp,d7ncpcp,d8ncpcp,d9ncpcp,d4wspd,d5wspd,d6wspd,d7wspd,d8wspd,d9wspd,d4wdir,d5wdir,d6wdir,d7wdir,d8wdir,d9wdir,d4atmp,d5atmp,d6atmp,d7atmp,d8atmp,d9atmp,d4stmp,d5stmp,d6stmp,d7stmp,d8stmp,d9stmp',
              comments='')

    # 요약인자 & 파생인자
    # ADiff swdir : 일사량 평균 변화량
    diff_swdir1 = swdir[:, 1] - swdir[:, 0]
    diff_swdir2 = swdir[:, 2] - swdir[:, 1]
    diff_swdir3 = swdir[:, 3] - swdir[:, 2]
    diff_swdir4 = swdir[:, 4] - swdir[:, 3]
    diff_swdir5 = swdir[:, 5] - swdir[:, 4]
    diff_swdir = np.c_[diff_swdir1, diff_swdir2, diff_swdir3, diff_swdir4, diff_swdir5]
    adiff_swdir = np.mean(diff_swdir, axis=1)

    # ADiff stmp : 수온 평균 변화량
    diff_stmp1 = stmp[:, 1] - stmp[:, 0]
    diff_stmp2 = stmp[:, 2] - stmp[:, 1]
    diff_stmp3 = stmp[:, 3] - stmp[:, 2]
    diff_stmp4 = stmp[:, 4] - stmp[:, 3]
    diff_stmp5 = stmp[:, 5] - stmp[:, 4]
    diff_stmp = np.c_[diff_stmp1, diff_stmp2, diff_stmp3, diff_stmp4, diff_stmp5]
    adiff_stmp = np.mean(diff_stmp, axis=1)

    # S.A.D(Diff WA4 ~ 9) ; Sea Air Difference,해기차(해수온 - 기온)
    d4sad = stmp[:, 0] - atmp[:, 0]
    d5sad = stmp[:, 1] - atmp[:, 1]
    d6sad = stmp[:, 2] - atmp[:, 2]
    d7sad = stmp[:, 3] - atmp[:, 3]
    d8sad = stmp[:, 4] - atmp[:, 4]
    d9sad = stmp[:, 5] - atmp[:, 5]

    # max
    max_ncpcp = np.max(ncpcp, axis=1)
    max_swdir = np.max(swdir, axis=1)
    max_stmp = np.max(stmp, axis=1)
    max_wspd = np.max(wspd, axis=1)

    # min
    min_ncpcp = np.min(ncpcp, axis=1)
    min_swdir = np.min(swdir, axis=1)
    min_stmp = np.min(stmp, axis=1)
    min_wspd = np.min(wspd, axis=1)

    # mean
    mean_ncpcp = np.mean(ncpcp, axis=1)
    mean_swdir = np.mean(swdir, axis=1)
    mean_stmp = np.mean(stmp, axis=1)
    mean_wspd = np.mean(wspd, axis=1)

    # total
    total_ncpcp = np.sum(ncpcp, axis=1)
    total_swdir = np.sum(swdir, axis=1)
    total_stmp = np.sum(stmp, axis=1)

    # WCI
    wci = np.zeros((len(DF_D9), 6))
    for i in range(len(DF_D9)):

        # d4
        wci[i, 0] = (math.sqrt((100 * wspd[i, 0]) - wspd[i, 0] + 10.5)) * (33 - atmp[i, 0])
        # d5
        wci[i, 1] = (math.sqrt((100 * wspd[i, 1]) - wspd[i, 1] + 10.5)) * (33 - atmp[i, 1])
        # d6
        wci[i, 2] = (math.sqrt((100 * wspd[i, 2]) - wspd[i, 2] + 10.5)) * (33 - atmp[i, 2])
        # d7
        wci[i, 3] = (math.sqrt((100 * wspd[i, 3]) - wspd[i, 3] + 10.5)) * (33 - atmp[i, 3])
        # d8
        wci[i, 4] = (math.sqrt((100 * wspd[i, 4]) - wspd[i, 4] + 10.5)) * (33 - atmp[i, 4])
        # d9
        wci[i, 5] = (math.sqrt((100 * wspd[i, 5]) - wspd[i, 5] + 10.5)) * (33 - atmp[i, 5])

    # 요약인자 및 파생인자 Table
    AdditoryFactor = np.c_[adiff_swdir, adiff_stmp, d4sad, d5sad, d6sad, d7sad, d8sad, d9sad, max_ncpcp, max_swdir, max_stmp, max_wspd, min_ncpcp, min_swdir, min_stmp, min_wspd, mean_ncpcp, mean_swdir, mean_stmp, mean_wspd, total_ncpcp, total_swdir, total_stmp, wci]

    # 전체 Dataset : Input Dataset
    InputDataset = np.c_[BasicFactor2, AdditoryFactor]
    np.savetxt(Predict_DATE + '/' + 'InputDataset_' + area + '.csv',
               InputDataset,
               delimiter=',',
               fmt='%3.4f',
               header='lat,lon,d4swdir,d5swdir,d6swdir,d7swdir,d8swdir,d9swdir,d4ncpcp,d5ncpcp,d6ncpcp,d7ncpcp,d8ncpcp,d9ncpcp,d4wspd,d5wspd,d6wspd,d7wspd,d8wspd,d9wspd,d4wdir,d5wdir,d6wdir,d7wdir,d8wdir,d9wdir,d4stmp,d5stmp,d6stmp,d7stmp,d8stmp,d9stmp,adiff_swdir,adiff_stmp,d4sad,d5sad,d6sad,d7sad,d8sad,d9sad,max_ncpcp,max_swdir,max_stmp,max_wspd,min_ncpcp,min_swdir,min_stmp,min_wspd,mean_ncpcp,mean_swdir,mean_stmp,mean_wspd,total_ncpcp,total_swdir,total_stmp,wci4,wci5,wci6,wci7,wci8,wci9',
               comments='')

# Input Data 표준화
Ref = np.loadtxt('NeuralNet/Model7 2019_0616/Mean_Std.csv', delimiter=',', skiprows=1)

YS = np.loadtxt(Predict_DATE + '/' + 'InputDataset_YS.csv', delimiter=',', skiprows=1)
location_YS = YS[:, 0:2]
YS = YS[:, 2:]

for i in range(YS.shape[0]):

    for j in range(YS.shape[1]):

        YS[i, j] = (YS[i, j] - Ref[j, 0])/(Ref[j, 1])

YS = np.c_[location_YS, YS]

TYGJ = np.loadtxt(Predict_DATE + '/' + 'InputDataset_TYGJ.csv', delimiter=',', skiprows=1)
location_TYGJ = TYGJ[:, 0:2]
TYGJ = TYGJ[:, 2:]

for i in range(TYGJ.shape[0]):

    for j in range(TYGJ.shape[1]):

        TYGJ[i, j] = (TYGJ[i, j] - Ref[j, 0])/(Ref[j, 1])

TYGJ = np.c_[location_TYGJ, TYGJ]

np.savetxt(Predict_DATE + '/' + 'InputDataset_YS_s.csv', YS, delimiter=',', fmt='%3.4f',
          header='lat,lon,d4swdir,d5swdir,d6swdir,d7swdir,d8swdir,d9swdir,d4ncpcp,d5ncpcp,d6ncpcp,d7ncpcp,d8ncpcp,d9ncpcp,d4wspd,d5wspd,d6wspd,d7wspd,d8wspd,d9wspd,d4wdir,d5wdir,d6wdir,d7wdir,d8wdir,d9wdir,d4stmp,d5stmp,d6stmp,d7stmp,d8stmp,d9stmp,adiff_swdir,adiff_stmp,d4sad,d5sad,d6sad,d7sad,d8sad,d9sad,max_ncpcp,max_swdir,max_stmp,max_wspd,min_ncpcp,min_swdir,min_stmp,min_wspd,mean_ncpcp,mean_swdir,mean_stmp,mean_wspd,total_ncpcp,total_swdir,total_stmp,wci4,wci5,wci6,wci7,wci8,wci9',
          comments='')

np.savetxt(Predict_DATE + '/' + 'InputDataset_TYGJ_s.csv', TYGJ, delimiter=',', fmt='%3.4f',
          header='lat,lon,d4swdir,d5swdir,d6swdir,d7swdir,d8swdir,d9swdir,d4ncpcp,d5ncpcp,d6ncpcp,d7ncpcp,d8ncpcp,d9ncpcp,d4wspd,d5wspd,d6wspd,d7wspd,d8wspd,d9wspd,d4wdir,d5wdir,d6wdir,d7wdir,d8wdir,d9wdir,d4stmp,d5stmp,d6stmp,d7stmp,d8stmp,d9stmp,adiff_swdir,adiff_stmp,d4sad,d5sad,d6sad,d7sad,d8sad,d9sad,max_ncpcp,max_swdir,max_stmp,max_wspd,min_ncpcp,min_swdir,min_stmp,min_wspd,mean_ncpcp,mean_swdir,mean_stmp,mean_wspd,total_ncpcp,total_swdir,total_stmp,wci4,wci5,wci6,wci7,wci8,wci9',
          comments='')


# Step 4 : Prediction
area = ['YS', 'TYGJ']

# Load Data
D_YS = pd.read_csv(Predict_DATE + '/' + 'InputDataset_' + area[0] + '_s.csv')
D_TYGJ = pd.read_csv(Predict_DATE + '/' + 'InputDataset_' + area[1] + '_s.csv')

x_data_YS = D_YS[['d4swdir', 'd5swdir', 'd6swdir', 'd7swdir', 'd8swdir', 'd9swdir',
                  'd4ncpcp', 'd5ncpcp', 'd6ncpcp', 'd7ncpcp', 'd8ncpcp', 'd9ncpcp',
                  'd4wspd', 'd5wspd', 'd6wspd', 'd7wspd', 'd8wspd', 'd9wspd',
                  'd4wdir', 'd5wdir', 'd6wdir', 'd7wdir', 'd8wdir', 'd9wdir',
                  'd4stmp', 'd5stmp', 'd6stmp', 'd7stmp', 'd8stmp', 'd9stmp',
                  'adiff_swdir', 'adiff_stmp',
                  'd4sad', 'd5sad', 'd6sad', 'd7sad', 'd8sad', 'd9sad',
                  'max_ncpcp', 'max_swdir', 'max_stmp', 'max_wspd',
                  'min_ncpcp', 'min_swdir', 'min_stmp', 'min_wspd',
                  'mean_ncpcp', 'mean_swdir', 'mean_stmp', 'mean_wspd',
                  'total_ncpcp', 'total_swdir', 'total_stmp',
                  'wci4', 'wci5', 'wci6', 'wci7', 'wci8', 'wci9']]

x_data_TYGJ = D_TYGJ[['d4swdir', 'd5swdir', 'd6swdir', 'd7swdir', 'd8swdir', 'd9swdir',
                      'd4ncpcp', 'd5ncpcp', 'd6ncpcp', 'd7ncpcp', 'd8ncpcp', 'd9ncpcp',
                      'd4wspd', 'd5wspd', 'd6wspd', 'd7wspd', 'd8wspd', 'd9wspd',
                      'd4wdir', 'd5wdir', 'd6wdir', 'd7wdir', 'd8wdir', 'd9wdir',
                      'd4stmp', 'd5stmp', 'd6stmp', 'd7stmp', 'd8stmp', 'd9stmp',
                      'adiff_swdir', 'adiff_stmp',
                      'd4sad', 'd5sad', 'd6sad', 'd7sad', 'd8sad', 'd9sad',
                      'max_ncpcp', 'max_swdir', 'max_stmp', 'max_wspd',
                      'min_ncpcp', 'min_swdir', 'min_stmp', 'min_wspd',
                      'mean_ncpcp', 'mean_swdir', 'mean_stmp', 'mean_wspd',
                      'total_ncpcp', 'total_swdir', 'total_stmp',
                      'wci4', 'wci5', 'wci6', 'wci7', 'wci8', 'wci9']]

x_data_location_YS = D_YS[['lat', 'lon']]
x_data_location_TYGJ = D_TYGJ[['lat', 'lon']]

# Create Deep Neural Network Model(Multi-layer Neural Network)
n_node = 500
learning_rate = 1e-5
k_prob = 1.0

# Input layer
X = tf.placeholder(tf.float32, shape=[None, 59], name='X')
Y = tf.placeholder(tf.float32, shape=[None, 2], name='Y')

keep_prob = tf.placeholder(tf.float32)

# Hidden Layer1
W1 = tf.Variable(tf.random_normal([59, n_node], stddev=0.01), name='weight1')
b1 = tf.Variable(tf.random_normal([n_node], stddev=0.01), name='bias1')
layer1 = tf.nn.relu(tf.add(tf.matmul(X, W1), b1), name='layer1')
layer1 = tf.nn.dropout(layer1, keep_prob)

# Hidden Layer2
W2 = tf.Variable(tf.random_normal([n_node, n_node], stddev=0.01), name='weight2')
b2 = tf.Variable(tf.random_normal([n_node], stddev=0.01), name='bias2')
layer2 = tf.nn.relu(tf.add(tf.matmul(layer1, W2), b2), name='layer2')
layer2 = tf.nn.dropout(layer2, keep_prob)

# Hidden Layer3
W3 = tf.Variable(tf.random_normal([n_node, n_node], stddev=0.01), name='weight3')
b3 = tf.Variable(tf.random_normal([n_node], stddev=0.01), name='bias3')
layer3 = tf.nn.relu(tf.add(tf.matmul(layer2, W3), b3), name='layer3')
layer3 = tf.nn.dropout(layer3, keep_prob)

# Hidden Layer4
W4 = tf.Variable(tf.random_normal([n_node, n_node], stddev=0.01), name='weight4')
b4 = tf.Variable(tf.random_normal([n_node], stddev=0.01), name='bias4')
layer4 = tf.nn.relu(tf.add(tf.matmul(layer3, W4), b4), name='layer4')
layer4 = tf.nn.dropout(layer4, keep_prob)

# Output layer
W5 = tf.Variable(tf.random_normal([n_node, 2], stddev=0.01), name='weight5')
b5 = tf.Variable(tf.random_normal([2], stddev=0.01), name='bias5')
hypothesis = tf.add(tf.matmul(layer4, W5), b5)
output = tf.nn.softmax(hypothesis, name='output_layer')

# tf.train.Saver
saver = tf.train.Saver()

# Cost
cost_i = tf.nn.softmax_cross_entropy_with_logits_v2(logits=hypothesis, labels=Y)
cost = tf.reduce_mean(cost_i)
train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Predict
predict = tf.cast(output > 0.5, dtype=np.float32)
correct_prediction = tf.equal(tf.argmax(Y, axis=1), tf.argmax(output, axis=1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Run
with tf.Session() as sess:
    saver.restore(sess, 'NeuralNet/Model7 2019_0616/HAB_Prediction_2019_0616')

    p = tf.argmax(output, axis=1)
    result = sess.run(p, feed_dict={X: x_data_YS, keep_prob: k_prob})
    result = np.array(result, dtype=np.float32)

    h = sess.run(output, feed_dict={X: x_data_YS, keep_prob: k_prob})

r = np.c_[x_data_location_YS, h[:, 0]]

np.savetxt(Predict_DATE + '/' + area[0] + '_' + Predict_DATE + '00.csv', r,
           header='lat,lon,pred_result',
           delimiter=',',
           comments='',
           fmt='%3.4f')

with tf.Session() as sess:
    saver.restore(sess, 'NeuralNet/Model7 2019_0616/HAB_Prediction_2019_0616')

    p = tf.argmax(output, axis=1)
    result = sess.run(p, feed_dict={X: x_data_TYGJ, keep_prob: k_prob})
    result = np.array(result, dtype=np.float32)

    h = sess.run(output, feed_dict={X: x_data_TYGJ, keep_prob: k_prob})

r = np.c_[x_data_location_TYGJ, h[:, 0]]

np.savetxt(Predict_DATE + '/' + area[1] + '_' + Predict_DATE + '00.csv', r,
           header='lat,lon,pred_result',
           delimiter=',',
           comments='',
           fmt='%3.4f')
