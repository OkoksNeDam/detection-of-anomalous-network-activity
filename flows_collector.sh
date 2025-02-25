#!/bin/bash

while [ $# -gt 0 ]
do
    key=$1
    case $key in
        --i)
            # Указанный интерфейс.
            INTERFACE=$2
            ;;
        --outdir)
            # Папка для сохранения файлов.
            OUTPUT_DIR=$2
            ;;
        --capture_time)
            # Время захвата трафика в секундах.
            TRAFFIC_CAPTURE_TIME=$2
            ;;
    esac
    shift 2
done

# Временный файл для захвата всего трафика
CAPTURE_FILE="temp_capture.pcap"

mkdir -p "$OUTPUT_DIR"

# Захватываем весь трафик в один файл.
tshark -i "$INTERFACE" -w "$CAPTURE_FILE" -f "tcp" -a duration:$TRAFFIC_CAPTURE_TIME

# Получаем список уникальных потоков
streams=$(tshark -r "$CAPTURE_FILE" -T fields -e tcp.stream | sort -u)
echo Создаем файлы pcap...
for stream in $streams; 
do
    output_file="$OUTPUT_DIR/flow_$stream.pcap"
    # Создание файла для потока stream.
    tshark -r "$CAPTURE_FILE" -Y "tcp.stream eq $stream" -w "$output_file"
done

# Удаление временного файла CAPTURE_FILE.
rm -f "$CAPTURE_FILE"

echo done!