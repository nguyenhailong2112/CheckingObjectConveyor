# SCOPE OF WORK - Industrial Conveyor Object Counting System – Fail-Safe Demo

Phase: PoC / Industrial Demo
Hardware Target: Core i5-13700 + RTX4060
Deployment Target: PC Vision (Edge-ready)

# PHẦN 1 — TRIẾT LÝ THIẾT KẾ HỆ THỐNG + MỤC TIÊU NGHIỆP VỤ + KIẾN TRÚC TƯ DUY

I. Vấn đề thực sự cần giải quyết

Nghe qua bài toán:

Detect Object
Count Object
Track Object

rất nhiều đội Vision sẽ nghĩ:

Camera
↓
YOLO
↓
Tracker
↓
Count

Đây là cách làm demo học thuật.

Trong môi trường thực tế nó dễ hỏng vì:

vật chồng chéo
vật dính sát
blur
miss detection
occlusion
đổi ánh sáng
tracker mất ID
frame drop
camera lag
vật biến dạng

Điều cần giải quyết thật sự không phải:

Làm sao detect được vật

mà là:

Làm sao đảm bảo:
1 vật lý thực
=
1 lần đếm duy nhất
Triết lý cốt lõi của hệ thống
Object Existence
↓
Object Persistence
↓
Object Validation
↓
Single Count Guarantee

Ý nghĩa:

Object Existence

Hệ thống cần trả lời:

"Có vật thể tồn tại hay không?"

không phải:

"Đây là vật gì?"

Do đó:

Single class:

foreground_object

không cần:

box
bag
carton
bottle
...

Lý do:

Bạn không cần phân loại.

Bạn chỉ cần:

có vật hay không
Object Persistence

Một vật xuất hiện:

frame 1
frame 2
frame 3
frame 4

không có nghĩa:

4 vật

mà:

1 vật tồn tại liên tục

Do đó:

tracking tồn tại để:

duy trì sự tồn tại vật lý

chứ không phải:

theo dõi hành vi đối tượng
Object Validation

Một vật được detect:

không có nghĩa được count

Ví dụ:

confidence thấp

hoặc

overlap nghiêm trọng

hoặc

trajectory bất thường

↓

phải xác nhận lại.

Single Count Guarantee

Đây là mục tiêu cao nhất:

Một vật thể vật lý
↓

được phép count đúng duy nhất một lần

Ưu tiên:

Accuracy Count > Stability > Latency > Maintainability
II. Phạm vi hệ thống

Hệ thống sẽ làm:

Bắt buộc

✅ Detect vật thể

✅ Track vật thể

✅ Count vật thể

✅ Fail-safe

✅ Logging

✅ Monitoring

✅ Review uncertain cases

Không thuộc phạm vi PoC

❌ OCR

❌ Barcode

❌ Defect inspection

❌ Classification

❌ Multi-camera fusion

❌ ERP/MES integration

❌ PLC synchronization

❌ Cloud analytics

❌ Predictive analytics

Lý do:

PoC phải tập trung vào:

Single Count Guarantee
III. Mục tiêu KPI của dự án
Metric	Target
Count Accuracy	≥99%
Double Count Rate	<0.2%
Miss Count Rate	<0.2%
ID Switch Rate	<1%
Uncertain Rate	<2%
Precision	≥97%
Recall	≥97%
FPS	≥35
Runtime stability	≥8 giờ
Crash	0
IV. Kiến trúc tư duy tổng thể

Đây là luồng logic của toàn hệ thống:

Camera Input
        ↓
ROI Management
        ↓
Adaptive Preprocessing
        ↓
Foreground Detection
        ↓
Overlap Analysis
        ↓
Conditional Refinement
        ↓
Tracking
        ↓
State Machine
        ↓
Dual-Zone Validation
        ↓
Count Lock
        ↓
Fail-safe
        ↓
Review Queue
        ↓
Monitoring
        ↓
Logging

Giải thích:

Camera Input

Nhiệm vụ:

lấy frame ổn định

không phải:

đọc video đơn thuần
ROI

Nhiệm vụ:

chỉ xử lý vùng quan tâm
Detection

Nhiệm vụ:

tìm object candidate
Tracking

Nhiệm vụ:

duy trì định danh vật lý
State Machine

Nhiệm vụ:

xác định trạng thái đối tượng
Dual Zone

Nhiệm vụ:

xác thực vật thực sự đi qua băng tải
Count Lock

Nhiệm vụ:

chống đếm lặp
Fail-safe

Nhiệm vụ:

không chắc chắn
↓

không count
Review Queue

Nhiệm vụ:

lưu lỗi

↓

retrain

Đây là nền móng của toàn bộ dự án.

# PHẦN 2 - DATASETS 
Phần này mình sẽ là người tự chủ động xử lý, vậy nên bạn hãy cứ yên tâm và tin tưởng ở mình nha!

# PHẦN 3 — SYSTEM ARCHITECTURE + CAMERA LAYER + ROI + PREPROCESSING + INPUT PIPELINE
I. Mục tiêu của Runtime System

Runtime system phải đảm bảo:

Functional goals

✅ nhận video liên tục

✅ xử lý realtime

✅ detect/count chính xác

✅ duy trì tracking

Non-functional goals

✅ không lag tích lũy

✅ không memory leak

✅ tự phục hồi lỗi

✅ không block pipeline

✅ chạy liên tục nhiều giờ

KPI:

Metric	Target
Input FPS stability	>95%
Frame drop	<2%
Memory leak	0
Camera reconnect	<5 giây
Runtime	≥8 giờ
II. Kiến trúc Runtime tổng thể

Luồng chạy thực tế:

Camera Thread
        ↓
Frame Queue
        ↓
ROI Manager
        ↓
Preprocessing Thread
        ↓
Detection Thread
        ↓
Tracking Thread
        ↓
Counting Thread
        ↓
Visualization Thread
        ↓
Logger Thread

Không làm kiểu:

while True:

    frame=read()

    detect()

    track()

    count()

    display()

Lý do:

Một module chậm:

↓
toàn hệ thống chậm
↓
lag tích lũy
↓
FPS tụt

Do đó:

Pipeline phải:

multi-stage
+
asynchronous
III. Camera Layer Design

Camera layer không phải:

đọc video

Camera layer là:

nguồn dữ liệu sống của toàn hệ thống

Input hỗ trợ:

RTSP

USB Camera

Industrial Camera

Video File

Interface:

class CameraSource:

    def connect()

    def read()

    def reconnect()

    def health_check()

    def release()

Output:

frame
timestamp
frame_id
camera_status

Ví dụ:

{
frame: ndarray,

timestamp:171512.32,

frame_id:1231,

status:"healthy"
}
IV. Queue Design

Đây là phần cực quan trọng.

Sai:

queue=maxsize(100)

Khi detector chậm:

camera

30 FPS

↓

queue đầy

↓

frame cũ bị xử lý

↓

thực tế trễ 5–10 giây

Thiết kế đúng:

Queue(maxsize=1)

Logic:

if queue.full():

    queue.get()

queue.put(frame)

Ý nghĩa:

Luôn giữ:

frame mới nhất

không giữ:

mọi frame

Trade-off:

Mất một số frame.

Nhưng:

realtime ổn định > giữ toàn bộ frame
V. Camera Health Monitor

Nhiều demo bỏ qua phần này.

Thực tế:

Camera có thể:

treo

drop frame

mất tín hiệu

exposure lỗi

Thiết kế:

class CameraHealth:

    frozen_detector()

    fps_monitor()

    reconnect_monitor()

    exposure_monitor()
1. Frozen frame detection

Logic:

So sánh:

Frame(t)

Frame(t−1)

Nếu:

pixel_difference<threshold

liên tục:

3–5 giây

↓

camera frozen
2. FPS monitor

Theo dõi:

actual_fps

Nếu:

actual_fps<expected_fps*0.5

↓

alert

3. Exposure anomaly

Tính:

mean_intensity

Nếu:

brightness<min

brightness>max

↓

warning

VI. ROI Management

Mục tiêu:

Không xử lý toàn bộ ảnh.

Chỉ xử lý:

vùng có vật chạy

Ví dụ:

Camera:

1920x1080

Băng tải:

chiếm 35%

Sai:

detect toàn bộ frame

Đúng:

crop ROI

Lợi ích:

giảm compute
35–60%
giảm false positive
tăng FPS

Thiết kế:

class ROIManager:

    draw_roi()

    draw_entry_zone()

    draw_verify_zone()

    save()

    load()

File:

{
roi:

[
150,
200,
1600,
900
],

entry_zone:

[
200,
300,
1500,
450
],

verify_zone:

[
200,
650,
1500,
800
]
}
VII. Entry Zone và Verify Zone

Thiết kế:

ROI

┌─────────────────┐
│                 │
│ Entry Zone      │
│─────────────────│
│                 │
│                 │
│─────────────────│
│ Verify Zone     │
│                 │
└─────────────────┘

Mục tiêu:

Không count ngay khi detect.

Object:

NEW

↓

ENTERED

↓

STABLE

↓

VERIFY

↓

COUNT

Điều này giảm:

false count
duplicate count
ghost count
VIII. Preprocessing Design

Nguyên tắc:

Preprocessing:

không được phá dữ liệu

Sai:

CLAHE mọi frame

denoise mọi frame

Kết quả:

méo texture

thay đổi đặc trưng

Đúng:

Adaptive preprocessing.

Pipeline:

Input
    ↓
Brightness analysis
    ↓
Noise analysis
    ↓
Conditional processing
    ↓
Resize
    ↓
Normalize
IX. Brightness Analysis

Tính:

mean_intensity

Nếu:

mean<80

↓

Low light

Nếu:

mean>220

↓

Over exposure

X. Noise Analysis

Ước lượng:

noise_variance

Nếu:

noise_variance>threshold

↓

Apply:

fastNlMeansDenoising()
XI. CLAHE Logic

Chỉ dùng khi:

contrast<threshold

Ví dụ:

if contrast<25:

    apply_CLAHE()

Không:

always_apply=True
XII. Resize Strategy

Camera:

1920x1080

Runtime:

1280x720

Lý do:

Cân bằng:

accuracy

vs

speed
XIII. Preprocessing Configuration

File:

preprocessing:

    target_size:

        width:1280
        height:720

    brightness:

        low:80
        high:220

    contrast_threshold:25

    noise_threshold:15

    use_CLAHE:true

    use_denoise:true
XIV. Runtime Folder Structure
runtime/

    camera/

        camera_source.py

        camera_health.py

    roi/

        roi_manager.py

    preprocess/

        adaptive_preprocess.py

    queue/

        frame_queue.py

# PHẦN 4 — DETECTION LAYER + TRAINING STRATEGY + OVERLAP HANDLING + REFINEMENT PIPELINE
I. Mục tiêu Detection Layer

Detection layer phải trả lời:

"Có vật thể tồn tại ở đâu?"

không phải:

"Đây là loại vật gì?"

Do đó:

Class:

foreground_object

duy nhất.

Không:

carton
bag
bottle
foam_box
...

Lý do:

Bạn đang giải:

Object Counting Problem

không phải:

Object Classification Problem

Output detector:

[
{
bbox:[x1,y1,x2,y2],
confidence:0.93
},

{
bbox:[...],
confidence:0.89
}
]
II. Kiến trúc Detection Runtime

Luồng:

ROI frame
      ↓
Adaptive preprocess
      ↓
YOLO11m inference
      ↓
Confidence filtering
      ↓
Overlap candidate analysis
      ↓
Conditional refinement
      ↓
Object candidate output
III. Tại sao chọn YOLO11m

Không chọn cực lớn:

YOLO11x

Không chọn cực nhỏ:

YOLO11n

Phân tích:

Model	Accuracy	FPS	RTX4060
n	thấp	rất cao	dư
s	trung bình	rất cao	dư
m	tốt	tốt	phù hợp
l	cao	giảm	nặng
x	rất cao	thấp	thừa

YOLO11m là điểm cân bằng:

accuracy
+
speed
+
maintainability
IV. Training Strategy

Không train kiểu:

train mặc định
↓
hy vọng model tốt

Thiết kế:

Dataset
      ↓
Baseline train
      ↓
Failure analysis
      ↓
Hard sample mining
      ↓
Retrain
      ↓
Validation

Chu trình:

Train
   ↓
Lỗi
   ↓
Thu thập lỗi
   ↓
Bổ sung dataset
   ↓
Retrain
V. Training Configuration

Ví dụ:

model:

    yolo11m.pt

imgsz:

    1280

epochs:

    100

batch:

    16

optimizer:

    AdamW

lr0:

    0.001

weight_decay:

    0.0005

patience:

    20

cos_lr:

    true

mosaic:

    0.5

mixup:

    0.1

Giải thích:

Epoch:

100

đủ để hội tụ.

Mosaic:

0.5

giúp:

dense scene
overlap

Mixup:

0.1

giảm overfit.

Không:

mixup=0.5

vì tạo dữ liệu giả quá mạnh.

VI. Detection Confidence Strategy

Đây là phần nhiều đội làm sai.

Sai:

confidence=0.8

Vấn đề:

miss object

Sai tiếp:

confidence=0.2

Vấn đề:

false positive

Thiết kế:

confidence=0.5

mặc định.

Sau đó:

track_conf=
alpha*current
+
(1-alpha)*history

Ví dụ:

alpha=0.7

Lý do:

Quyết định cuối cùng dựa trên:

track-level confidence

không phải:

single frame confidence

Ví dụ:

Frame:

0.92
0.87
0.48
0.91
0.89

EMA:

0.92
0.89
0.77
0.84
0.87

Không bị dao động mạnh.

VII. Overlap Problem

Đây là bài toán khó nhất.

Ví dụ:

██████
  ██████

Detector thường:

┌─────────┐
│ object  │
└─────────┘

thành:

1 object

trong khi thực tế:

2 object

Nếu không xử lý:

miss count
VIII. Overlap Candidate Detection

Không chạy refinement mọi frame.

Lý do:

Rất nặng.

Ta chỉ kích hoạt khi nghi ngờ.

Điều kiện:

Area anomaly
area_ratio=
current_area/
moving_average_area

Nếu:

area_ratio>1.8

↓

suspect

Aspect ratio anomaly
w/h

Nếu:

aspect>3

↓

suspect

Density anomaly
bbox_count /
roi_area

Nếu quá lớn:

↓

suspect

Shape change anomaly
shape_change

Nếu:

>30%

↓

suspect

IX. Conditional Refinement Pipeline

Luồng:

Detection
    ↓

Overlap suspicion?

    ↓

NO
    ↓
Output

YES
    ↓

YOLO11-seg
    ↓

Refined candidates
    ↓

Output

Không dùng:

SAM2

ở demo.

Lý do:

SAM2:

Ưu:

mask đẹp

Nhược:

rất nặng

khó realtime

khó maintain

YOLO-seg:

Ưu:

nhanh

đủ tốt

dễ deploy
X. Refinement Output

Output:

[
{
bbox:[...],

mask:[...]

},

{

bbox:[...],

mask:[...]

}
]

Sau refinement:

██████
 ██████

↓

Object1

Object2
XI. NMS Strategy

Sai:

iou=0.9

Vấn đề:

merge object

Sai:

iou=0.1

Vấn đề:

duplicate box

Thiết kế:

iou=0.5

Có thể tune:

0.45–0.6
XII. Hard Sample Mining

Sau khi chạy demo:

Lưu:

miss detection

false detection

overlap failure

blur failure

Folder:

false_samples/

    overlap/

    blur/

    dense/

    occlusion/

Sau đó:

re-annotate

↓

retrain

↓

deploy v2
XIII. Runtime Module Structure
vision/

    detector/

        detector.py

        infer_engine.py

        confidence.py

    overlap/

        candidate_analyzer.py

        overlap_refiner.py

    training/

        train.py

        export.py
XIV. KPI Detection Layer
Metric	Target
Detection Precision	≥97%
Detection Recall	≥97%
False Positive	<2%
False Negative	<2%
Inference latency	<20ms
Detection FPS	>50

# PHẦN 5 — TRACKING LAYER + TEMPORAL CONSISTENCY + STATE MACHINE + OBJECT PERSISTENCE LOGIC
I. Mục tiêu Tracking Layer

Tracking KHÔNG nhằm:

theo dõi hành vi

Tracking phải đảm bảo:

1 vật lý thực

↓

1 định danh liên tục

↓

1 lần count

Tracking layer phải:

✅ duy trì ID

✅ xử lý miss detection ngắn

✅ xử lý occlusion

✅ xử lý overlap

✅ chống ID switch

✅ hỗ trợ counting logic

KPI:

Metric	Target
ID Switch Rate	<1%
Track Recovery	>95%
Double Count Rate	<0.2%
Lost Track Rate	<2%
II. Kiến trúc Tracking

Luồng:

Detector output
        ↓
ByteTrack Association
        ↓
Track Update
        ↓
Temporal Consistency
        ↓
State Machine
        ↓
Track Registry
        ↓
Counting Layer

Input:

[
{
bbox:[100,200,300,500],
confidence:0.91
},

{
bbox:[400,220,580,490],
confidence:0.88
}
]

Output:

[
{
track_id:15,
bbox:[...],
track_conf:0.89,
state:"STABLE"
},

{
track_id:16,
bbox:[...],
track_conf:0.93,
state:"NEW"
}
]
III. Tại sao chọn ByteTrack

Không chọn tracker cực phức.

Ví dụ:

DeepSORT
StrongSORT
OCSORT
BoTSORT

Lý do:

Bài toán của chúng ta:

camera top-down

1 hướng

không re-identification đa camera

ByteTrack mạnh ở:

1. Nhanh
2. Tận dụng low confidence box
3. Tốt với miss detection ngắn
4. Realtime dễ triển khai
IV. ByteTrack Configuration

Không hard-code.

Thiết kế:

tracking:

    match_thresh:0.65

    track_buffer:

        int(fps*0.3)

    min_box_area:100

    lost_cleanup:10

Ví dụ:

FPS:

40

↓

track_buffer=int(40×0.3)

=12

Ý nghĩa:

Nếu detector mất:

12 frame

↓

track vẫn giữ.

V. Track Registry

Đây là thành phần cực quan trọng.

Thiết kế:

class TrackRegistry:

    tracks={

        track_id:TrackObject

    }

TrackObject:

class TrackObject:

    id

    bbox

    confidence

    state

    trajectory

    age

    missed_frames

    zone_history

    counted

    uncertainty

Ví dụ:

{
id:17,

bbox:[120,300,450,620],

confidence:0.91,

state:"STABLE",

trajectory:[...],

counted:False,

uncertainty:False
}
VI. Temporal Consistency

Đây là phần cực kỳ quan trọng.

Một detect ở một frame:

không đủ đáng tin

Ví dụ:

Frame:

frame1

detect=YES
frame2

detect=NO
frame3

detect=YES

Nếu dùng detector trực tiếp:

YES

NO

YES

↓

2 object khác nhau

Nhưng thực tế:

1 object

Temporal consistency xử lý:

YES

PREDICT

YES

Track vẫn giữ.

VII. Trajectory Buffer

Mỗi object:

Lưu:

trajectory=
[
(x1,y1),

(x2,y2),

(x3,y3)
]

Độ dài:

20–30 points

Mục đích:

direction
speed
acceleration
anomaly detection
VIII. Motion Validation

Theo dõi:

speed=
distance/frame

Nếu:

speed>physical_limit

↓

reject

Ví dụ:

Băng tải:

0.8 m/s

Camera scale:

120 pixel =10 cm

Nếu object:

nhảy

700 pixel/frame

↓

không hợp lý

↓

Uncertain

IX. Direction Validation

Băng tải:

TOP

↓

BOTTOM

Tính:

dy=
current_y−previous_y

Nếu:

dy<0

↓

reverse movement

↓

Uncertain

X. Track Confidence Aggregation

Không dùng confidence của detector đơn lẻ.

Thiết kế:

track_conf=

α×current

+

(1−α)×history

Ví dụ:

alpha=0.7

Frame:

0.95
0.90
0.50
0.91
0.88

EMA:

0.95
0.92
0.79
0.84
0.87

Tránh:

confidence dao động mạnh
XI. Object State Machine

Đây là trái tim logic của toàn hệ thống.

State diagram:

NEW
    ↓

ENTERED
    ↓

STABLE

↙        ↘

COUNTED   UNCERTAIN

↓              ↓

EXITED      REVIEW
XII. Giải thích trạng thái
NEW

Điều kiện:

track vừa xuất hiện

Ví dụ:

age<3 frame

Không count.

ENTERED

Điều kiện:

đi vào Entry Zone

Không count.

STABLE

Điều kiện:

age>5

confidence>threshold

trajectory ổn định

Cho phép:

đi xác thực count
COUNTED

Điều kiện:

qua Verify Zone

Hành động:

count+=1

count_registry.add(track_id)
EXITED

Điều kiện:

ra khỏi ROI

Cleanup:

remove(track)
UNCERTAIN

Điều kiện:

trajectory bất thường

overlap unresolved

confidence thấp

ID switch nghi ngờ

Không count.

REVIEW

Điều kiện:

UNCERTAIN kết thúc

Đưa vào:

review_queue
XIII. Count Registry

Cơ chế chống đếm lặp.

count_registry=
set()

Logic:

if track_id not in count_registry:

    count()

    count_registry.add(track_id)

Kết quả:

1 track

=

count tối đa 1 lần
XIV. Cleanup Strategy

Không xóa ngay.

Nếu:

missed_frames>lost_cleanup

↓

cleanup

Ví dụ:

lost_cleanup=10
XV. Runtime Structure
tracking/

    bytetrack_engine.py

    track_registry.py

    temporal_filter.py

    motion_validator.py

    state_machine.py

    trajectory.py
XVI. KPI Tracking Layer
Metric	Target
ID Switch	<1%
Track Recovery	>95%
Lost Track	<2%
Double Count	<0.2%
Motion anomaly false trigger	<1%
XVII. Kết thúc phần 5

Đến đây hệ thống đã có:

Camera
     ↓

ROI
     ↓

Preprocess
     ↓

Detection
     ↓

Overlap refinement
     ↓

Tracking
     ↓

Temporal consistency
     ↓

State machine

Lúc này hệ thống không chỉ:

"nhìn thấy vật"

mà đã hiểu:

"đây là cùng một vật tồn tại liên tục"

# PHẦN 6 — COUNTING ENGINE + DUAL-ZONE VALIDATION + SINGLE-COUNT GUARANTEE + FAIL-SAFE LOGIC + KPI SYSTEM
I. Mục tiêu Counting Engine

Mục tiêu không phải:

đếm object xuất hiện

Mà là:

đếm đúng vật lý thực đi qua băng tải

KPI nghiệp vụ:

Metric	Target
Count Accuracy	≥99%
Double Count Rate	<0.2%
Miss Count Rate	<0.5%
Uncertain Rate	<2%
False Count	<0.2%
II. Kiến trúc Counting Layer

Pipeline:

Tracking output
        ↓
State validation
        ↓
Zone validation
        ↓
Direction validation
        ↓
Single-count validation
        ↓
Fail-safe validation
        ↓
Count commit
        ↓
Logging

Input:

{
track_id:17,

state:"STABLE",

bbox:[100,200,400,500],

trajectory:[...]

}

Output:

{
track_id:17,

count_decision=True,

count_reason:"validated"
}
III. Dual-Zone Validation

Không dùng:

if line_cross:

     count+=1

Vì:

line crossing

rất dễ lỗi:

rung bbox
object dài
overlap
detector nhảy

Dùng:

Entry Zone
        ↓
Verify Zone

Ví dụ:

+----------------------+

 Entry Zone

-----------------------

 Verify Zone

+----------------------+

Luồng hợp lệ:

NEW
↓

ENTERED

↓

STABLE

↓

Entry Zone

↓

Verify Zone

↓

COUNT

Nếu:

Verify trước Entry

↓

Reject

IV. Zone Manager

Thiết kế:

class ZoneManager:

      entry_zone

      verify_zone

      virtual_line

Kiểm tra:

if centroid in entry_zone:

      track.entered=True
if centroid in verify_zone:

      track.verified=True
V. Zone History

Mỗi track:

zone_history=
[
ENTRY,
ENTRY,
VERIFY
]

Mục tiêu:

xác minh:

đúng trình tự

Ví dụ:

Hợp lệ:

ENTRY

↓

VERIFY

Không hợp lệ:

VERIFY

↓

ENTRY
ENTRY

↓

ENTRY

↓

EXIT

↓

Reject

VI. Direction Validation

Băng tải:

TOP

↓

BOTTOM

Tính:

dy=

current_y−previous_y

Nếu:

dy<0

↓

reverse

↓

Reject

Nếu:

speed≈0

↓

object đứng yên

↓

Uncertain

VII. Single Count Registry

Đây là cơ chế quan trọng nhất.

Thiết kế:

count_registry=
set()

Logic:

if track_id not in count_registry:

        count+=1

        count_registry.add(track_id)

Ví dụ:

Track:

17

Qua Verify:

count=120

Track mất:

2 frame

Xuất hiện lại:

17

Kiểm tra:

17 in count_registry

↓

True

↓

Không count lại

VIII. Count Commit Logic

Điều kiện bắt buộc:

if (

track.state=="STABLE"

and track.entered

and track.verified

and valid_direction

and not uncertain

and track.id not in count_registry

):

Thực hiện:

count+=1

track.counted=True

count_registry.add(track.id)
IX. Count Lock Mechanism

Sau khi count:

track.counted=True

Mục tiêu:

khóa track

Ví dụ:

Track 17

↓

COUNT

↓

bbox rung

↓

cross line lại

Không:

count lần 2
X. Fail-safe Layer

Đây là lớp bảo vệ cuối.

Triết lý:

Không chắc chắn

=

Không count
XI. Uncertain Rules
Rule 1

Confidence thấp:

track_conf<0.5

↓

UNCERTAIN

Rule 2

Trajectory bất thường:

speed>

physical_limit

↓

UNCERTAIN

Rule 3

Đảo hướng:

dy<0

↓

REJECT

Rule 4

Overlap không giải quyết được:

overlap=True

refinement=False

↓

UNCERTAIN

Rule 5

Zone sai thứ tự:

VERIFY

↓

ENTRY

↓

REJECT

Rule 6

ID switch nghi ngờ:

distance>

threshold

↓

UNCERTAIN

XII. Severity System
Trigger	Severity	Action
Low confidence	Low	Uncertain
Motion anomaly	Medium	Uncertain
Overlap unresolved	Medium	Uncertain
Zone mismatch	High	Reject
Reverse direction	High	Reject
Suspected ID switch	High	Uncertain
XIII. Review Queue

Thiết kế:

class ReviewQueue:

      frame

      metadata

      track_history

      timestamp

Ví dụ:

{
frame:"img_241.png",

track_id:17,

reason:"overlap_unresolved",

history:[...]

}

Mục tiêu:

review thủ công
retraining
root-cause analysis
XIV. Runtime Logging

Mỗi count:

timestamp,
track_id,
state,
confidence,
decision

Ví dụ:

12:30:22,
17,
COUNTED,
0.91,
VALID

Ví dụ uncertain:

12:31:04,
22,
UNCERTAIN,
0.44,
LOW_CONF
XV. KPI Engine

Đây là lớp đánh giá hệ thống.

Thiết kế:

class KPIEngine:

      total_count

      uncertain_count

      fp_count

      fn_count

      double_count

KPI tính realtime:

Count Accuracy
correct_count
/
ground_truth
Double Count Rate
double_count

/

total_count
Miss Count Rate
miss_count

/

ground_truth
Uncertain Rate
uncertain

/

total
False Positive
FP

/

total
XVI. Dashboard KPI

Hiển thị realtime:

TOTAL COUNT:      1245

UNCERTAIN:        12

FPS:              41

COUNT ACCURACY:   99.2%

DOUBLE COUNT:     0.08%

MISS COUNT:       0.3%

CAMERA:           HEALTHY
XVII. KPI Acceptance Gate

Đây là điều kiện nghiệm thu.

Metric	Acceptance
Count Accuracy	≥99%
Double Count	<0.2%
Miss Count	<0.5%
Precision	≥97%
Recall	≥97%
Uncertain	<2%
FPS	≥35
Camera Recovery	<3 s
ID Switch	<1%
XVIII. Runtime Structure
counting/

    zone_manager.py

    counting_engine.py

    count_registry.py

    fail_safe.py

    uncertain_rules.py

    review_queue.py

    kpi_engine.py
XIX. Kết thúc Phần 6

Đến đây hệ thống đã đạt:

Camera
    ↓

ROI
    ↓

Preprocessing
    ↓

Detection
    ↓

Overlap refinement
    ↓

Tracking
    ↓

Temporal consistency
    ↓

State machine
    ↓

Counting engine
    ↓

Fail-safe
    ↓

KPI

Và lúc này hệ thống đã đạt mục tiêu nghiệp vụ:

Một vật lý thực
        ↓
Một ID ổn định
        ↓
Một lần xác thực
        ↓
Một lần count duy nhất

# PHẦN 7 — OPERATIONAL SYSTEM
Monitoring + Dashboard + Logging + Testing + Validation + Deployment + UI/UX
I. Mục tiêu phần này

Không chỉ hiển thị:

BBox
Track ID
Count

Mà phải tạo được:

Conveyor Monitoring Console

Người vận hành phải nhìn 3–5 giây là hiểu:

hệ thống đang hoạt động hay không
camera khỏe hay lỗi
count đang bao nhiêu
có bất thường không
ca sản xuất hiện tại thế nào
cần thao tác gì
II. Kiến trúc hệ thống vận hành
Camera
    ↓

Vision Pipeline
    ↓

Tracking
    ↓

Counting
    ↓

Fail-safe
    ↓

KPI Engine
    ↓

Data Service Layer
    ↓

Dashboard/UI
    ↓

Logs + Database
III. Kiến trúc UI tổng thể

Không làm:

OpenCV window đầy chữ

Không làm:

cửa sổ debug dành cho developer

Làm:

Industrial Operator Dashboard

Bố cục:

+------------------------------------------------------+

 Camera View                     KPI Panel

+----------------------+    +----------------+

|                      |    | TOTAL: 1254    |

|                      |    | TARGET:1500    |

|                      |    | UNCERTAIN:3    |

|                      |    | FPS:41         |

|                      |    | STATUS:GOOD    |

+----------------------+    +----------------+

--------------------------------------------------------

 Production Analytics

+------------------------------------------------------+

| Hourly Count Chart                                  |

+------------------------------------------------------+

--------------------------------------------------------

 Event Panel

+------------------------------------------------------+

| [12:31] Camera reconnect                            |

| [12:35] Object uncertain                            |

| [12:37] Count committed                             |

+------------------------------------------------------+

--------------------------------------------------------

 Controls

[Start]

[Stop]

[Reset]

[Export Report]

[Screenshot]

+------------------------------------------------------+
IV. Công nghệ UI

Demo:

PyQt6

Lý do:

✓ ổn định

✓ desktop native

✓ realtime tốt

✓ dễ đóng gói

✓ ít phụ thuộc

Tương lai:

Backend:

FastAPI

Frontend:

React

Nhưng demo:

PyQt

là phù hợp nhất.

V. Module UI

Cấu trúc:

ui/

    main_window.py

    camera_widget.py

    kpi_widget.py

    chart_widget.py

    event_widget.py

    settings_widget.py

    control_widget.py
VI. Camera Widget

Hiển thị:

video realtime
bbox
track id
direction
zone
trajectory

Ví dụ:

+----------------------------------+

ID17

+----------+

|          |

| object   |

+----------+

↓

Track

Entry Zone

Verify Zone

+----------------------------------+

Màu trạng thái:

Trạng thái	Màu
NEW	xanh dương
STABLE	xanh lá
COUNTED	trắng
UNCERTAIN	vàng
ERROR	đỏ
VII. KPI Widget

Hiển thị realtime:

TOTAL COUNT

1254
TARGET PRODUCTION

1500
CURRENT FPS

41
COUNT ACCURACY

99.2%
UNCERTAIN

3
DOUBLE COUNT

0.1%
CAMERA STATUS

HEALTHY
VIII. Production Analytics

Biểu đồ:

count theo thời gian
uncertain theo thời gian
FPS theo thời gian
throughput

Ví dụ:

Items

400 |

300 |

200 |

100 |

0____________________

 8h 9h 10h 11h

Hiển thị:

Hourly production
Shift production
Daily production
IX. Event Panel

Hiển thị log dạng thời gian thực:

Ví dụ:

12:30:22

Track17 COUNTED
12:30:28

Track22 UNCERTAIN
12:30:45

Camera reconnect
12:31:00

FPS dropped

Màu:

Event	Màu
Info	xanh
Warning	vàng
Error	đỏ
X. Operator Control Panel

Chức năng:

Start System
Stop System
Pause
Reset Count
Save Screenshot
Export Report
Load ROI
Settings

Ví dụ:

[START]

[STOP]

[RESET]

[EXPORT]

[ROI]
XI. Settings Panel

Cho phép chỉnh:

confidence_threshold:0.5

track_buffer:12

uncertain_threshold:0.05

fps_limit:40

Không cần sửa code.

XII. Logging System

Cấu trúc:

logs/

    count_log.csv

    uncertain_log.csv

    system_log.csv

    error_log.csv

Ví dụ:

count:

timestamp,track,decision

12:30:22,17,COUNT

uncertain:

timestamp,track,reason

12:31:01,22,LOW_CONF

system:

timestamp,event

12:35:22,CAMERA_RECONNECT
XIII. Database Layer

Demo:

SQLite

Lưu:

Count history

Events

KPI history

Review queue

Tương lai:

PostgreSQL
XIV. Report Generator

Xuất:

Daily Report

PDF:

Date: 23/05/2026

Total Count:12540

Uncertain:22

Average FPS:40

Count Accuracy:99.1%

Double Count:0.1%

Biểu đồ:

✓ production

✓ uncertain

✓ runtime

XV. Camera Health Monitoring

Theo dõi:

frame freeze
dropped frames
reconnect
exposure anomaly

Trạng thái:

HEALTHY
WARNING
ERROR
RECONNECTING
XVI. Testing Matrix
Test	Target
Normal	Pass
Overlap nhẹ	Pass
Overlap nặng	Pass
Blur	Pass
Dense	Pass
Occlusion	Pass
Camera reconnect	Pass
Long runtime	Pass
Stress throughput	Pass
XVII. Long Runtime Test

Mục tiêu:

4–8 giờ

Theo dõi:

memory leak
FPS drift
CPU drift
GPU drift
reconnect stability

KPI:

Metric	Target
FPS drop	<5%
Memory increase	<10%
Crash	0
Reconnect success	>99%
XVIII. Deployment Structure
conveyor_system/

    camera/

    preprocessing/

    detection/

    tracking/

    counting/

    fail_safe/

    monitoring/

    ui/

    database/

    logs/

    configs/

    reports/
XIX. Final Deliverables

Người dùng nhận:

✓ Source code

✓ Model

✓ TensorRT engine

✓ Dashboard

✓ Config

✓ Dataset

✓ Logs

✓ Report system

✓ Documentation

✓ Video demo

XX. Kết thúc Phần 7

Đến đây hệ thống đã trở thành:

Camera
    ↓

AI Pipeline
    ↓

Tracking
    ↓

Counting
    ↓

Fail-safe
    ↓

KPI
    ↓

Database
    ↓

Dashboard
    ↓

Operator

Lúc này đây không còn là:

một chương trình detect object

nữa.

Nó đã trở thành:

Industrial Conveyor Monitoring System

với đủ:

phần nhìn
phần vận hành
phần giám sát
phần báo cáo
phần kiểm kê
phần kiểm định hệ thống

# PHẦN 8 — DATA LIFECYCLE + RETRAINING + MAINTENANCE + HANDOVER + FUTURE ROADMAP
I. Mục tiêu phần này

Hệ thống phải:

✓ tiếp tục hoạt động sau demo

✓ học từ lỗi mới

✓ dễ bảo trì

✓ dễ nâng cấp

✓ dễ bàn giao

✓ không phụ thuộc cá nhân viết code

II. Data Lifecycle Architecture

Luồng dữ liệu:

Camera
     ↓

Inference Runtime
     ↓

Event Detection
     ↓

Review Queue
     ↓

Human Validation
     ↓

Dataset Update
     ↓

Retraining
     ↓

Model Validation
     ↓

Deployment

Triết lý:

Hệ thống không đứng yên

↓

Hệ thống liên tục học
III. Runtime Data Collection

Không lưu toàn bộ video 24/7.

Sai lầm phổ biến:

24 giờ video

↓

lưu hết

Kết quả:

Storage đầy rất nhanh

Chỉ lưu:

uncertain events
false positive
false negative
overlap lỗi
camera anomaly

Cấu trúc:

runtime_data/

    uncertain/

    false_positive/

    false_negative/

    overlap_cases/

    camera_errors/

Ví dụ:

uncertain/

    20260523/

        frame_001.png

        meta.json
IV. Metadata Structure

Mỗi sample:

{
"timestamp":"2026-05-23 12:30:22",

"track_id":17,

"reason":"overlap_unresolved",

"confidence":0.42,

"camera":"cam01",

"bbox":[100,200,400,500]
}

Mục tiêu:

✓ trace lỗi

✓ retraining

✓ root-cause analysis

V. Human Review Workflow

Runtime:

UNCERTAIN
     ↓

Review Queue

Người vận hành:

Approve

Reject

Relabel

Ví dụ:

Track17

Reason:

Low confidence

[Object đúng]

[False]

[Need relabel]

Kết quả:

verified_dataset
VI. Dataset Versioning

Không:

dataset_final_v2_new_final_last.zip

Thiết kế:

datasets/

    v1/

    v2/

    v3/

Mỗi version:

v3/

    images/

    labels/

    metadata.json

metadata:

{
"version":"v3",

"samples":1120,

"overlap":310,

"blur":145,

"created":"2026-05-23"
}
VII. Model Versioning

Không:

best_final_final_v3.pt

Thiết kế:

models/

    best_v1.pt

    best_v2.pt

    best_v3.pt

metrics:

{
"precision":0.98,

"recall":0.97,

"count_accuracy":0.992,

"fps":41
}
VIII. Model Registry

Thiết kế:

model_registry/

    active/

    archive/

Ví dụ:

active/

    best_v3.engine

Rollback:

best_v2.engine

Nếu:

best_v3

↓

accuracy giảm

↓

quay lại:

best_v2
IX. Retraining Strategy

Không retrain:

mỗi tuần

Không retrain:

mỗi lỗi nhỏ

Kích hoạt khi:

Điều kiện	Trigger
Accuracy giảm	>2%
Uncertain tăng	>5%
Loại hàng mới	xuất hiện
Overlap tăng	đáng kể

Pipeline:

Collect
    ↓

Review
    ↓

Merge Dataset
    ↓

Train
    ↓

Validate
    ↓

A/B Test
    ↓

Deploy
X. A/B Validation

Không deploy trực tiếp.

Ví dụ:

Model A

Accuracy=99.2
Model B

Accuracy=98.7

Nếu:

B<A

↓

Reject

XI. Maintenance Plan

Hàng ngày:

✓ kiểm tra camera

✓ kiểm tra log lỗi

✓ kiểm tra uncertain

Hàng tuần:

✓ kiểm tra throughput

✓ kiểm tra runtime health

✓ review uncertain samples

Hàng tháng:

✓ đánh giá accuracy

✓ đánh giá drift

✓ đánh giá retrain

XII. Runtime Health Monitoring

Theo dõi:

CPU
GPU
RAM
FPS
camera status
disk usage

Alert:

GPU >90%

↓

Warning

Disk >85%

↓

Warning

Camera disconnected

↓

Critical

XIII. Backup Strategy

Cần backup:

✓ models

✓ configs

✓ datasets

✓ logs

✓ reports

Cấu trúc:

backup/

    daily/

    weekly/

    monthly/
XIV. Documentation Package

Bàn giao:

User Manual

Gồm:

✓ khởi động

✓ dừng

✓ reset

✓ export report

✓ review uncertain

Technical Manual

Gồm:

✓ architecture

✓ configs

✓ tuning

✓ troubleshooting

API Document

Nếu có:

REST API

WebSocket
XV. Training Session

Bàn giao:

Buổi 1

Operator

Nội dung:

✓ chạy hệ thống

✓ thao tác UI

✓ export

✓ xử lý lỗi cơ bản

Buổi 2

Engineer

Nội dung:

✓ cấu hình

✓ retraining

✓ model update

✓ debug

XVI. Future Expansion Roadmap

Phase 1

Detect + Count

Phase 2

Multi-camera

Phase 3

Barcode/OCR

Phase 4

Defect Inspection

Phase 5

MES integration

Phase 6

Cloud monitoring

Phase 7

Predictive analytics
XVII. Final Acceptance KPI
Metric	Target
Count Accuracy	≥99%
Double Count	<0.2%
Miss Count	<0.5%
Uncertain	<2%
FPS	≥35
Camera Recovery	<3 s
Runtime Stability	>8 h
Crash	0
XVIII. Final System Architecture
Camera
    ↓

ROI
    ↓

Adaptive Preprocessing
    ↓

YOLO Detection
    ↓

Overlap Refinement
    ↓

ByteTrack
    ↓

Temporal Consistency
    ↓

State Machine
    ↓

Counting Engine
    ↓

Fail-safe
    ↓

KPI Engine
    ↓

Database
    ↓

Dashboard
    ↓

Operator
    ↓

Review Queue
    ↓

Dataset Update
    ↓

Retraining
XIX. Dự án chính thức khép lại

Đến đây chúng ta không còn có:

một model YOLO

hay:

một đoạn code đếm vật thể

mà đã có:

Industrial Conveyor Object Counting System

bao gồm đầy đủ:

✓ kiến trúc hệ thống
✓ pipeline AI
✓ logic nghiệp vụ
✓ fail-safe
✓ KPI
✓ dashboard
✓ logging
✓ kiểm thử
✓ bàn giao
✓ vòng đời dữ liệu
✓ bảo trì
✓ lộ trình mở rộng

# PHẦN 9 - MULTI-CAMERA SCALE EDITION

Dự án:

Industrial Conveyor Object Counting System — Multi-Camera Scale Platform

Phiên bản:

v2.0 Scale Edition

Mục tiêu:

Scale hệ thống từ:

1 Camera

thành:

16 Camera Concurrent Processing

trong khi vẫn giữ:

Single Count Guarantee
Fail-safe
Real-time
Maintainability
Fault Isolation
PHẦN 1 — MỤC TIÊU HỆ THỐNG
1.1 Functional Objectives

Hệ thống phải:

✓ xử lý đồng thời tối đa 16 camera

✓ hỗ trợ RTSP/USB/IP Camera

✓ detect realtime

✓ tracking realtime

✓ counting realtime

✓ fail-safe

✓ centralized monitoring

✓ quản lý tập trung

✓ không ảnh hưởng chéo giữa camera

1.2 Non-functional Objectives
Hạng mục	KPI
Camera count	≤16
Count accuracy	≥99%
Double count	<0.2%
FPS/camera	≥15
System uptime	>99%
Camera recovery	<3 s
ID switch	<1%
Crash tolerance	camera-level
Runtime	>24 h
PHẦN 2 — KIẾN TRÚC HỆ THỐNG

Từ:

Monolithic Architecture

chuyển sang:

Distributed Service Architecture

Kiến trúc:

Camera Streams
        ↓

Frame Acquisition Layer
        ↓

Message Queue Layer
        ↓

Inference Worker Pool
        ↓

Tracking Service
        ↓

Counting Service
        ↓

Event Bus
        ↓

Storage Layer
        ↓

Dashboard Layer
        ↓

Operator
PHẦN 3 — CAMERA ACQUISITION LAYER

Mỗi camera phải độc lập hoàn toàn.

Cấu trúc:

camera_service/

    camera_manager.py

    stream_reader.py

    reconnect.py

    health_monitor.py

Mỗi camera:

CameraWorker

↓

Frame Queue(maxsize=1)

Ví dụ:

cam01_queue
cam02_queue
cam03_queue
...
cam16_queue

Chức năng:

Stream Input

Hỗ trợ:

RTSP
USB
Video file
IP Camera
Auto-Reconnect

Nếu:

stream disconnected

↓

retry

Retry:

1 s
3 s
5 s
10 s
Health Monitor

Theo dõi:

frozen frame
dropped frame
exposure anomaly
camera latency
PHẦN 4 — MESSAGE QUEUE LAYER

Không cho camera giao tiếp trực tiếp với inference.

Thiết kế:

Camera
    ↓

Frame Queue
    ↓

Message Broker

Đề xuất:

Redis Streams

hoặc:

RabbitMQ

Ví dụ message:

{
"camera":"cam01",
"timestamp":"2026-05-23",
"frame_id":221
}
PHẦN 5 — GPU INFERENCE WORKER POOL

Không:

16 camera

↓

16 YOLO model

Mà:

16 camera
     ↓

GPU Worker Pool

Cấu trúc:

inference/

    worker_1.py

    worker_2.py

    worker_3.py

    worker_4.py

Ví dụ:

workers=4
Dynamic Batching

Input:

cam01 frame
cam02 frame
cam03 frame
cam04 frame

↓

batch infer

↓

GPU

Output:

cam01 result
cam02 result
cam03 result
cam04 result
PHẦN 6 — TRACKING SERVICE

Mỗi camera:

Tracker instance riêng

Ví dụ:

trackers={

"cam01":ByteTrack(),

"cam02":ByteTrack(),

...

"cam16":ByteTrack()

}

Track ID:

Sai:

Track=17

Đúng:

cam03_track17

Track format:

global_track=

camera_id+"_"+track_id
PHẦN 7 — COUNTING SERVICE

Mỗi camera:

Counter()

Registry riêng:

count_registry={

"cam01":set(),

"cam02":set()

}

Count logic:

ENTRY

↓

STABLE

↓

VERIFY

↓

COUNT

Không cho phép:

count twice
PHẦN 8 — EVENT BUS

Không:

count+=1

Thiết kế:

publish(

event="COUNT_COMMITTED",

camera="cam01",

track="cam01_track21"

)

Subscriber:

Dashboard

Logger

Database

Analytics
PHẦN 9 — DATABASE LAYER

Không dùng:

SQLite

Dùng:

PostgreSQL

Schema:

camera

track

count_event

uncertain_event

system_event

Ví dụ:

count_event

camera_id

track_id

timestamp
PHẦN 10 — DASHBOARD

Dashboard:

4×4 grid

Ví dụ:

CAM01 CAM02 CAM03 CAM04

CAM05 CAM06 CAM07 CAM08

CAM09 CAM10 CAM11 CAM12

CAM13 CAM14 CAM15 CAM16

Mỗi tile:

Hiển thị:

✓ live stream

✓ count

✓ FPS

✓ uncertain

✓ health

✓ reconnect status

Click camera:

Mở:

Detailed View

Hiển thị:

✓ events

✓ charts

✓ logs

✓ uncertain samples

PHẦN 11 — RESOURCE SCHEDULER

Theo dõi:

GPU:

utilization
VRAM
FPS

CPU:

usage

RAM:

usage

Disk:

usage

Nếu:

GPU>90%

↓

Adaptive Policy:

giảm inference FPS
giảm resolution
tăng batching
PHẦN 12 — FAILOVER & FAULT ISOLATION

Ví dụ:

CAM07 crash

Không được:

toàn hệ thống crash

Chỉ:

restart CAM07 pipeline

Isolation:

CameraWorker riêng

Tracker riêng

Counter riêng
PHẦN 13 — TESTING MATRIX
Test	Mục tiêu
1 camera	baseline
4 camera	concurrency
8 camera	load
16 camera	stress
reconnect	recovery
long runtime 24h	stability
GPU overload	scheduler
camera failure	isolation
network loss	recovery
PHẦN 14 — DEPLOYMENT TOPOLOGY

Cho 16 camera tôi sẽ không dùng:

1 RTX4060

Đề xuất:

Node1

RTX4070Ti/4080

CAM1–4


Node2

RTX4070Ti/4080

CAM5–8


Node3

RTX4070Ti/4080

CAM9–12


Node4

RTX4070Ti/4080

CAM13–16


Central Server

Dashboard
Database
Monitoring
PHẦN 15 — DELIVERABLES

Bàn giao:

✓ camera service

✓ inference worker pool

✓ tracking service

✓ counting service

✓ event bus

✓ dashboard

✓ PostgreSQL schema

✓ monitoring tools

✓ deployment scripts

✓ Docker compose

✓ documentation

✓ API docs

✓ runtime manuals

KẾT LUẬN

Phiên bản trước:

Industrial Vision Application

Phiên bản scale:

Industrial Vision Platform

Điểm quan trọng nhất là:

Thuật toán lõi

Detect
Track
Count
Fail-safe

giữ nguyên.

Chỉ có:

Runtime architecture

được nâng cấp thành:

Multi-stream distributed architecture

để từ 1 camera có thể đi lên 16 camera mà không phải đập bỏ toàn bộ hệ thống đã xây trước đó.