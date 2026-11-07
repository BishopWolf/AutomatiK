#!/bin/bash
cd "$(dirname "$0")" || exit 1

CONKY_BIN="${CONKY_BIN:-}"
if [[ -z "$CONKY_BIN" ]]; then
	if [[ "${XDG_SESSION_TYPE:-}" == "wayland" && -x "$HOME/.local/opt/conky-1.24.2/usr/bin/conky" ]]; then
		CONKY_BIN="$HOME/.local/opt/conky-1.24.2/usr/bin/conky"
		CONKY_LIBDIR="$HOME/.local/opt/conky-1.24.2/usr/lib/conky"
		export CONKY_LIBDIR
	else
		CONKY_BIN="$(command -v conky)"
	fi
fi

if [[ -z "$CONKY_BIN" || ! -x "$CONKY_BIN" ]]; then
	printf 'Conky executable not found. Set CONKY_BIN to a valid executable.\n' >&2
	exit 1
fi

for config in infofile clockfile memfile cpufile topfile diskfile netfile graphiccardfile; do
	pkill -KILL -f "[c]onky .* -c .*/AutomatiK/${config}" 2>/dev/null || true
done
pkill -f "[p]ython3 poll_disk.py" 2>/dev/null || true
pkill -f "[p]ython3 poll_day.py" 2>/dev/null || true

mkdir -p ~/.fonts ~/.local/share/fonts
cp fonts/*.*tf ~/.fonts/ 2>/dev/null
cp fonts/*.*tf ~/.local/share/fonts/ 2>/dev/null
fc-cache -f ~/.fonts 2>/dev/null

python3 info01.py
python3 clock01.py
python3 mem01.py
python3 cpu01.py
python3 disk01.py
python3 top01.py
python3 net01.py
python3 graphiccard01.py

if [[ ! -f "$PWD/libwayland_argb_fix.so" || "$PWD/wayland_argb_fix.c" -nt "$PWD/libwayland_argb_fix.so" ]]; then
	gcc -O2 -shared -fPIC "$PWD/wayland_argb_fix.c" -o "$PWD/libwayland_argb_fix.so" $(pkg-config --cflags --libs x11 cairo imlib2) -ldl 2>/dev/null || true
fi
if [[ -f "$PWD/libwayland_argb_fix.so" ]]; then
	export LD_PRELOAD="$PWD/libwayland_argb_fix.so${LD_PRELOAD:+:$LD_PRELOAD}"
fi

"$CONKY_BIN" -q -d -c "$PWD/infofile"
"$CONKY_BIN" -q -d -c "$PWD/clockfile"
"$CONKY_BIN" -q -d -c "$PWD/memfile"
"$CONKY_BIN" -q -d -c "$PWD/cpufile"
"$CONKY_BIN" -q -d -c "$PWD/topfile"
"$CONKY_BIN" -q -d -c "$PWD/diskfile"
"$CONKY_BIN" -q -d -c "$PWD/netfile"
"$CONKY_BIN" -q -d -c "$PWD/graphiccardfile"

unset LD_PRELOAD

python3 poll_disk.py &
python3 poll_day.py &

notify-send -i ~/AutomatiK/AutomatiK.png \
"Information" \
"Automatik is started
To move the widgets around the desktop,
use Alt+ left-Click"
