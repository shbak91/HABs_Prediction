import glob
import os
import shutil
import numpy as np

# Path
DATASET_DIR = 'Merged_DB'
G1SST_DIR = 'G1SST_DB'

# Step 1 : LDAPS 폴더 리스트 생성(Merged_DB 폴더 내 미리 저장된 LDAPS 데이터 활용)
list_DIR = os.listdir(DATASET_DIR)

print(list_DIR)
print(len(list_DIR))

# Step 2 : LDAPS 폴더 이름을 읽어들여 같은 폴더를 가진 G1SST 폴더 찾기
for i in list_DIR:
    
    # Step 2-1 : 폴더와 그외 구분
    # 폴더는 이름이 '201'로 시작
    if i[0:3] == '201':
        
        print(i)
        
        # Step 2-2 : Merged_DB 폴더 내 list_DIR 내 폴더 리스트 만들기
        list_DIR_MergedDB = os.listdir('Merged_DB' + '/' + i)
        list_DIR_G1SST = os.listdir('G1SST_DB' + '/' + i)
        
        print(list_DIR_MergedDB)
        print(list_DIR_G1SST)
        
        # Step 2-3 : 폴더 리스트 내 이름이 '201'로 시작하는 폴더에 있는 파일을 읽어 들여 같은 이름 폴더로 복사
        for j in list_DIR_G1SST:
            
            if j[0:3] == '201':
                
                SST_file = 'G1SST_DB' + '/' + i + '/' + j + '/' + 'SST_' + j + '.csv'
                Copy_DIR = 'Merged_DB' + '/' + i + '/' + j
                shutil.copy(SST_file, Copy_DIR)
