# Todo: use system ffmpeg (patches)
# libdca/dcadec?

Name:           avidemux
Version:        2.6.15
Release:        1%{?dist}
Summary:        Free video editor designed for simple cutting, filtering and encoding tasks
License:        GPLv2
URL:            http://fixounet.free.fr/avidemux/

Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{version}.tar.gz
Patch0:         %{name}-2.6.15-system-libs.patch

BuildRequires:  a52dec-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  faac-devel
BuildRequires:  faad2-devel
#BuildRequires:  ffmpeg-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gettext intltool
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  js-devel
BuildRequires:  lame-devel
BuildRequires:  libass-devel
BuildRequires:  libfdk-aac-devel
BuildRequires:  libmad-devel
BuildRequires:  libogg-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libvpx-devel
BuildRequires:  libxml2-devel
BuildRequires:  libXmu-devel
BuildRequires:  libxslt
BuildRequires:  libxslt
BuildRequires:  libXv-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  nvenc
BuildRequires:  opencore-amr-devel
BuildRequires:  opus-devel
BuildRequires:  pkgconfig
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  SDL2-devel
BuildRequires:  sqlite-devel
BuildRequires:  twolame-devel
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  xvidcore-devel
BuildRequires:  yasm-devel

Provides:       bundled(ffmpeg) = 3.0.3

%description
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible MPEG
files, MP4 and ASF, using a variety of codecs. Tasks can be automated using
projects, job queue and powerful scripting capabilities.

%package devel
Summary:    Development files for Avidemux
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%setup -qn %{name}_%{version}
%patch0 -p1

# Remove bundled libraries
rm -fr \
    avidemux_plugins/ADM_audioDecoders/ADM_ad_ac3/ADM_liba52 \
    avidemux_plugins/ADM_audioDecoders/ADM_ad_mad/ADM_libMad \
    avidemux_plugins/ADM_audioEncoders/twolame/ADM_libtwolame \
    avidemux_plugins/ADM_videoFilters6/ass/ADM_libass

# rpmlint fixes
find . -name "*.swp" -delete
find . -name "*.cpp" -exec chmod 644 {} \;
find . -name "*.h" -exec chmod 644 {} \;
sed -i \
    -e '/Encoding=UTF-8/d' \
    -e 's/Categories=Application;AudioVideo/Categories=AudioVideo;/g' \
    -e 's/Exec=avidemux2_gtk/Exec=avidemux3_qt5/g' \
    *.desktop

%build
# Get the actual components to be built with the official build command:
# bash -x bootStrap.bash --with-core --with-cli --with-plugins

prep() {
export CFLAGS="%{optflags} -I%{_includedir}/nvenc"
%cmake \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DFAKEROOT=%{_builddir}/%{name}_%{version}/install \
    -DENABLE_QT5=True \
    -DCMAKE_EDIT_COMMAND=vim \
    -DNVENC_INCLUDE_DIR=%{_includedir}/nvenc \
    $*
}

build() {
# Make headers available to the other components
make \
    INSTALL="install -p" \
    DESTDIR=%{_builddir}/%{name}_%{version}/install \
    install \
    $*
}

mkdir buildCore; pushd buildCore
prep ../avidemux_core
build
popd

mkdir buildQt5; pushd buildQt5
prep ../avidemux/qt4
build
popd

mkdir buildCli; pushd buildCli
prep ../avidemux/cli
build
popd

mkdir buildPluginsCommon; pushd buildPluginsCommon
prep -DPLUGIN_UI=COMMON ../avidemux_plugins
build
popd

mkdir buildPluginsQt5; pushd buildPluginsQt5
prep -DPLUGIN_UI=QT4 ../avidemux_plugins
popd

mkdir buildPluginsCLI; pushd buildPluginsCLI
prep -DPLUGIN_UI=CLI ../avidemux_plugins
build
popd

mkdir buildPluginsSettings; pushd buildPluginsSettings
prep -DPLUGIN_UI=SETTINGS ../avidemux_plugins
build
popd

%install
cp -pa install/* %{buildroot}/

install -p -Dm 644 man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -p -Dm 644 %{name}_icon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -p -Dm 644 %{name}2.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# rpmlint fixes
chmod 755 %{buildroot}%{_libdir}/*.so*

%post
/sbin/ldconfig
%if 0%{?fedora} == 23 || 0%{?rhel}
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%endif
%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel}
%{_bindir}/update-desktop-database &> /dev/null || :
%endif

%postun
/sbin/ldconfig
%if 0%{?fedora} == 23 || 0%{?rhel}
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%endif
%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel}
%{_bindir}/update-desktop-database &> /dev/null || :
%endif

%files
%license COPYING 
%doc README AUTHORS
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}6
%{_datadir}/pixmaps/%{name}.png
%{_libdir}/*
%{_mandir}/man1/*

%files devel
%{_includedir}/%{name}

%changelog
* Sun Nov 20 2016 Simone Caronni <negativo17@gmail.com> - 2.6.15-1
- First build.
