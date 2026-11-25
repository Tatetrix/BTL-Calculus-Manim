import re
import subprocess
from pathlib import Path

# ================= CẤU HÌNH =================
# 1.10 -> tăng tốc 10% (giữ nguyên tông giọng) để tổng video < 10 phút (~9:45)
# 1.00 -> giữ tốc độ gốc (ghép xong trong ~2 giây nếu cùng độ phân giải)
SPEED = 1.10

OUTPUT_NAME = "Final_Calculus1_Group4.mp4"
# ============================================

SCRIPT_DIR = Path(__file__).resolve().parent
SCENE_RE = re.compile(r"^scene0?([1-8])\.mp4$", re.IGNORECASE)


def find_scenes():
    found = {}
    for p in SCRIPT_DIR.rglob("*.mp4"):
        if "partial_movie_files" in p.parts or p.name == OUTPUT_NAME:
            continue
        m = SCENE_RE.match(p.name)
        if not m:
            continue
        idx = int(m.group(1))
        # Nếu có nhiều bản của cùng 1 scene, tự lấy file mới render nhất
        if idx not in found or p.stat().st_mtime > found[idx].stat().st_mtime:
            found[idx] = p

    missing = []
    for i in range(1, 9):
        if i in found:
            print(f"  [OK]    Scene 0{i}: {found[i].relative_to(SCRIPT_DIR)}")
        else:
            print(f"  [THIẾU] Scene 0{i}")
            missing.append(f"Scene0{i}.mp4")

    if missing:
        raise FileNotFoundError("Không tìm thấy: " + ", ".join(missing))

    return [found[i] for i in range(1, 9)]


def probe_video(path: Path):
    try:
        res = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height,r_frame_rate",
                "-of", "csv=p=0",
                str(path),
            ],
            capture_output=True, text=True, check=True,
        )
        w, h, fps = res.stdout.strip().split(",")
        return int(w), int(h), fps
    except Exception:
        return None


def get_duration(path: Path):
    try:
        res = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True, text=True, check=True,
        )
        return float(res.stdout.strip())
    except Exception:
        return None


def run_ffmpeg_with_fallback(base_args, filter_args, map_args, output_file):
    cmd_gpu = [
        "ffmpeg", "-y", *base_args, *filter_args, *map_args,
        "-c:v", "h264_nvenc", "-preset", "p4", "-cq", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_file),
    ]
    try:
        print("\nĐang xuất bằng GPU NVIDIA (NVENC)...")
        subprocess.run(cmd_gpu, check=True)
    except subprocess.CalledProcessError:
        print("\nKhông bật được NVENC -> chuyển sang CPU (libx264 veryfast)...")
        cmd_cpu = [
            "ffmpeg", "-y", *base_args, *filter_args, *map_args,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(output_file),
        ]
        subprocess.run(cmd_cpu, check=True)


def main():
    print("Đang quét 8 file Scene01.mp4 -> Scene08.mp4...")
    videos = find_scenes()
    output_file = SCRIPT_DIR / OUTPUT_NAME

    infos = [probe_video(v) for v in videos]
    same_format = all(infos) and len(set(infos)) == 1

    if same_format:
        list_file = SCRIPT_DIR / "_concat_list.txt"
        with open(list_file, "w", encoding="utf-8") as f:
            for v in videos:
                f.write(f"file '{v.as_posix()}'\n")
        try:
            if abs(SPEED - 1.0) < 1e-3:
                print("\nĐang ghép nhanh không nén lại (1.0x)...")
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(list_file), "-c", "copy",
                        "-movflags", "+faststart", str(output_file),
                    ],
                    check=True,
                )
            else:
                run_ffmpeg_with_fallback(
                    ["-f", "concat", "-safe", "0", "-i", str(list_file)],
                    ["-vf", f"setpts=PTS/{SPEED}", "-af",
                        f"aresample=async=1,atempo={SPEED}"],
                    [],
                    output_file,
                )
        finally:
            if list_file.exists():
                list_file.unlink()
    else:
        # Tự động chuẩn hóa nếu 8 scene có độ phân giải / fps khác nhau
        valid = [x for x in infos if x]
        target_w, target_h, target_fps = max(
            valid, key=lambda x: x[0] * x[1]) if valid else (1920, 1080, "30/1")
        print(
            f"\nPhát hiện các scene khác độ phân giải/fps -> tự chuẩn hóa về {target_w}x{target_h}...")

        base_args = []
        filters = []
        concat_inputs = []
        for i, v in enumerate(videos):
            base_args.extend(["-i", str(v)])
            filters.append(
                f"[{i}:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2,fps={target_fps},setsar=1[v{i}]"
            )
            filters.append(
                f"[{i}:a]aresample=44100,aformat=channel_layouts=stereo[a{i}]")
            concat_inputs.append(f"[v{i}][a{i}]")

        filters.append(
            f"{''.join(concat_inputs)}concat=n=8:v=1:a=1[vcat][acat]")
        if abs(SPEED - 1.0) < 1e-3:
            v_out, a_out = "[vcat]", "[acat]"
        else:
            filters.append(f"[vcat]setpts=PTS/{SPEED}[vout]")
            filters.append(f"[acat]atempo={SPEED}[aout]")
            v_out, a_out = "[vout]", "[aout]"

        run_ffmpeg_with_fallback(
            base_args,
            ["-filter_complex", ";".join(filters)],
            ["-map", v_out, "-map", a_out],
            output_file,
        )

    dur = get_duration(output_file)
    print(f"\nXONG! File xuất ra: {output_file}")
    if dur:
        mins, secs = divmod(dur, 60)
        print(f"Tổng thời lượng: {int(mins)}:{secs:05.2f} ({dur:.1f}s)")


if __name__ == "__main__":
    main()
