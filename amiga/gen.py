#!/usr/bin/env python3
"""gen.py OUTDIR: the files Meson would generate for the Amiga build, made
without Meson.

- Config.h from src/Config.template.h, with the values the Amiga build
  takes (no HTTP, no Lua, no platform clipboard, no installer, data beside
  the program);
- VcsTag.h (no tag);
- ElementNumbers.h and ToolNumbers.h: the element and tool lists, read from
  src/simulation/elements/meson.build and src/simulation/simtools/meson.build;
- the embedded resources (font, save icons, credits) as NAME.cpp/NAME.h,
  laid out as upstream's resources/to-array.py lays them out.

The AmiCradle Team. GPL 3 or later, like The Powder Toy."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

VERSION = re.search(r"version:.*?'(\d+\.\d+\.\d+)'", (ROOT / "meson.build").read_text(), re.S).group(1)
MAJOR, MINOR, BUILD = VERSION.split(".")

CONFIG = {
    "SET_WINDOW_ICON": "false",
    "DEBUG": "false",
    "X86_KILL_DENORMALS": "false",
    "BETA": "false",
    "SNAPSHOT": "false",
    "MOD": "false",
    "NOHTTP": "true",
    "LUACONSOLE": "false",
    "ALLOW_FAKE_NEWER_VERSION": "false",
    "USE_UPDATESERVER": "false",
    "CAN_INSTALL": "false",
    "SHARED_DATA_FOLDER": "false",
    "USE_BLUESCREEN": "false",
    "INSTALL_CHECK": "false",
    "IGNORE_UPDATES": "true",
    "ENFORCE_HTTPS": "true",
    "SECURE_CIPHERS_ONLY": "false",
    "PLATFORM_CLIPBOARD": "false",
    "USE_SYSTEM_CERT_PROVIDER": "false",
    "FFTW_PLAN_MEASURE": "true",
    "ALLOW_QUIT": "true",
    "DEFAULT_TOUCH_UI": "false",
    "ALLOW_DATA_FOLDER": "true",
    "PATH_SEP_CHAR": "/",
    "FORCE_WINDOW_FRAME_OPS": "forceWindowFrameOpsNone",
    "SERVER": "https://powdertoy.co.uk",
    "STATICSERVER": "https://static.powdertoy.co.uk",
    "UPDATESERVER": "",
    "IDENT_PLATFORM": "UNKNOWN",
    "IDENT": "M68K-AMIGAOS-LIBNIX",
    "APPNAME": "The Powder Toy",
    "APPCOMMENT": "Physics sandbox game",
    "APPEXE": "powder",
    "APPID": "uk.co.powdertoy.tpt",
    "APPDATA": "The Powder Toy",
    "APPVENDOR": "powdertoy",
    "PACKAGE_MODE": "default",
    "MOD_ID": "0",
    "DISPLAY_VERSION_MAJOR": MAJOR,
    "DISPLAY_VERSION_MINOR": MINOR,
    "BUILD_NUM": BUILD,
    "UPSTREAM_VERSION_MAJOR": MAJOR,
    "UPSTREAM_VERSION_MINOR": MINOR,
    "UPSTREAM_BUILD_NUM": BUILD,
}


def write(name, text):
    path = OUT / name
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def configure(template, values):
    def sub(m):
        if m.group(1) not in values:
            raise SystemExit(f"{template}: no value for @{m.group(1)}@")
        return values[m.group(1)]
    return re.sub(r"@([A-Za-z_0-9]+)@", sub, template.read_text())


def numbered(meson, list_name):
    """[(NAME, id)] from a meson list of names, as the meson loops number them."""
    text = meson.read_text()
    body = re.search(list_name + r"\s*=\s*\[(.*?)\]", text, re.S).group(1)
    return [(name, i) for i, name in enumerate(re.findall(r"'([A-Z0-9_]+)'", body))]


write("Config.h", configure(SRC / "Config.template.h", CONFIG))
write("VcsTag.h", configure(SRC / "VcsTag.template.h", {"VCS_TAG": ""}))

elements = numbered(SRC / "simulation/elements/meson.build", "simulation_elem_names")
tools = numbered(SRC / "simulation/simtools/meson.build", "simulation_tool_names")
write("ElementNumbers.h", configure(SRC / "simulation/ElementNumbers.template.h", {
    "element_numbers": "\n\t".join(f"X({n}, {i}) \\" for n, i in elements)}))
write("ToolNumbers.h", configure(SRC / "simulation/ToolNumbers.template.h", {
    "tool_numbers": "\n\t".join(f"X({n}, {i}) \\" for n, i in tools)}))
# the element and tool sources, for the Makefile
write("elements.mk", "ELEMENT_SRC = " + " ".join(
    f"src/simulation/elements/{n}.cpp" for n, _ in elements) + "\n" +
    "TOOL_SRC = " + " ".join(f"src/simulation/simtools/{n}.cpp" for n, _ in tools) + "\n")

for name, rel in [("save_local_png", "resources/save_local.png"),
                  ("save_online_png", "resources/save_online.png"),
                  ("font_bz2", "resources/font.bz2"),
                  ("credits_json", "resources/credits.json")]:
    data = (ROOT / rel).read_bytes()
    write(f"{name}.h", f"""
#pragma once
#include <array>
#include <span>

extern const struct {name}Resource
{{
	std::array<unsigned char, {len(data)}> data;

	std::span<const char> AsCharSpan() const
	{{
		return std::span(reinterpret_cast<const char *>(data.data()), data.size());
	}}

	std::span<const unsigned char> AsUcharSpan() const
	{{
		return std::span(data.data(), data.size());
	}}
}} {name};
""")
    write(f"{name}.cpp", f"""
#include "{name}.h"

const struct {name}Resource {name} = {{{{{{ {", ".join(str(b) for b in data)} }}}}}};
""")
