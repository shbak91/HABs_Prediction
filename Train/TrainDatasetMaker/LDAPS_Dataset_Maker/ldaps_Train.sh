#!/bin/bash

# 인자수 확인
if [ $# -ne 3 ]
then
    echo "Usage: $0 [Target Date(yyyymmdd)] [index(00, 03, 06, ... , 21)] [Result Date(yyyymmdd)]"
    exit 0
fi

# 환경변수
TARGET_DATE=$1
IDX=$2
RESULT_DATE=$3
KWGRIB2=/home/marinersgis/Redtide/kwgrib2/bin/kwgrib2
HOME_DIR=/home/marinersgis
DATA_DIR=$HOME_DIR/Data/LDAPS/2013/$TARGET_DATE
LOCATION_DIR=$HOME_DIR/Redtide/TrainDB/location
RESULT_DIR=$HOME_DIR/Redtide/TrainDB
LOG_DIR=$HOME_DIR/Redtide/TrainDB/Log

# 시작
start_time=$(date +%s.%N)

# LDAPS 데이터 추출 및 저장
# 날짜별-인덱스별 관심영역의 기본인자(강수량, 일사량, V값, U값, 기온) 추출
IFS=","
while read lat lon
do
    SWDIR=$($KWGRIB2 -lon $lon $lat $DATA_DIR/l015v070erlounish000.$TARGET_DATE$IDX.gb2 -d 2)
    NCPCP=$($KWGRIB2 -lon $lon $lat $DATA_DIR/l015v070erlounish000.$TARGET_DATE$IDX.gb2 -d 8)
    UGRD=$($KWGRIB2 -lon $lon $lat $DATA_DIR/l015v070erlounish000.$TARGET_DATE$IDX.gb2 -d 15)
    VGRD=$($KWGRIB2 -lon $lon $lat $DATA_DIR/l015v070erlounish000.$TARGET_DATE$IDX.gb2 -d 16)
    TMP=$($KWGRIB2 -lon $lon $lat $DATA_DIR/l015v070erlounish000.$TARGET_DATE$IDX.gb2 -d 21)

    echo ${SWDIR#*val=},${NCPCP#*val=},${UGRD#*val=},${VGRD#*val=},${TMP#*val=},$lat,$lon >> $RESULT_DIR/$RESULT_DATE/$TARGET_DATE/ldaps_$IDX.csv
done < $LOCATION_DIR/$RESULT_DATE.csv

# 종료
end_time=$(date +%s.%N)

# 실행시간 확인
elapsed_time=$(echo "$end_time - $start_time" | bc)
htime=$(echo "$elapsed_time/3600" | bc)
mtime=$(echo "($elapsed_time/60) - ($htime * 60)" | bc)
stime=$(echo "$elapsed_time-(($elapsed_time/60) * 60)" | bc)
echo "ldaps_$IDX.csv : ${htime}H ${mtime}M ${stime}S" >> $LOG_DIR/$RESULT_DATE.log
echo "[LDAPS-YS] - l015v070erlounish000.${TARGET_DATE}${IDX}.gb2 추출완료" >> $LOG_DIR/$RESULT_DATE.log
echo "" >> $LOG_DIR/$RESULT_DATE.log


