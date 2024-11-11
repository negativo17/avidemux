#global tag %{version}

%global commit0 7baa0b8ab6b8d4dce316830832fc9d59bfa01a09
%global date 20241101
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global commit1 b91c7f7c26577e5be005b094604f813058c31682
%global date 20240815
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

%global __cmake_in_source_build 1
%global _lto_cflags %{nil}

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%global org org.avidemux.Avidemux

Name:           avidemux
Version:        2.8.2%{!?tag:^%{date}git%{shortcommit0}}
Release:        1%{?dist}
Epoch:          1
Summary:        Free video editor designed for simple cutting, filtering and encoding tasks
License:        GPLv2
URL:            http://fixounet.free.fr/%{name}/

%if 0%{?tag:1}
Source0:        https://github.com/mean00/avidemux2/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/mean00/avidemux2_i18n/archive/%{version}/%{name}_i18n-%{version}.tar.gz
%else
Source0:        https://github.com/mean00/avidemux2/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:        https://github.com/mean00/avidemux2_i18n/archive/%{commit1}.tar.gz#/%{name}_i18n-%{shortcommit1}.tar.gz
%endif

BuildRequires:  a52dec-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  lame-devel
BuildRequires:  libaom-devel
BuildRequires:  libappstream-glib
BuildRequires:  libass-devel
BuildRequires:  libfdk-aac-devel
BuildRequires:  libmad-devel
BuildRequires:  libmp4v2-devel
BuildRequires:  libogg-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libvpx-devel >= 1.7.0
BuildRequires:  libxml2-devel
BuildRequires:  libXmu-devel
BuildRequires:  libxslt
BuildRequires:  libXv-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  nv-codec-headers
BuildRequires:  opencore-amr-devel
BuildRequires:  opus-devel
BuildRequires:  pkgconfig
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-linguist
BuildRequires:  SDL2-devel
BuildRequires:  sqlite-devel
BuildRequires:  twolame-devel
BuildRequires:  vapoursynth-devel
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  xvidcore-devel

%ifarch x86_64
BuildRequires:  yasm
%endif

%description
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible MPEG
files, MP4 and ASF, using a variety of codecs. Tasks can be automated using
projects, job queue and powerful scripting capabilities.

%package libs
Summary:    Base libraries for Avidemux
Provides:   bundled(ffmpeg) = 4.4.1

%description libs
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible MPEG
files, MP4 and ASF, using a variety of codecs. Tasks can be automated using
projects, job queue and powerful scripting capabilities.

This package contains the base libraries.

%package cli
Summary:    Command line interface for Avidemux

%description cli
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible MPEG
files, MP4 and ASF, using a variety of codecs. Tasks can be automated using
projects, job queue and powerful scripting capabilities.

This package contains the command line interface.

%package gui
Summary:    Graphical interface for Avidemux
Obsoletes:  %{name}-gtk < %{epoch}:%{version}-%{release}
Provides:   %{name}-gtk = %{epoch}:%{version}-%{release}
Obsoletes:  %{name}-i18n < %{epoch}:%{version}-%{release}
Provides:   %{name}-i18n = %{epoch}:%{version}-%{release}
Obsoletes:  %{name}-qt < %{epoch}:%{version}-%{release}
Provides:   %{name}-qt = %{epoch}:%{version}-%{release}
Obsoletes:  %{name} < %{epoch}:%{version}-%{release}
Provides:   %{name} = %{epoch}:%{version}-%{release}

%description gui
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible MPEG
files, MP4 and ASF, using a variety of codecs. Tasks can be automated using
projects, job queue and powerful scripting capabilities.

This package contains the graphical interface.

%prep
%setup -q -T -c -n %{name}-%{version}
tar --strip 1 -xzf %{SOURCE0}
tar --strip 1 -C avidemux/qt4/i18n -xzf %{SOURCE1}

# Remove bundled libraries
rm -fr \
    avidemux_plugins/ADM_audioDecoders/ADM_ad_ac3/ADM_liba52 \
    avidemux_plugins/ADM_audioDecoders/ADM_ad_mad/ADM_libMad \
    avidemux_plugins/ADM_audioEncoders/twolame/ADM_libtwolame \
    avidemux_plugins/ADM_muxers/muxerMp4v2/libmp4v2 \
    avidemux_plugins/ADM_videoFilters6/ass/ADM_libass

# rpmlint fixes
find . -name "*.swp" -delete
find . -name "*.cpp" -exec chmod 644 {} \;
find . -name "*.h" -exec chmod 644 {} \;

%build

# Get the actual components to be built with the official build command:
# bash -x ./bootStrap.bash \
#     --with-core \
#     --with-cli \
#     --with-qt \
#     --with-plugins \
#     --with-system-libass \
#     --with-system-liba52 \
#     --with-system-libmad \
#     --with-system-libmp4v2

prep() {
%cmake \
    -DAVIDEMUX_SOURCE_DIR=%{_builddir}/%{name}-%{version} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_EDIT_COMMAND=vim \
    -DENABLE_QT6=True \
    -DFAKEROOT=%{_builddir}/%{name}-%{version}/install \
    -DNVENC_INCLUDE_DIR=%{_includedir}/nvenc \
    -DOpenGL_GL_PREFERENCE=GLVND \
    -DUSE_EXTERNAL_LIBASS=true \
    -DUSE_EXTERNAL_LIBMAD=true \
    -DUSE_EXTERNAL_LIBA52=true \
    -DUSE_EXTERNAL_MP4V2=true \
    $*
}

build() {
# Headers need to be installed prior to compiling other components and Makefiles
# are not generated properly with other targets
%make_build \
    INSTALL="install -p" \
    DESTDIR=%{_builddir}/%{name}-%{version}/install \
    install \
    $*
}

mkdir build_core
pushd build_core
prep ../avidemux_core
build
popd

mkdir build_core_plugins
pushd build_core_plugins
prep -DPLUGIN_UI=COMMON ../avidemux_plugins
build
popd

mkdir build_core_plugins_settings
pushd build_core_plugins_settings
prep -DPLUGIN_UI=SETTINGS ../avidemux_plugins
build
popd

mkdir build_cli
pushd build_cli
prep ../avidemux/cli
build
popd

mkdir build_cli_plugins
pushd build_cli_plugins
prep -DPLUGIN_UI=CLI ../avidemux_plugins
build
popd

mkdir build_qt
pushd build_qt
prep ../avidemux/qt4
build
popd

mkdir build_qt_plugins
pushd build_qt_plugins
prep -DPLUGIN_UI=QT4 ../avidemux_plugins
build
popd

%install
# Remove unused headers & Windows executables
rm -fr install/%{_includedir}
rm -fr install/%{_datadir}/ADM6_addons

cp -pav install/* %{buildroot}/

# Generic man page
install -p -Dm 644 man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{org}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{org}.appdata.xml

%files libs
%license COPYING 
%doc README AUTHORS
%{_bindir}/vsProxy
%dir %{_datadir}/%{name}6
%dir %{_libdir}/ADM_plugins6
%{_libdir}/ADM_plugins6/audioDecoder
%{_libdir}/ADM_plugins6/audioDevices
%{_libdir}/ADM_plugins6/audioEncoders
%{_libdir}/ADM_plugins6/autoScripts
%{_libdir}/ADM_plugins6/demuxers
%{_libdir}/ADM_plugins6/muxers
%{_libdir}/ADM_plugins6/scriptEngines
%{_libdir}/ADM_plugins6/pluginSettings
%{_libdir}/ADM_plugins6/videoDecoders
%dir %{_libdir}/ADM_plugins6/videoEncoders
%{_libdir}/ADM_plugins6/videoEncoders/*.so
%dir %{_libdir}/ADM_plugins6/videoFilters
%{_libdir}/ADM_plugins6/videoFilters/*.so
%{_libdir}/libADM6avcodec.so.61
%{_libdir}/libADM6avformat.so.61
%{_libdir}/libADM6avutil.so.59
%{_libdir}/libADM6postproc.so.58
%{_libdir}/libADM6swscale.so.8
%{_libdir}/libADM_audioParser6.so
%{_libdir}/libADM_core6.so
%{_libdir}/libADM_coreAudio6.so
%{_libdir}/libADM_coreAudioDevice6.so
%{_libdir}/libADM_coreAudioEncoder6.so
%{_libdir}/libADM_coreAudioFilterAPI6.so
%{_libdir}/libADM_coreDemuxer6.so
%{_libdir}/libADM_coreDemuxerMpeg6.so
%{_libdir}/libADM_coreImage6.so
%{_libdir}/libADM_coreImageLoader6.so
%{_libdir}/libADM_coreJobs.so
%{_libdir}/libADM_coreLibVAEnc6.so
%{_libdir}/libADM_coreLibVA6.so
%{_libdir}/libADM_coreMuxer6.so
%{_libdir}/libADM_coreScript.so
%{_libdir}/libADM_coreSocket6.so
%{_libdir}/libADM_coreSqlLight3.so
%{_libdir}/libADM_coreSubtitles6.so
%{_libdir}/libADM_coreUI6.so
%{_libdir}/libADM_coreUtils6.so
%{_libdir}/libADM_coreVDPAU6.so
%{_libdir}/libADM_coreVideoCodec6.so
%{_libdir}/libADM_coreVideoEncoder6.so
%{_libdir}/libADM_coreVideoFilter6.so
%{_mandir}/man1/%{name}.1*

%files gui
%{_bindir}/avidemux3_jobs_qt6
%{_bindir}/avidemux3_qt6
%{_bindir}/vsProxy_gui_qt6
%{_datadir}/applications/%{org}.desktop
%{_datadir}/icons/hicolor/*/apps/%{org}.png
%{_datadir}/%{name}6/qt6
%{_datadir}/metainfo/%{org}.appdata.xml
%{_libdir}/ADM_plugins6/shaderDemo
%{_libdir}/ADM_plugins6/videoEncoders/qt6
%{_libdir}/ADM_plugins6/videoFilters/qt6
%{_libdir}/libADM_UIQT66.so
%{_libdir}/libADM_openGLQT66.so
%{_libdir}/libADM_render6_QT6.so

%files cli
%{_bindir}/avidemux3_cli
%{_datadir}/%{name}6
%{_libdir}/ADM_plugins6/videoFilters/cli
%{_libdir}/libADM_UI_Cli6.so
%{_libdir}/libADM_render6_cli.so

%changelog
* Mon Nov 11 2024 Simone Caronni <negativo17@gmail.com> - 1:2.8.2^20240815git7baa0b8-1
- Update to 2.8.2 snapshot.
- Trim changelog.
- Switch to QT 6.

* Wed Jun 07 2023 Simone Caronni <negativo17@gmail.com> - 1:2.8.1-4
- Rebuild for updated dependencies.

* Tue Mar 14 2023 Simone Caronni <negativo17@gmail.com> - 1:2.8.1-3
- Rebuild for updated dependencies.

* Thu Jan 05 2023 Simone Caronni <negativo17@gmail.com> - 1:2.8.1-2
- Rebuild for updated dependencies.

* Thu Sep 22 2022 Simone Caronni <negativo17@gmail.com> - 1:2.8.1-1
- Update to 2.8.1.

* Fri Apr 22 2022 Simone Caronni <negativo17@gmail.com> - 1:2.8.0-2
- Clean up SPEC file, split for the different branches.

* Wed Apr 13 2022 Simone Caronni <negativo17@gmail.com> - 1:2.8.0-1
- Update to 2.8.0.
