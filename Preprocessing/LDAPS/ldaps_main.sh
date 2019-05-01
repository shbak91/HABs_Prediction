#!/bin/bash

# 인자수 확인
if [ $# -ne 2 ]
then
    echo "Usage: $0 [Target Date(yyyymmdd)] [Result Date(yyyymmdd)]"
    exit 0
fi

# 환경변수
HOME_DIR=/home/marinersgis/Redtide
DATA_DIR=$HOME_DIR/DataSet
RESULT_DIR=$HOME_DIR/Result
LOG_DIR=$HOME_DIR/Log
TARGET_DATE=$1
RESULT_DATE=$2



# TYGJ LDAPS 데이터 생성
echo "[$RESULT_DATE] ldaps_TYGJ.sh" >> $LOG_DIR/$RESULT_DATE.log
echo "" >> $LOG_DIR/$RESULT_DATE.log

# 결과 디렉토리 생성
if [ ! -d $RESULT_DIR/$RESULT_DATE/TYGJ ]
then
    mkdir -p $RESULT_DIR/$RESULT_DATE/TYGJ
    echo "[${RESULT_DATE}-TYGJ] 디렉토리 생성" >> $LOG_DIR/$RESULT_DATE.log
    echo "" >> $LOG_DIR/$RESULT_DATE.log
fi

# 파일 존재 유무를 확인하고, LDAPS 데이터 전처리
for IDX in 00 03 06 09 12 15 18 21
do
    if [ -e $DATA_DIR/l015v070erlounish000.$TARGET_DATE$IDX.gb2 ]; then
        sh $HOME_DIR/ldaps_TYGJ.sh $TARGET_DATE $IDX $RESULT_DATE &
    else
        echo "[ERROR] $TARGET_DATE - l015v070erlounish000.$TARGET_DATE$IDX.gb2 파일이 존재하지 않습니다."
    fi
done




# 통영-거제해역 처리 Waiting (3분)
sleep 3m


# YS LDAPS 데이터 생성
echo "[$RESULT_DATE] ldaps_YS.sh" >> $LOG_DIR/$RESULT_DATE.log
echo "" >> $LOG_DIR/$RESULT_DATE.log

# 결과 디렉토리 생성
if [ ! -d $RESULT_DIR/$RESULT_DATE/YS ]
then
    mkdir -p $RESULT_DIR/$RESULT_DATE/YS 
    echo "[${RESULT_DATE}-YS] 디렉토리 생성" >> $LOG_DIR/$RESULT_DATE.log
    echo "" >> $LOG_DIR/$RESULT_DATE.log
fi

# 파일 존재 유무를 확인하고, LDAPS 데이터 전처리 수행
for IDX in 00 03 06 09 12 15 18 21
do
    if [ -e $DATA_DIR/l015v070erlounish000.$TARGET_DATE$IDX.gb2 ]; then
        sh $HOME_DIR/ldaps_YS.sh $TARGET_DATE $IDX $RESULT_DATE &
    else
        echo "[ERROR] $TARGET_DATE - l015v070erlounish000.$TARGET_DATE$IDX.gb2 파일이 존재하지 않습니다."
    fi
done


