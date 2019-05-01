
# coding: utf-8
import h5py
import numpy as np
import glob
import os

# 환경변수 설정
HOME_DIR = '/home/marinersgis/Redtide'
DATASET_DIR = HOME_DIR + '/DataSet'
RESULT_DIR = HOME_DIR + '/Result'
print('예보를 생산할 날짜(yyyymmdd)를 입력하시오 :')
RESULT_DATE = input()
print('자료(COMS_MI)의 날짜(yyyymmdd)를 입력하시오 :')
DATA_DATE = input()

# File list
files = DATASET_DIR + '/' + 'comsmile2sstcn' + DATA_DATE + '*.h5'
h5_list = glob.glob(files)

print(len(h5_list))

# Load MI Data
h5temp = h5py.File(h5_list[0]).get('Product').get('Sea_Surface_Temperature')
h5Tensor = np.zeros([len(h5_list), h5temp.shape[0], h5temp.shape[1]])

# Load Location Information
# Location_XY2.csv : MI SST 영상에서 추출해야할 영상 내 좌표(XY) 리스트
# TYGJ : 통영-거제 해역
# YS : 여수 해역
XY_TYGJ = np.loadtxt(DATASET_DIR + '/' + 'TYGJ_XY2.csv', delimiter=',')
XY_YS = np.loadtxt(DATASET_DIR + '/' + 'YS_XY2.csv', delimiter=',')

# Export Variables
# Column 1 : Lat
# Column 2 : Lon
# Column 3 : SST
# Output_Location : 출력시킬 변수
Output_TYGJ = np.zeros([XY_TYGJ.shape[0], 3])
Output_YS = np.zeros([XY_YS.shape[0], 3])

# Location_Coordinate.csv : 예보를 생산해야할 해역(Point)의 좌표(GCS ; 경위도) 목록
Coord_TYGJ = np.loadtxt(DATASET_DIR + '/' + 'TYGJ_Coordinate.csv', delimiter=',')
Coord_YS = np.loadtxt(DATASET_DIR + '/' + 'YS_Coordinate.csv', delimiter=',')
Output_TYGJ[:, 0] = Coord_TYGJ[:, 0]
Output_TYGJ[:, 1] = Coord_TYGJ[:, 1]
Output_YS[:, 0] = Coord_YS[:, 0]
Output_YS[:, 1] = Coord_YS[:, 1]

for i in range(len(h5_list)):
    
    h5File = h5py.File(h5_list[i], 'r').get('Product').get('Sea_Surface_Temperature')
    h5File = np.array(h5File)
    h5File = (h5File * 0.0411) - 5
    h5File[h5File > 1300] = np.nan
    h5Tensor[i, ] = h5File
    
    if i % 20 == 0:
        print('Complete %d files' % i)
        
h5mean = np.nanmean(h5Tensor, axis=0)
h5mean = np.transpose(h5mean)


# 통영-거제 해역 Target Point 추출
for i in range(XY_TYGJ.shape[0]):
    
    Output_TYGJ[i, 2] = h5mean[int(XY_TYGJ[i, 2]), int(XY_TYGJ[i, 3])]
    
# 여수 해역 Target Point 추출
for i in range(XY_YS.shape[0]):
    
    Output_YS[i, 2] = h5mean[int(XY_YS[i, 2]), int(XY_YS[i, 3])]

# Export를 위한 폴더 생성
os.mkdir(RESULT_DIR + '/' + RESULT_DATE + '/')
    
# csv로 Export
np.savetxt(RESULT_DIR + '/' + RESULT_DATE + '/' + 'MI_TYGJ.csv', Output_TYGJ, delimiter=',', fmt='%3.4f')
np.savetxt(RESULT_DIR + '/' + RESULT_DATE + '/' + 'MI_YS.csv', Output_YS, delimiter=',', fmt='%3.4f')

