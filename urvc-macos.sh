#!/bin/bash
# Ultimate RVC launcher for macOS
# CPU-only mode (no CUDA support)

VENV_PATH=.venv

main() {
    command=$1
    shift
    case $command in
        run)
            check_dependencies
            /Users/che/.local/bin/uv run ./src/ultimate_rvc/web/main.py "$@"
            ;;
        cli)
            check_dependencies
            /Users/che/.local/bin/uv run ./src/ultimate_rvc/cli/main.py "$@"
            ;;
        update)
            git pull
            /Users/che/.local/bin/uv sync
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
