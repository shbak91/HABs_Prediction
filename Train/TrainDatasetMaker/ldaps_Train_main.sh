#!/bin/bash

# 사용자가 입력한 인자 확인
# 입력한 인자가 2개가 아닌 경우 프로그램 종료
if [ $# -ne 2 ]
then
    echo "Usage: $0 [Target Date(yyyymmdd)] [Result Date(yyyymmdd)]"
    exit 0
fi

# 경로설정(환경변수)
TARGET_DATE=$1
RESULT_DATE=$2
HOME_DIR=/home/marinersgis
DATA_DIR=$HOME_DIR/Data/LDAPS/2013/$TARGET_DATE
RESULT_DIR=$HOME_DIR/Redtide/TrainDB
LOG_DIR=$HOME_DIR/Redtide/TrainDB/Log

# LDAPS 데이터 생성
echo "[$RESULT_DATE] ldaps_Train.sh" >> $LOG_DIR/$RESULT_DATE.log
echo "" >> $LOG_DIR/$RESULT_DATE.log

# 결과 디렉토리 생성
if [ ! -d $RESULT_DIR/$RESULT_DATE/$TARGET_DATE ]
then
    mkdir -p $RESULT_DIR/$RESULT_DATE/$TARGET_DATE
    echo "[${RESULT_DATE}-$TARGET_DATE] 디렉토리 생성" >> $LOG_DIR/$RESULT_DATE.log
    echo "" >> $LOG_DIR/$RESULT_DATE.log
fi

# 파일 존재 유무를 확인하고, LDAPS 데이터 전처리
for IDX in 00 03 06 09 12 15 18 21
do
    if [ -e $DATA_DIR/l015v070erlounish000.$TARGET_DATE$IDX.gb2 ]; then
        sh $HOME_DIR/Redtide/ldaps_Train.sh $TARGET_DATE $IDX $RESULT_DATE &
    else
        echo "[ERROR] $TARGET_DATE - l015v070erlounish000.$TARGET_DATE$IDX.gb2 파일이 존재하지 않습니다."
    fi
done

# Data 생산시간 : 약 1분
sleep 1m
