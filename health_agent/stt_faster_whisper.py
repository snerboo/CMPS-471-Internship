import os
import subprocess
import tempfile


class FasterWhisperSTT:
    def __init__(self, model_size="small", compute_type="int8"):
        self.model_size = model_size
        self.compute_type = compute_type
        self._fw_model = None
        try:
            from faster_whisper import WhisperModel  # type: ignore

            self._fw_model = WhisperModel(model_size, compute_type=compute_type)
        except Exception:
            self._fw_model = None

    def _transcribe_with_faster_whisper(self, filename):
        segments, _ = self._fw_model.transcribe(filename, vad_filter=True)
        text_parts = [seg.text.strip() for seg in segments if seg.text and seg.text.strip()]
        return " ".join(text_parts).strip()

    def _transcribe_with_whisper_cli(self, filename):
        cli_path = "./whisper.cpp/build/bin/whisper-cli"
        model_path = "./whisper.cpp/models/ggml-base.en.bin"
        if not os.path.exists(cli_path) or not os.path.exists(model_path):
            raise FileNotFoundError(
                "No STT backend available. Install faster-whisper or build whisper.cpp binary and model."
            )

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as out:
            out_path = out.name

        try:
            cmd = [
                cli_path,
                "-m",
                model_path,
                "-f",
                filename,
                "-nt",
                "-of",
                out_path,
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            txt_file = f"{out_path}.txt"
            if os.path.exists(txt_file):
                with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read().strip()
            return ""
        finally:
            for path in (out_path, f"{out_path}.txt"):
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

    def transcribe(self, filename):
        if self._fw_model is not None:
            return self._transcribe_with_faster_whisper(filename)
        return self._transcribe_with_whisper_cli(filename)
