{pkgs}: {
  deps = [
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.libuv
    pkgs.cacert
    pkgs.glibcLocales
    pkgs.libxcrypt
  ];
}
