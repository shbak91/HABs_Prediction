# G1SST Dataset Maker
# v1.1 2019_0527
# S.H.Bak

import glob
import numpy as np
import h5py
import math
import os
import datetime

# User Define Function 
# h5 Loader
def load_h5(fid, attr_id):

    h5File = h5py.File(fid, 'r')
    h5 = np.array(h5File.get('HDFEOS').get('GRIDS').get('Image Data').get('Data Fields').get(attr_id))

    return(h5)

# 거리 계산 함수
def dist(x1, x2, y1, y2):

    d = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))

    return(d)

# Step 0 : 날짜 정보 입력

# 적조 발생일 리스트 생성
REDTIDE_DIR = 'Location'
REDTIDE_CSV = REDTIDE_DIR + '/' + '*.csv'
REDTIDE_LIST = glob.glob(REDTIDE_CSV)

for i in REDTIDE_LIST:
    
    temp_REDTIDE_DATE = i[9:-4] # 적조 발생일
    
    REDTIDE_DATE = temp_REDTIDE_DATE[0:4] + temp_REDTIDE_DATE[5:9]
    
    # 사용자에게 입력받은 적조 발생일(String)을 날짜 형식으로 변환(datetime)
    REDTIDE_DATE = datetime.datetime.strptime(REDTIDE_DATE, '%Y%m%d')

    # SST DATE : 추출할 SST 날짜
    # SST DATE를 저장할 공간 생성
    SST_DATE = np.zeros((6,1))

    # SST DATE 자동 생성(D-9 ~ D-4)
    for i in range(6):

        temp_date =REDTIDE_DATE + datetime.timedelta(days = (i - 9) )

        SST_DATE[i] = datetime.datetime.strftime(temp_date, '%Y%m%d')

    # 날짜 형식의 적조 발생일을 다시 문자열로 변환
    REDTIDE_DATE = datetime.datetime.strftime(REDTIDE_DATE, '%Y%m%d')
    
    for i in SST_DATE:

        # Step 1 : 적조 발생 위치 정보 불러오기
        # 사용자에게 적조 발생일을 입력받음(yyyymmdd)
        # REDTIDE_DATE = input()

        SST_DATE = str(i)
        SST_DATE = SST_DATE[1:9]

        # 입력받은 발생일에 해당하는 csv 파일명 생성(yyyy_mmdd.csv)
        REDTIDE_DIR = 'Location'
        REDTIDE_CSV = REDTIDE_DIR + '/' + REDTIDE_DATE[0:4] + '_' + REDTIDE_DATE[4:9] + '.csv'

        # csv 파일 불러오기
        R_Location = np.loadtxt(REDTIDE_CSV, delimiter=',')

        # 결과를 저장할 폴더 생성
        if os.path.isdir('REDTIDE_SST' + '/' + REDTIDE_DATE) is False:

            os.mkdir('REDTIDE_SST' + '/' + REDTIDE_DATE)
        
        # Step 2 : G1SST 불러오기
        # 사용자에게 SST를 추출할 날짜 정보 입력받기(yyyymmdd)
        # SST_DATE = input()

        # 입력받은 발생일에 해당하는 he5 파일명 생성(SST_yyyymmdd000000.he5_area.he5)
        SST_DIR = 'G1SST(Red Tide Period)'
        SST_file = SST_DIR + '/' + 'SST_' + SST_DATE + '000000.he5_area.he5'

        # he5 파일에서 SST 읽어오기
        SST = load_h5(SST_file, 'SST Image Pixel Values')
        
        # Step 3 : G1SST의 Lat/Lon 파일 불러오기
        coord = 'coord' + '/' + '*.he5'
        coord_list = glob.glob(coord)

        lat = load_h5(coord_list[0], 'Latitude Image Pixel Values')
        lon = load_h5(coord_list[1], 'Longitude Image Pixel Values')
        
        # Step 4 : G1SST & Lat/Lon Table 생성
        # Reshape
        SST = SST.reshape(-1, 1)
        lat = lat.reshape(-1, 1)
        lon = lon.reshape(-1, 1)

        # Table
        table = np.c_[lat, lon, SST]

        # Table에 저장된 SST 중에서 -999인 자료 제거
        table = table[table[:, 2] > 0]

        # Step 5 : 적조 발생 위치를 순차적으로 읽어들여 거리를 구한 다음 가장 가까운 픽셀의 SST 탐색

        # R_Location과 가장 가까운 SST 추출
        # output : 출력시킬 데이터
        # output[:, 0] : Lat
        # output[:, 1] : Lon
        # output[:, 2] : close sst
        temp_sst = np.zeros((len(R_Location), 1))
        output = np.c_[R_Location, temp_sst]

        for i in range(len(R_Location)):

            # R_Location과 SST(table)의 거리 계산
            d = np.zeros(len(table))

            for j in range(len(table)):

                d[j] = dist(R_Location[i, 0], table[j, 0], R_Location[i, 1], table[j, 1])

            # d(거리)에 저장된 거리 중 가장 작은 값이 존재하는 위치(min_location)
            min_location = np.where(d == np.min(d))

            close_sst = table[min_location, 2]

            output[i, 2] = close_sst

        # Step 6 : Export
        # 결과를 저장할 폴더 생성
        SST_SAVE_DIR = 'REDTIDE_SST' + '/' + REDTIDE_DATE + '/' + SST_DATE
        os.mkdir(SST_SAVE_DIR)

        fid = SST_SAVE_DIR + '/' + 'SST_' + SST_DATE + '.csv'
        np.savetxt(fid, output, delimiter=',', fmt='%3.4f')

