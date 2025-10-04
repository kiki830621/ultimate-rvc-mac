#!/bin/bash
# Ultimate RVC launcher for macOS
# Optimized for Apple Silicon with MPS (Metal Performance Shaders) GPU acceleration

VENV_PATH=.venv

# Detect Mac architecture and GPU capabilities
detect_mac_architecture() {
    ARCH=$(uname -m)
    if [ "$ARCH" = "arm64" ]; then
        echo "🍎 Detected: Apple Silicon (M1/M2/M3/M4)"
        echo "✨ MPS (Metal) GPU acceleration: ENABLED"
    else
        echo "🍎 Detected: Intel Mac"
        echo "⚡ Running in CPU mode (MPS not available)"
    fi
}

main() {
    command=$1
    shift
    case $command in
        run)
            check_dependencies
            detect_mac_architecture
            /Users/che/.local/bin/uv run ./src/ultimate_rvc/web/main.py "$@"
            ;;
        cli)
            check_dependencies
            detect_mac_architecture
            /Users/che/.local/bin/uv run ./src/ultimate_rvc/cli/main.py "$@"
            ;;
        update)
            git pull
            /Users/che/.local/bin/uv sync
            ;;
        benchmark)
            check_dependencies
            echo "=== macOS Performance Benchmark ==="
            python3 -c "import torch; print(f'PyTorch Version: {torch.__version__}'); print(f'Device: {\"MPS (GPU)\" if torch.backends.mps.is_available() else \"CPU\"}'); print(f'MPS Built: {torch.backends.mps.is_built()}')"
            ;;
        help)
            show_help
            ;;
        *)
            cat <<- EOF
			Invalid command.
			Use './urvc-macos.sh help' to see available commands.
			EOF
            exit 1
            ;;
    esac
}

check_dependencies() {
    if [ ! -d "$VENV_PATH" ]; then
        echo "Dependencies not found. Please run 'uv sync' first."
        exit 1
    fi
}

show_help() {
	cat <<- EOF

	Ultimate RVC - macOS 啟動器 (CPU 模式)

	用法: ./urvc-macos.sh [命令] [選項]

	命令:
	  run          啟動 Ultimate RVC 網頁介面
	                 啟動後請開啟: http://127.0.0.1:7860
	  cli          啟動 CLI 命令列模式
	                 選項:
	                   --help     顯示說明並離開
	  update       更新到最新版本
	  help         顯示此說明訊息

	範例:
	  ./urvc-macos.sh run         # 啟動網頁介面
	  ./urvc-macos.sh cli --help  # 查看 CLI 選項

	注意:
	  - macOS 僅支援 CPU 模式，處理速度會較慢
	  - 需要穩定的網路連線下載模型
	  - 首次啟動會下載必要的 AI 模型

	EOF
}

main "$@"
