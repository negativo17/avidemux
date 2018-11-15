# Todo: use system ffmpeg (patches)
# libdca/dcadec?

Name:           avidemux
Version:        2.7.1
Release:        3%{?dist}
Epoch:          1
Summary:        Free video editor designed for simple cutting, filtering and encoding tasks
License:        GPLv2
URL:            http://fixounet.free.fr/avidemux/

Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{version}.tar.gz

BuildRequires:  a52dec-devel
BuildRequires:  alsa-lib-devel
%if 0%{?fedora}
BuildRequires:  cmake
%else
BuildRequires:  cmake3
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  faac-devel
BuildRequires:  faad2-devel
#BuildRequires:  ffmpeg-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  js-devel
BuildRequires:  lame-devel
BuildRequires:  libass-devel
BuildRequires:  libfdk-aac-devel
BuildRequires:  libmad-devel
BuildRequires:  libmp4v2-devel
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

%description
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible MPEG
files, MP4 and ASF, using a variety of codecs. Tasks can be automated using
projects, job queue and powerful scripting capabilities.

%package libs
Summary:    Base libaries for Avidemux
Provides:   bundled(ffmpeg) = 3.0.3

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
Obsoletes:  %{name}-gtk%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:   %{name}-gtk%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:  %{name}-i18n%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:   %{name}-i18n%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:  %{name}-qt%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:   %{name}-qt%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:  %{name}%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:   %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description gui
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible MPEG
files, MP4 and ASF, using a variety of codecs. Tasks can be automated using
projects, job queue and powerful scripting capabilities.

This package contains the graphical interface.

%package devel
Summary:    Development files for Avidemux
Requires:   %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   %{name}-cli%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   %{name}-gui%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%autosetup -n %{name}_%{version}

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
%if 0%{?fedora}
%cmake \
%else
%cmake3 \
%endif
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DFAKEROOT=%{_builddir}/%{name}_%{version}/install \
    -DENABLE_QT5=True \
    -DCMAKE_EDIT_COMMAND=vim \
    -DNVENC_INCLUDE_DIR=%{_includedir}/nvenc \
    -DUSE_EXTERNAL_LIBASS=ON \
    -DUSE_EXTERNAL_LIBMAD=ON \
    -DUSE_EXTERNAL_LIBA52=ON \
    -DUSE_EXTERNAL_MP4V2=ON \
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
build
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

# Windows executables
rm -fr %{buildroot}/%{_datadir}/ADM6_addons

install -p -Dm 644 man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -p -Dm 644 %{name}_icon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -p -Dm 644 %{name}2.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# rpmlint fixes
chmod 755 %{buildroot}%{_libdir}/*.so*

%ldconfig_scriptlets libs

%ldconfig_scriptlets cli

%post gui
%{?ldconfig}
%if 0%{?rhel} == 7
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%{_bindir}/update-desktop-database &> /dev/null || :
%endif

%postun gui
%{?ldconfig}
%if 0%{?rhel} == 7
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%{_bindir}/update-desktop-database &> /dev/null || :
%endif

%files libs
%license COPYING 
%doc README AUTHORS
%{_libdir}/ADM_plugins6
%exclude %{_libdir}/ADM_plugins6/videoEncoders/qt5
%exclude %{_libdir}/ADM_plugins6/videoFilters/qt5
# Rebranded & patched ffmpeg:
%{_libdir}/libADM6avcodec.so.57
%{_libdir}/libADM6avformat.so.57
%{_libdir}/libADM6avutil.so.55
%{_libdir}/libADM6postproc.so.54
%{_libdir}/libADM6swscale.so.4
# end
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
%{_libdir}/libADM_coreSubtitle.so
%{_libdir}/libADM_coreUI6.so
%{_libdir}/libADM_coreUtils6.so
%{_libdir}/libADM_coreVDPAU6.so
%{_libdir}/libADM_coreVideoCodec6.so
%{_libdir}/libADM_coreVideoEncoder6.so
%{_libdir}/libADM_coreVideoFilter6.so

%files gui
%{_bindir}/avidemux3_jobs_qt5
%{_bindir}/avidemux3_qt5
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
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
%{_mandir}/man1/*

%files devel
%{_includedir}/%{name}

%changelog
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
