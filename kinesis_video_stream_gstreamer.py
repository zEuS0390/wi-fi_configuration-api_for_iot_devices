import os, signal, subprocess, time

gstreamer_pipeline = r"gst-launch-1.0 libcamerasrc ! video/x-raw,width=640,height=480,framerate=30/1,format=I420 ! videoconvert ! v4l2h264enc extra-controls=controls,repeat_sequence_header=1 ! video/x-h264,level='(string)4' ! h264parse ! video/x-h264,stream-format=avc, alignment=au,width=640,height=480,framerate=30/1 ! "

kvssink = "kvssink stream-name={stream_name} access-key={access_key} secret-key={secret_key} aws-region={aws_region} log-config=/home/user/Desktop/amazon-kinesis-video-streams-producer-sdk-cpp/kvs_log_configuration".format(
    stream_name=os.environ.get("AWS_KINESIS_VIDEO_STREAM_NAME"),
    access_key=os.environ.get("AWS_KINESIS_VIDEO_STREAM_ACCESS_KEY_ID"),
    secret_key=os.environ.get("AWS_KINESIS_VIDEO_STREAM_SECRET_ACCESS_KEY"),
    aws_region=os.environ.get("AWS_KINESIS_VIDEO_STREAM_REGION")
)

pro = subprocess.Popen(gstreamer_pipeline+kvssink, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

try:
    while pro.poll() is None:
        time.sleep(1)
except:
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
