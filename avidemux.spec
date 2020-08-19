%global org org.avidemux.Avidemux

Name:           avidemux
Version:        2.7.6
Release:        1%{?dist}
Epoch:          1
Summary:        Free video editor designed for simple cutting, filtering and encoding tasks
License:        GPLv2
URL:            http://fixounet.free.fr/%{name}/

Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{version}.tar.gz
Patch0:         https://github.com/mean00/%{name}2/commit/a1d969d47a5d2e49a7c3a0a0b6c7e6ed9fd46622.patch

BuildRequires:  a52dec-devel
BuildRequires:  alsa-lib-devel
%if 0%{?fedora}
BuildRequires:  cmake
%else
BuildRequires:  cmake3
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  lame-devel
BuildRequires:  libaom-devel
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  libappstream-glib
%endif
BuildRequires:  libass-devel
BuildRequires:  libfdk-aac-devel
BuildRequires:  libmad-devel
BuildRequires:  libmp4v2-devel
BuildRequires:  libogg-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
%if 0%{?rhel} == 7
BuildRequires:  libvpx1.7-devel
%else
BuildRequires:  libvpx-devel >= 1.7.0
%endif
BuildRequires:  libxml2-devel
BuildRequires:  libXmu-devel
BuildRequires:  libxslt
BuildRequires:  libxslt
BuildRequires:  libXv-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  nv-codec-headers
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
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  vapoursynth-devel
%endif
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  xvidcore-devel
BuildRequires:  yasm-devel

%description
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible MPEG
files, MP4 and ASF, using a variety of codecs. Tasks can be automated using
projects, job queue and powerful scripting capabilities.

%package libs
Summary:    Base libraries for Avidemux
Provides:   bundled(ffmpeg) = 4.2.3

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
%autosetup -p1 -n %{name}_%{version}

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
%if 0%{?fedora}
%cmake \
%else
%cmake3 \
%endif
    -DAVIDEMUX_SOURCE_DIR=%{_builddir}/%{name}_%{version} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_EDIT_COMMAND=vim \
    -DENABLE_QT5=True \
    -DFAKEROOT=%{_builddir}/%{name}_%{version}/install \
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
    DESTDIR=%{_builddir}/%{name}_%{version}/install \
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
%if 0%{?fedora} || 0%{?rhel} >= 8
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{org}.appdata.xml
%endif

%ldconfig_scriptlets libs

%ldconfig_scriptlets cli

%if 0%{?rhel} == 7

%post gui
%{?ldconfig}
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%{_bindir}/update-desktop-database &> /dev/null || :

%postun gui
%{?ldconfig}
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%{_bindir}/update-desktop-database &> /dev/null || :

%endif

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
%{_libdir}/libADM6avcodec.so.58
%{_libdir}/libADM6avformat.so.58
%{_libdir}/libADM6avutil.so.56
%{_libdir}/libADM6postproc.so.55
%{_libdir}/libADM6swscale.so.5
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
%{_bindir}/avidemux3_jobs_qt5
%{_bindir}/avidemux3_qt5
%{_bindir}/vsProxy_gui_qt5
%{_datadir}/applications/%{org}.desktop
%{_datadir}/icons/hicolor/*/apps/%{org}.png
%{_datadir}/%{name}6/qt5
%if 0%{?fedora} || 0%{?rhel} >= 8
%{_datadir}/metainfo/%{org}.appdata.xml
%else
%exclude %{_datadir}/metainfo
%endif
%{_libdir}/ADM_plugins6/shaderDemo
%{_libdir}/ADM_plugins6/videoEncoders/qt5
%{_libdir}/ADM_plugins6/videoFilters/qt5
%{_libdir}/libADM_UIQT56.so
%{_libdir}/libADM_openGLQT56.so
%{_libdir}/libADM_render6_QT5.so

%files cli
%{_bindir}/avidemux3_cli
%{_datadir}/%{name}6
%{_libdir}/ADM_plugins6/videoFilters/cli
%{_libdir}/libADM_UI_Cli6.so
%{_libdir}/libADM_render6_cli.so

%changelog
* Tue Aug 18 2020 Simone Caronni <negativo17@gmail.com> - 1:2.7.6-1
- Update to 2.7.6.
- Clean up SPEC file.

* Mon Oct 21 2019 Simone Caronni <negativo17@gmail.com> - 1:2.7.3-4
- Rebuild for updated dependencies.

* Sun Jul 07 2019 Simone Caronni <negativo17@gmail.com> - 1:2.7.3-3
- Rebuild for updated dependencies.

* Mon May 27 2019 Simone Caronni <negativo17@gmail.com> - 1:2.7.3-2
- Rebuild for updated dependencies.

* Sun May 12 2019 Simone Caronni <negativo17@gmail.com> - 1:2.7.3-1
- Update to 2.7.3.

* Thu Feb 28 2019 Simone Caronni <negativo17@gmail.com> - 1:2.7.1-4
- Rebuild for updated dependencies.

* Thu Nov 15 2018 Simone Caronni <negativo17@gmail.com> - 1:2.7.1-3
- Rebuild for updated x265.

* Fri Sep 21 2018 Simone Caronni <negativo17@gmail.com> - 1:2.7.1-2
- Rebuild for updated dependencies.

* Mon Jul 16 2018 Simone Caronni <negativo17@gmail.com> - 1:2.7.1-1
- Update to 2.7.1.

* Fri Apr 27 2018 Simone Caronni <negativo17@gmail.com> - 1:2.7.0-5
- Fix build on Fedora 28.

* Fri Apr 27 2018 Simone Caronni <negativo17@gmail.com> - 1:2.7.0-4
- Rebuild for updated dependencies.
- Update SPEC file.

* Tue Apr 10 2018 Simone Caronni <negativo17@gmail.com> - 1:2.7.0-3
- Rebuild for updated dependencies.

* Thu Jan 11 2018 Simone Caronni <negativo17@gmail.com> - 1:2.7.0-2
- Rebuild for updated libraries.

* Fri Oct 27 2017 Simone Caronni <negativo17@gmail.com> - 1:2.7.0-1
- Update to 2.7.0.
- Require cmake 3 on RHEL 7.

* Mon May 15 2017 Simone Caronni <negativo17@gmail.com> - 2.6.20-1
- Update to 2.6.20.
- Bump Epoch.

* Sun Feb 26 2017 Simone Caronni <negativo17@gmail.com> - 2.6.18-3
- Rebuild for x265 update.

* Fri Feb 10 2017 Simone Caronni <negativo17@gmail.com> - 2.6.18-2
- Add missing QT5 components to GUI subpackage, thanks George Seaton!

* Fri Jan 27 2017 Simone Caronni <negativo17@gmail.com> - 2.6.18-1
- Update to 2.6.18.

* Tue Jan 03 2017 Simone Caronni <negativo17@gmail.com> - 2.6.16-1
- Update to 2.6.16.
- Update system libraries patch.

* Wed Dec 14 2016 Simone Caronni <negativo17@gmail.com> - 2.6.15-3
- GUI package should also obsolete generic package.

* Mon Nov 21 2016 Simone Caronni <negativo17@gmail.com> - 2.6.15-2
- Split components in gui/cli/libs subpackages.
- Use system libmp4v2.

* Sun Nov 20 2016 Simone Caronni <negativo17@gmail.com> - 2.6.15-1
- First build.
