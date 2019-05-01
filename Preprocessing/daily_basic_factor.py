
# coding: utf-8

# In[117]:


import os
import glob
import numpy as np
import math


# In[118]:


# Path
HOME_DIR = 'e:'
DATASET_DIR = HOME_DIR + '/Daily'

# print('Daily Data를 생산할 폴더 이름(yyyymmdd)을 입력하시오 : ')
#RESULT_DATE = input()
RESULT_DATE = '20190402'


# In[119]:


# Load Raw Data 
# 통영-거제 해역
# LDAPS File List 생성
ldaps_ty = DATASET_DIR + '/' + RESULT_DATE + '/' + 'TYGJ' + '/'+ 'ldaps_' + '*.csv'
ldaps_list_ty = glob.glob(ldaps_ty)

# MI
mi_ty = np.loadtxt(DATASET_DIR + '/' + RESULT_DATE + '/' + 'TYGJ' + '/' + 'MI_TYGJ.csv', delimiter=',')
mi_ty = mi_ty[:, -1]

# 여수 해역
# LDAPS File list 생성
ldaps_ys = DATASET_DIR + '/' + RESULT_DATE + '/' + 'YS' + '/' + 'ldaps_' + '*.csv'
ldaps_list_ys = glob.glob(ldaps_ys)

# MI
mi_ys = np.loadtxt(DATASET_DIR + '/' + RESULT_DATE + '/' + 'YS' + '/' + 'MI_YS.csv', delimiter=',')
mi_ys = mi_ys[:, -1]


# In[122]:


# csv 파일을 순차적으로 불러와서  요소(Component)별 변수 할당
# 통영-거제 해역
temp_csv = np.loadtxt(ldaps_list_ty[0], delimiter=',')

# Location Info.
location_ty = temp_csv[:, 5:7]

temp_SWDIR = np.zeros((temp_csv.shape[0], len(ldaps_list_ty)))
temp_NCPCP = np.zeros((temp_csv.shape[0], len(ldaps_list_ty)))
temp_UGRD = np.zeros((temp_csv.shape[0], len(ldaps_list_ty)))
temp_VGRD = np.zeros((temp_csv.shape[0], len(ldaps_list_ty)))
temp_TMP = np.zeros((temp_csv.shape[0], len(ldaps_list_ty)))

# 일 데이터 병합
for i in range(len(ldaps_list_ty)):
    temp_csv = np.loadtxt(ldaps_list_ty[i], delimiter=',')
    
    # col1 : SWDIR(일사량)
    # col2 : NCPCP(강수량)
    # col3 : UGRD(U)
    # col4 : VGRD(V)
    # col5 : TMP(Air Temperature)
    temp_SWDIR[:, i] = temp_csv[:, 0]
    temp_NCPCP[:, i] = temp_csv[:, 1]
    temp_UGRD[:, i] = temp_csv[:, 2]
    temp_VGRD[:, i] = temp_csv[:, 3]
    temp_TMP[:, i] = temp_csv[:, 4]
    
# 요소별 합성 후 일일 데이터 생산
# SWDIR 일사량 - 일평균
SWDIR = np.mean(temp_SWDIR, axis=1)
# NCPCP 강수량  - 1시간 평균 * 24
NCPCP = np.mean(temp_NCPCP, axis=1) * 24
# WSPEED 풍속 - sqrt(U평균 제곱 + V평균 제곱)
UGRD = np.mean(temp_UGRD, axis=1)
VGRD = np.mean(temp_VGRD, axis=1)

WSPD = np.zeros([UGRD.shape[0], 1])
for i in range(len(UGRD)):
    WSPD[i] = math.sqrt((UGRD[i] * UGRD[i]) + (VGRD[i] * VGRD[i]))
    
# WDIR 풍향
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
ATMP = np.mean(temp_TMP, axis=1)
        
# 통합
TY = np.c_[location_ty, SWDIR, NCPCP, WSPD, WDIR, ATMP, mi_ty]

# export csv
np.savetxt(DATASET_DIR + '/' + RESULT_DATE + '/' + 'TYGJ' + '/' + 'DailyFactor_TYGJ.csv', 
           TY, delimiter=',', fmt='%3.4f',
          header='lat, lon, swdir, ncpcp, wspd, wdir, atmp, stmp',
          comments='')

# 여수 해역
temp_csv = np.loadtxt(ldaps_list_ys[0], delimiter=',')

# Location Info.
location_ys = temp_csv[:, 5:7]

temp_SWDIR = np.zeros((temp_csv.shape[0], len(ldaps_list_ys)))
temp_NCPCP = np.zeros((temp_csv.shape[0], len(ldaps_list_ys)))
temp_UGRD = np.zeros((temp_csv.shape[0], len(ldaps_list_ys)))
temp_VGRD = np.zeros((temp_csv.shape[0], len(ldaps_list_ys)))
temp_TMP = np.zeros((temp_csv.shape[0], len(ldaps_list_ys)))

# 일 데이터 병합
for i in range(len(ldaps_list_ys)):
    temp_csv = np.loadtxt(ldaps_list_ys[i], delimiter=',')
    
    # col1 : SWDIR(일사량)
    # col2 : NCPCP(강수량)
    # col3 : UGRD(U)
    # col4 : VGRD(V)
    # col5 : TMP(Air Temperature)
    temp_SWDIR[:, i] = temp_csv[:, 0]
    temp_NCPCP[:, i] = temp_csv[:, 1]
    temp_UGRD[:, i] = temp_csv[:, 2]
    temp_VGRD[:, i] = temp_csv[:, 3]
    temp_TMP[:, i] = temp_csv[:, 4]
    
# 요소별 합성 후 일일 데이터 생산
# SWDIR 일사량 - 일평균
SWDIR = np.mean(temp_SWDIR, axis=1)
# NCPCP 강수량  - 1시간 평균 * 24
NCPCP = np.mean(temp_NCPCP, axis=1) * 24
# WSPEED 풍속 - sqrt(U평균 제곱 + V평균 제곱)
UGRD = np.mean(temp_UGRD, axis=1)
VGRD = np.mean(temp_VGRD, axis=1)

WSPD = np.zeros([UGRD.shape[0], 1])
for i in range(len(UGRD)):
    WSPD[i] = math.sqrt((UGRD[i] * UGRD[i]) + (VGRD[i] * VGRD[i]))
    
# WDIR 풍향
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
ATMP = np.mean(temp_TMP, axis=1)
        
# 통합
YS = np.c_[location_ys, SWDIR, NCPCP, WSPD, WDIR, ATMP, mi_ys]

# export csv
np.savetxt(DATASET_DIR + '/' + RESULT_DATE + '/' + 'YS' + '/' + 'DailyFactor_YS.csv', 
           YS, delimiter=',', fmt='%3.4f',
          header='lat, lon, swdir, ncpcp, wspd, wdir, atmp, stmp',
          comments='')

