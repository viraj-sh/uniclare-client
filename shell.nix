{ pkgs ? import <nixpkgs> { } }:

let
  runtimeLibs = with pkgs; [
    # Base
    stdenv.cc.cc.lib
    zlib
    zstd
    brotli

    # GL / graphics
    libGL
    libglvnd # libEGL
    libgbm
    libdrm
    vulkan-loader

    # Wayland / input
    wayland
    libxkbcommon

    # X11
    libx11
    libxext
    libxrandr
    libxcomposite
    libxdamage
    libxfixes
    libxrender
    libxi
    libxcursor
    libxtst
    libxkbfile
    libxshmfence

    # xcb
    libxcb
    libxcb-util
    libxcb-cursor
    libxcb-wm
    libxcb-image
    libxcb-keysyms
    libxcb-render-util

    # GTK stack / fonts
    glib
    gtk3
    gdk-pixbuf
    pango
    cairo
    atk
    at-spi2-atk
    harfbuzz
    fontconfig
    freetype

    # QtWebEngine / Chromium
    dbus
    expat
    nss
    nspr
    cups
    alsa-lib
    libpulseaudio
    krb5
    icu
    libpng
    libjpeg
    libwebp
    libxml2
    libxslt
    lcms2
    libopus
    libevent
    minizip
    snappy
  ];
in
pkgs.mkShell {
  packages = [ pkgs.uv ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath runtimeLibs;

  # --pure sets this to a nonexistent file, which breaks httpx
  SSL_CERT_FILE = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";

  QTWEBENGINE_DISABLE_SANDBOX = "1";
  PYWEBVIEW_GUI = "qt";
}