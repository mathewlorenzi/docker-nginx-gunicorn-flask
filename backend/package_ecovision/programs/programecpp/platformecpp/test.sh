#! /bin/bash 
# for c++
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../../../build/lib 
export LD_LIBRARY_PATH

# HOST=$1
PORT=$1
CAMID=$2

# if [ "$HOST" == "" ]; then
#     echo "host as first arg not provided"
#     exit 1
# fi
if [ "$PORT" == "" ]; then
    echo "port as first arg not provided"
    exit 1
fi
if [ "$CAMID" == "" ]; then
    echo "camid as second arg not provided"
    exit 1
fi

./../../../build/bin/platformecpp -subsize 0 -control control2d.txt -create_tcp_server -camidname $CAMID -port $PORT -motionwindow 2 -context2dec LOCAL -fantagaugedim 70 -httpPostGet_waitIntervalBeforeRetrying 1
#./../../../build/bin/platformecpp -subsize 0 -control control2d.txt -http_client_to_flask_server -camidname $CAMID -host $HOST -port $PORT -motionwindow 2 -context2dec LOCAL -fantagaugedim 70 -httpPostGet_waitIntervalBeforeRetrying 1
#./../../../build/bin/platformecpp -subsize 0 -control control2d.txt -http_client_to_flask_server -camidname paulo9 -host https://www.ecovision.ovh -port 81 -motionwindow 2 -context2dec LOCAL -fantagaugedim 70 httpPostGet_waitIntervalBeforeRetrying 10
#./../../../build/bin/platformecpp -subsize 0 -control control2d.txt -lcsmainfolder -directory /home/ecorvee/data/LCS-videos/database1/ -lcsvideoindex 33 -startat 1 -incrementvideoindex 10 -motionwindow 2  -context2dec LOCAL -fantagaugedim 70 

# ====================


#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/local/home/ecorvee/project/opencv-2.4.8/build/lib
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/inria/3party/lib

# in test_camera/gpio now ./../../build/bin/platformecpp --simul_ov7670 -subsize 0 -directory /home/ecorvee/data-fantastic/ -startstamp5 2016 9 27 11 16 -stopstamp6 2016 9 27 11 21 49 

#./../../build/bin/platformecpp --GRAB /dev/video1
#./../../build/bin/platformecpp --testcalibgt
#./../../build/bin/platformecpp --test_stereo_ground_zone
#./../../build/bin/platformecpp --test_disparity /user/ecorvee/home/data-fantastic/stereo/b08/2016-09-14/19h/20mn/2016-09-14T19:20:26.594000.jpg /user/ecorvee/home/data-fantastic/stereo/b08/2016-09-14/19h/20mn/2016-09-14T19:20:31.889000.jpg
##./../../build/bin/platformecpp --test_disparity /user/ecorvee/home/data-fantastic/stereo/b08/2016-09-14/19h/20mn/2016-09-14T19:20:26.594000.jpg /user/ecorvee/home/data-fantastic/stereo/b08/2016-09-14/19h/20mn/2016-09-14T19:20:27.837000.jpg
#./../../build/bin/platformecpp --test_disparity /user/ecorvee/home/data-fantastic/stereo/b08/cam1-b-2016-09-20T18:23:18.422000.jpg /user/ecorvee/home/data-fantastic/stereo/b08/cam2-b-2016-09-20T18:23:18.473000.jpg
#./../../build/bin/platformecpp --test_disparity /user/ecorvee/home/data-fantastic/stereo/b08/cam1.jpg /user/ecorvee/home/data-fantastic/stereo/b08/cam2.jpg
#./../../build/bin/platformecpp --test_disparity /user/ecorvee/home/data-fantastic/stereo/test1.jpg /user/ecorvee/home/data-fantastic/stereo/test2.jpg

#board1 (USE_AUTOCALIB2D 1 and no smoothing please)
#./../../build/bin/platformecpp -control control2d.txt -recorded2d -subsize 0 -directory -directory /user/ecorvee/home/data-fantastic/calib_pattern/ -stamp -width 320 -height 240 -autocalib_output_filename ../../datafiles/auto_board_calib/calib_board1_fanta_home_2016_03_11_view1.txt

#./../../build/bin/platformecpp /user/ecorvee/home/data/LCS-videos/database1/20-LIGHTOFF_IRON_FALL1_demo/00000006.jpg
#./../../build/bin/platformecpp /user/ecorvee/home/temp/2016_01_25_16_54_59_picture_000000002.jpg

#simul cam1 - simul fswebcam
##./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo  -directory /home/ecorvee/data-fantastic/stereo-fall-b09/cam1/ -startstamp5 2016 2 12 20 31 -stopstamp5 2016 2 12 20 33 -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/stereo-fall-b09-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 2 -host 127.0.0.1 -port 3001 -step
# start 2016 5 15 23 19

# - home -
#./../../build/bin/platformecpp -stampfoldervideo -directory /home/ecorvee/data-fantastic/ -startstamp5 2016 5 15 23 22 -stopstamp6 2016 5 15 23 34 5  -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/stereo-fall-b09-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 20 -host 127.0.0.1 -port 3001 -fantagaugedim 70
# girls -startstamp5 2016 9 26 17 23 -stopstamp6 2016 9 26 17 30 25 
###./../../build/bin/platformecpp -stampfoldervideo -directory /home/ecorvee/data-fantastic/ -startstamp5 2016 9 27 11 16 -stopstamp6 2016 9 27 11 21 49 -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/home_entrance/mcc-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 20 -host 127.0.0.1 -port 3001 -fantagaugedim 70 -dzt_inputfilename ../../datafiles/drawing_zones_tool/home_entrance/dzt.txt
#-step
#-startstamp5 2016 5 15 23 19

#V1./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo  -directory /home/ecorvee/data-fantastic/ -startstamp5 2016 5 15 23 19 -stopstamp6 2016 5 15 23 34 5  -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/stereo-fall-b09-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 2 -host 127.0.0.1 -port 3001 -step
#-startstamp5 2016 5 15 23 19 -stopstamp6 2016 5 15 23 34 5
#-startstamp5 2016 5 15 23 32
#23 33 problem
#-startstamp5 2016 6 5 11 19 -stopstamp5 2016 6 5 11 23

# ---------- home -------------
##./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo -directory /home/ecorvee/data-fantastic/ -startstamp5 2016 5 30 11 55 -stopstamp4 2016 5 30 12 -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/fanta-stereo-home-salon/mcc-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 20 -host 127.0.0.1 -port 3001 -dzt_inputfilename ../../datafiles/drawing_zones_tool/dzt_fanta_home_fall.txt -fantagaugedim 70 
#-step


################## last prog used before nexguard

#-startstamp5 2016 9 1 17 40 
##./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo -directory /home/ecorvee/data-fantastic/ -startstamp5 2016 9 1 17 40 -stopstamp4 2016 9 1 18 -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/fanta-stereo-home-salon/mcc-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 20 -host 127.0.0.1 -port 3001 -fantagaugedim 50 
#-step

# ----- b08 ----- -startstamp5 2016 8 30 17 30  -startstamp6 2016 8 30 17 31 43 for fall along
##./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo -directory /home/ecorvee/data-fantastic/b08 -startstamp5 2016 8 30 17 30 -stopstamp4 2016 8 30 18 -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/b08/mcc-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 20 -host 127.0.0.1 -port 3001 -dzt_inputfilename ../../datafiles/drawing_zones_tool/b08.txt -fantagaugedim 70 -step

# ----- moving b08 ----- 
##./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo -directory /home/ecorvee/data-fantastic/stereo/b08/ -startstamp5 2016 9 14 19 20 -stopstamp4 2016 9 14 20 -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/b08/mcc-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 20 -host 127.0.0.1 -port 3001 -dzt_inputfilename ../../datafiles/drawing_zones_tool/b08.txt -fantagaugedim 70 
#--SIMULCAM2D 

# b09 cam1/cam2 - TODO recalibrate
#./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo -directory /home/ecorvee/data-fantastic/stereo-fall3-b09/cam1/ -startstamp5 2016 2 24 17 46 -stopstamp5 2016 2 24 17 48 -subsize 0 -control control2d.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 2 -host 127.0.0.1 -port 3001 -context2dvanish ../../datafiles/multi_cam_calib/stereo-fall2-b09/stereo-fall2-b09-results-inputs.txt 

#cam1/cam2
#./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo -directory /home/ecorvee/data-fantastic/stereo-fall2-b09/cam1/ -startstamp5 2016 2 22 20 57 -stopstamp4 2016 2 22 21 -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/stereo-fall2-b09/stereo-fall2-b09-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 2 -host 127.0.0.1 -port 3001 
#./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo -directory /home/ecorvee/data-fantastic/stereo-fall2-b09/cam2/ -startstamp5 2016 2 22 14 57 -stopstamp4 2016 2 22 16 -subsize 0 -control control2d.txt -context2dvanish ../../datafiles/multi_cam_calib/stereo-fall2-b09/stereo-fall2-b09-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 2 -host 127.0.0.1 -port 3001  
#./../../build/bin/platformecpp --SIMULCAM2D -stampfoldervideo -directory /home/ecorvee/data-fantastic/stereo-fall2-b09/cam1/ -subsize 0 -control control2d.txt -context2dRscan ../../datafiles/multi_cam_calib/stereo-fall2-b09/stereo-fall2-b09-results-inputs.txt -vanish_or_Rscan_from_mcc_indexcam 0  -write_stamp_folders_dir /home/ecorvee/temp/ -motionwindow 2 -host 127.0.0.1 -port 3001 -step
# .......................-context2dvanish
# .......................-context2dRscan

#./../../build/bin/platformecpp -control control2d.txt -recorded2d -subsize 0 -directory -directory /user/ecorvee/home/workspace_new/ecplatform/ferchau/ -stem car -nbdigit 1 -startat 1 -step -width 320 -height 240

# axis
#./../../build/bin/platformecpp -control control2d.txt -stream2d http://192.168.0.90/view/index.shtml -motionwindow 2 -host 127.0.0.1 -port 3001 -step

# --- LCS --- 2D videos, 33, 4 (5)6, - 10,11,12 - 21,22  (19,1,ghost) (4,switch on light)
#./../../build/bin/platformecpp --TEST_FOLDER_STAMPS
#./../../../build/bin/platformecpp -subsize 0 -control control2d.txt -lcsmainfolder -directory /home/ecorvee/data/LCS-videos/database1/ -lcsvideoindex 33 -startat 1 -incrementvideoindex 1 -motionwindow 2  -context2dec LOCAL -fantagaugedim 70
#-step
#-host 127.0.0.1 -port 3001 -step
#-bed LOCALBED

# --- databases ---
#./../../build/bin/platformecpp -subsize 0 -control control2d.txt -recorded2d -directory /user/ecorvee/home/data/pedestrians128x64/ -startat 1 -ext jpg -nbdigit 5 -step
#./../../build/bin/platformecpp -subsize 0 -control control2d.txt -recorded2d -directory /user/ecorvee/home/data/PennFudanPed/output/ -startat 0 -ext jpg -nbdigit 5 -step
#./../../build/bin/platformecpp -subsize 0 -control control2d.txt -recorded2d -directory /user/ecorvee/home/data/PennFudanPed/output-ppm/ -startat 1 -stem head -ext ppm -nbdigit 5 -step
##./../../build/bin/platformecpp -subsize 0 -control control2d.txt -recorded2d -directory /user/ecorvee/home/data/heads-32x32/ -startat 0 -stem image -ext jpg -nbdigit 6 -step

#./../../build/bin/libecc_main  -control control2d.txt -cam3dtype kinect2 -recorded3d -directory /home/ecorvee/kinect2data/maison/ -start_year 2015 -start_month 11 -start_day 9 -start_hour 18 -start_minute 20 -stop_year 2015 -stop_month 11 -stop_day 9 -stop_hour 19

#./../../build/bin/libecc_main  -halfsize -control control2d.txt -cam3dtype kinect2 -recorded3d -directory /home/ecorvee/kinect2data/athome_norgb/ -start_year 2015 -start_month 10 -start_day 28 -start_hour 10 -start_minute 12 -stop_year 2015 -stop_month 10 -stop_day 29 -stop_hour 1

#./../../build/bin/libecc_main -halfsize -control control2d.txt -cam3dtype asus -recorded3d -version 3sup -directory /user/ecorvee/home/ICP/asusdata_room/ -start_year 2015 -start_month 7 -start_day 27 -start_hour 10 -start_minute 48 -stop_year 2015 -stop_month 7 -stop_day 27 -stop_hour 11 

# CERTH
#./../../build/bin/libecc_main -control control3d.txt -recorded3d -cam3dtype asus -version 3sup -directory /user/ecorvee/home/CERTH/asusdata3/ -start_year 2015 -start_month 3 -start_day 26 -start_hour 14 -stop_year 2015 -stop_month 3 -stop_day 27

# --- LCS --- 2D videos, (5)6, - 10,11,12 - 21,22
#./../../build/bin/platformecpp --TEST_FOLDER_STAMPS
#./../../build/bin/platformecpp -control control2d.txt -lcsmainfolder -directory /home/ecorvee/data/LCS-videos/database1/ -lcsvideoindex 6 -startat 70 -motionwindow 2 -context2dec LOCAL -host 127.0.0.1 -port 3001 -step
#-bed LOCALBED


# --- BOREL-HALL
##./../../build/bin/libecc_main -halfsize -control control2d.txt -cam3dtype asus -recorded3d -version 3sup -directory /user/ecorvee/home/asusdata/borel-hall/ -start_year 2015 -start_month 9 -start_day 25 -start_hour 15 -stop_year 2015 -stop_month 9 -stop_day 25 -stop_hour 16

# --- fall-B09 FALL my office,   start at 2014-11-12T18:24:16.930000-bgrimage | -start_minute 24 -start_second 29 
##./../../build/bin/libecc_main -halfsize -control control2d.txt -cam3dtype asus -recorded3d -version 3sup -directory /user/ecorvee/home/asusdata/fall-B09/ -start_year 2014 -start_month 11 -start_day 12 -start_hour 18 -start_minute 24 -start_second 16 -stop_year 2014 -stop_month 11 -stop_day 13 -context2dvanish /user/ecorvee/home/workspace_new/ecplatform/datafiles/multi_cam_calib/mcc-fall-B09-results-inputs.txt -vanish_from_mcc_indexcam 0 -step

# --- lcs office
##./../../build/bin/libecc_main -halfsize -control control2d.txt -context2dec -cam3dtype asus -recorded3d -version 3sup -directory /user/ecorvee/home/asusdata/lcsoffice/ -start_year 2014 -start_month 12 -start_day 3 -start_hour 15 -stop_year 2014 -stop_month 12 -stop_day 9

# ---------- kinect2 ---------- -start_minute 10, 30
#./../../build/bin/libecc_main  -control control3d.txt -cam3dtype kinect2 -recorded3d -directory /home/ecorvee/kinect2data/maison/ -start_year 2015 -start_month 11 -start_day 9 -start_hour 18 -start_minute 20 -stop_year 2015 -stop_month 11 -stop_day 9 -stop_hour 19 
#-step

# --- thermal --- 2D videos
##./../../build/bin/libecc_main -halfsize -control control2d.txt -recorded2d -directory -directory /user/ecorvee/home/data/fanta/TIV__parts/ -stem frame_ -nbdigit 5 -startat 1000 -motionwindow 2 -context2d LOCALEC -step

# -------------------- live streaming from kinect/ASUS + recording --------------------
#-bed bed_valrose.txt 
#./../../build/bin/libecc_main -halfsize -CORRECT_FLOOR_3D 110 -control control3d.txt -stream3d -cam3dtype asus -cameraname unknownname 
##./../../build/bin/libecc_main -halfsize -control control2d.txt -stream3d -cam3dtype asus -cameraname unknownname 


#-halfsize 

##./../build/bin/libecc_main -halfsize -CORRECT_FLOOR_3D 70 -control control3d.txt -cam3dtype asus -recorded3d -version 3sup -directory /home/ecorvee/asusdata/ICP/asus-room/ -start_year 2015 -start_month 9 -start_day 1 -start_hour 14 -stop_year 2015 -stop_month 9 -stop_day 1 -stop_hour 15 
#-step

# ---------- bore-hall ---------- something wrong with depth ... recorded with writer3b ?
#./../build/bin/libecc_main -halfsize -CORRECT_FLOOR_3D 70 -control control3d.txt -cam3dtype asus -recorded3d -version 3sup -directory /home/ecorvee/asusdata/borel-hall/ -start_year 2015 -start_month 9 -start_day 25 -start_hour 15 -stop_year 2015 -stop_month 9 -stop_day 25 -stop_hour 16 

# ---------- valrose ----------
#./../build/bin/libecc_main -halfsize -CORRECT_FLOOR_3D 60 -control control3d.txt -cam3dtype asus -recorded3d -version 3sup -directory /home/ecorvee/VALROSE/asusdata/ministar9/ -norgb -start_year 2015 -start_month 3 -start_day 28 -start_hour 6 -stop_year 2015 -stop_month 3 -stop_day 29 -stop_hour 12 -step 

##./../build/bin/libecc_main -halfsize -CORRECT_FLOOR_3D 60 -control control3d.txt -cam3dtype asus -recorded3d -version 3sup -directory /home/ecorvee/asusdata/valrose/ministar9/ -norgb -start_year 2015 -start_month 3 -start_day 28 -start_hour 8 -start_minute 20 -stop_year 2015 -stop_month 3 -stop_day 29 -stop_hour 12 -step

 
#lost  ./../build/bin/libecc_main -halfsize -CORRECT_FLOOR_3D -control control3d.txt -cam3dtype asus -recorded3d -version 3sup -directory /home/ecorvee/ICP/asusdata/ -start_year 2015 -start_month 6 -start_day 12 -start_hour 10 -start_minute 16 -stop_year 2015 -stop_month 6 -stop_day 12 -stop_hour 12 -step



# for ministar9 -bed bed_valrose.txt and living room 

##./../build/bin/libecc_main -halfsize -control control3d.txt -cam3dtype asus -recorded3d -version 3sup -directory /run/netsop/u/srvpal/data/projects/demcare/valrose/asusdata/room005/bed/ -norgb -start_year 2015 -start_month 4 -start_day 4 -start_hour 16 -stop_year 2015 -stop_month 4 -stop_day 5 -stop_hour 1 -step

##./../build/bin/libecc_main -control control3d.txt -cam3dtype asus -recorded3d -version 3sup -directory /run/netsop/u/srvpal/data/projects/demcare/valrose/asusdata/room005/livingroom/ -norgb -start_year 2015 -start_month 2 -start_day 1 -start_hour 18 -stop_year 2015 -stop_month 4 -stop_day 5 -stop_hour 1 -step


#	./../build/bin/libecc_main -control control3d.txt -cam3dtype kinect -recorded3d -version 3sup -directory /home/ecorvee/recorded_fall/ -start_year 2014 -start_month 11 -start_day 12 -start_hour 18 -start_minute 23 -start_second 1 -stop_year 2014 -stop_month 12

#-halfsize

#./test1.exe
#./test2.exe

#./../build/bin/libecc_main -control control2d.txt -stream2d rtsp://192.168.0.99/img/video.sav
#./../build/bin/libecc_main -control control2d.txt -stream2d rtsp://10.2.4.220/img/video.sav -context2d ../../datafiles/calib/lcsoffice1/calibec_output.txt 
#nomore -logdir2d ../../../log2d/ -logrecord mpeg4

#-save_startcounter NOT USED ANYMORE, a file is used to replace that automatically (was used with USE_LOGOUT2D 1 and USE_LOGOUT2D_JPEG 2)

# --- LCS --- 2D videos, (5)6, - 10,11,12 - 21,22
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/data/LCS-videos/database1/ -lcsvideoindex 6 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED 
#-save_startcounter 1863 -step

# -------------------- streaming from kinect + recording --------------------
#-bed bed_valrose.txt 
##./../build/bin/libecc_main -halfsize -CORRECT_FLOOR_3D 110 -control control3d.txt -stream3d -cam3dtype asus -cameraname unknownname 
#-record_compress_3d_dir /home/ecorvee/recorded/ -record_compress_3d_fall 1 -record_compress_3d_period 1 -record_compress_when_track_moving 1 
#-record_compress_3d_dir /home/ecorvee/recorded/ -record_compress_3d_fall 1 -record_compress_3d_period 1
#-record_compress_3d_dir /home/ecorvee/recorded/ 
#-record_compress_3d_fall 1 -record_compress_3d_period 1
#-record_compress_3d_period 1
#-record_compress_3d_if_motion 1 
# recording only fall -record_compress_3d_fall 1 -record_compress_3d_period 1


#./../build/bin/libecc_main -control control3d.txt -recorded3d -version 3sup -directory /home/ecorvee/asusdata/ -start_year 2014 -start_month 9 -start_day 24 -start_hour 15 -start_minute 26 -start_second 1 -stop_year 2014 -stop_month 10


#13 ubuntu recorded 3d
#	./../build/bin/libecc_main -control control3d.txt -cam3dtype kinect -recorded3d -version 3sup -directory /home/ecorvee/recorded/ -start_year 2014 -start_month 11 -start_day 27 -start_hour 14 -start_minute 0 -start_second 1 -stop_year 2014 -stop_month 12
#	./../build/bin/libecc_main -control control3d.txt -cam3dtype kinect -recorded3d -version 3sup -directory /home/ecorvee/recorded/ -start_year 2014 -start_month 12 -start_day 2 -start_hour 10 -start_minute 0 -start_second 1 -stop_year 2014 -stop_month 12 -stop_day 2 -stop_hour 11



#	./../build/bin/libecc_main -control control3d.txt -cam3dtype kinect -recorded3d -version 3sup -directory /home/ecorvee/recorded/ -start_year 2014 -start_month 11 -start_day 6 -start_hour 16 -start_minute 15 -start_second 30 -stop_year 2014 -stop_month 12 -step
#	./../build/bin/libecc_main -control control3d.txt -cam3dtype kinect -recorded3d -version 3sup -directory /home/ecorvee/recorded/ -start_year 2014 -start_month 11 -start_day 7 -start_hour 17 -start_minute 5 -start_second 1 -stop_year 2014 -stop_month 12

###./../build/bin/libecc_main -halfsize -control control3d.txt -recorded3d -cam3dtype asus -version 3sup -directory /home/ecorvee/data-demcare/icp/scenario1/couloir1/ -start_year 2014 -start_month 7 -start_day 25 -start_hour 12 -start_minute 20 -start_second 1 -stop_year 2014 -stop_month 8  -host 127.0.0.1 -port 3000 -CamFusedWithCameraName icpcorridor2 
#-step
##./../build/bin/libecc_main -halfsize -control control3d.txt -recorded3d -cam3dtype asus -version 3sup -directory /home/ecorvee/data-demcare/icp/scenario1/couloir2/ -start_year 2014 -start_month 7 -start_day 25 -start_hour 12 -start_minute 19 -start_second 45 -stop_year 2014 -stop_month 8 -host 127.0.0.1 -port 3000 
#-step
#127.0.0.1
#./../build/bin/libecc_main -control control3d.txt -recorded3d -version 3sup -directory /u/srvpal/data/projects/stars/ICP_DataCollection_2014-07-25/scenario1/couloir2/ -start_year 2014 -start_month 7 -start_day 25 -start_hour 13 -start_minute 19 -start_second 45 -stop_year 2014 -stop_month 8
#./../build/bin/libecc_main -control control3d.txt -recorded3d -version 3sup -directory /home/ecorvee/data-demcare/icp/scenario2/couloir2/ -start_year 2014 -start_month 7 -start_day 25 -start_hour 13 -start_minute 8 -start_second 20 -stop_year 2014 -stop_month 8

# --- basel
#./../build/bin/libecc_main -control control3d.txt -cam3dtype asus -norgb -recorded3d -version 3sup -directory /home/ecorvee/data-demcare/basel/ -start_year 2014 -start_month 11 -start_day 27 -bed bed_basel2.txt

# --- EHPAD valrose
#./../build/bin/libecc_main -control control3d.txt -cam3dtype kinect -norgb -recorded3d -version 3sup -directory /home/ecorvee/data-demcare/valrose/ -start_year 2014 -start_month 8 -start_day 12 -bed bed_valrose.txt
#./../build/bin/libecc_main -control control3d.txt -cam3dtype kinect -norgb -recorded3d -version 3sup -directory /u/srvpal/data/projects/demcare/asusdata-ehpad-minipc1-norgb/ -start_year 2014 -start_month 8 -start_day 12
# --- EHPAD lie on bed
#./../build/bin/libecc_main -control control3d.txt -norgb -recorded3d -version 3sup -directory /u/srvpal/data/projects/demcare/asusdata-ehpad-minipc1-norgb/ -start_year 2014 -start_month 8 -start_day 6 -start_hour 10 -start_minute 11
#./../build/bin/libecc_main -control control3d.txt -cam3dtype kinect -recorded3d -version 4 -directory /home/ecorvee/data-kinect-compressed/home-v4/ -start_year 2013 -start_month 8 -start_day 5 -start_hour 12 -start_minute 50 -stop_year 2013 -stop_month 8 -stop_day 5 -stop_hour 12 -stop_minute 51 -stop_second 4

#./../build/bin/test_c -control control2d.txt -lcsmainfolder /home/ecorvee/LCS/data/database1/ -lcsvideoindex 6 -startat 50 -motionwindow 2 -context2d LOCAL 
#nomore -logdir2d ../../../log2d/


#-context2d ../../datafiles/calib/lcsoffice1/calibec_output.txt
#-context2d LOCAL 
#-stream2d rtsp://192.168.0.99/img/video.sav
#./../build/bin/compil-c
#-debug -step
#-adapt 99

#./../build/bin/test_c -control control2d.txt -lcsmainfolder /home/ecorvee/LCS/data/database1/ -lcsvideoindex 12 -startat 50 -motionwindow 2 -debug





#./../.././../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 1 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 0
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 2 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 436
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 3 -startat 70 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 774
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 4 -startat 60 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 1144
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 5 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 1477
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 6 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 1863
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 7 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 2143
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 10 -startat 70 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 2318
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 11 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 2540
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 12 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 2715
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 14 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 3002
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 16 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 3129
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 18 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 3352
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 19 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 3470
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 20 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 3590
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 21 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 3815
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 22 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 4037
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 23 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 4259
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 24 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 4480
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 25 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 4706
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 26 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 4928
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 27 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 5150
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 28 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 5376
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 29 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 5510
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 30 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 5692
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 31 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 5911
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 33 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 6030
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 34 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 6469
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 35 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 6620
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 36 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 6750
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 37 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 6983
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 38 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 7271
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 39 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 7559
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 40 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 7847
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 41 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 8132
#./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 42 -startat 1 -motionwindow 2 -context2d LOCALEC -bed LOCALBED -save_startcounter 8410
####./../build/bin/libecc_main -control control2d.txt -lcsmainfolder -directory /home/ecorvee/LCS/data/database1/ -lcsvideoindex 45 -startat 1 -motionwindow 2 -context2d LOCALEC -save_startcounter 8654
#-step
