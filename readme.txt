// dockerfileのビルド
docker build . -t yolo5/test

// dockerコンテナで5000番ポートでsrcフォルダをマウントしてコマンド実行
docker run -it -p 5000:5000 yolo5/test

docker run --privileged -it -p 5000:5000 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw --device /dev/video0:/dev/video0:mwr yolo5/test

// 予測を実行
python3 detect.py --weights yolov5s.pt --img 416 --conf 0.4

python3 detect.py --source /usr/src/app/data/images/bus.jpg --save-txt --save-conf
python3 detect.py --source /usr/src/app/data/movie/sample_walk.mp4 --save-txt

// コンテナからデータをコピー
sudo docker cp 22a182f15d89:/usr/src/app/runs ~/git/yolo/yolov5/runs 