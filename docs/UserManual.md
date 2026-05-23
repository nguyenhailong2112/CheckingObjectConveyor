# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG

## A. Cảnh báo quan trọng (bắt buộc đọc)

Tài liệu này tách rõ 2 chế độ:

1. **Chế độ KIỂM TRA LOGIC PoC (simulation/stub)**
   - Mục đích: kiểm tra code có chạy đúng theo thiết kế phần mềm.
   - Không đại diện cho hiệu năng/độ chính xác hiện trường.

2. **Chế độ VẬN HÀNH THỰC TẾ (production runtime)**
   - Mục đích: chạy camera + model thật + dữ liệu thật.
   - Repo hiện tại **chưa tích hợp đầy đủ** phần này.

---

## B. Chạy ở trạng thái hiện tại của repo

### B1) Kiểm tra logic phần mềm

```bash
python tests/test_suite_runner.py
# hoặc
pytest -q
```

Ý nghĩa:
- Chỉ xác nhận các logic code/module contract đang đúng.
- Không chứng minh độ chính xác đếm thực tế trên line.

### B2) Chạy mô phỏng preflight/demo

```bash
python scripts/preflight_check.py
python scripts/run_demo_session.py
```

Ý nghĩa:
- Chạy flow mô phỏng để kiểm tra orchestration.
- Không phải phiên bản production runtime hiện trường.

---

## C. Vận hành thực tế cần gì (chưa có sẵn trong repo)

Để chạy production thật, cần bổ sung:
1. Model weights (YOLO/TensorRT/ONNX...) + loader thật
2. Camera source thật (RTSP/USB/industrial camera)
3. Video dữ liệu test/validation thật
4. Ground-truth evaluator để đo Count Accuracy/Double Count/Miss Count

Nếu chưa có 4 mục trên, tuyệt đối không gọi là “vận hành thực tế”.

---

## D. Checklist trước khi nghiệm thu hiện trường

- [ ] Có model weights production
- [ ] Có camera/video thật
- [ ] Có ROI/zone calibrate theo line
- [ ] Có KPI đo trên ground-truth thật
- [ ] Có log runtime đầy đủ phiên chạy dài giờ



## Runtime thực tế
Xem tài liệu: `REAL_RUNTIME_QUICKSTART.md` để chạy model + camera/video thật.