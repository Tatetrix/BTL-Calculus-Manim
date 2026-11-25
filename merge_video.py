import os
from pathlib import Path
import subprocess


def merge_manim_videos(video_dir="media/videos/manim-2/480p15", output_name="full_video.mp4"):
    dir_path = Path(video_dir)

    if not dir_path.exists():
        print(f"[-] Không tìm thấy thư mục: {dir_path}")
        print("Hãy chắc chắn bạn đã chạy Manim để render các scene trước đó.")
        return

    # Lấy danh sách tất cả các file .mp4 bắt đầu bằng S (hoặc tất cả file mp4) và sắp xếp theo tên
    video_files = sorted([f for f in dir_path.glob("S*.mp4")])

    if not video_files:
        print(f"[-] Không tìm thấy file video S*.mp4 nào trong {dir_path}")
        return

    print(f"[+] Tìm thấy {len(video_files)} video đoạn:")
    for vf in video_files:
        print(f"    - {vf.name}")

    # Tạo file danh sách list.txt theo chuẩn concat của ffmpeg
    list_file_path = dir_path / "list.txt"
    with open(list_file_path, "w", encoding="utf-8") as f:
        for vf in video_files:
            # Dùng đường dẫn tương đối hoặc tên file
            f.write(f"file '{vf.name}'\n")

    output_path = dir_path / output_name

    # Lệnh ffmpeg gộp video không cần encode lại (cực nhanh)
    cmd = [
        "ffmpeg",
        "-y",                      # Ghi đè file cũ nếu có
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file_path),
        "-c", "copy",              # Copy trực tiếp luồng video/audio giữ nguyên chất lượng
        str(output_path)
    ]

    print(f"\n[*] Đang tiến hành gộp video thành '{output_name}'...")
    try:
        subprocess.run(cmd, check=True)
        print(f"[SUCCESS] Đã gộp thành công! File lưu tại: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Lỗi khi chạy ffmpeg: {e}")
    except FileNotFoundError:
        print("[-] Không tìm thấy lệnh 'ffmpeg'. Hãy đảm bảo máy tính đã cài ffmpeg và thêm vào biến môi trường (PATH).")

    # Dọn dẹp file list.txt tạm thời
    if list_file_path.exists():
        os.remove(list_file_path)


if __name__ == "__main__":
    # Bạn có thể thay đổi đường dẫn thư mục tùy theo độ phân giải bạn render (ví dụ: '1080p60')
    target_dir = "media/videos/manim-2/480p15"
    merge_manim_videos(video_dir=target_dir)
