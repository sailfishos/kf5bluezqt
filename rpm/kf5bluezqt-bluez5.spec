Name:       kf5bluezqt-bluez5
Summary:    KF5BluezQt - Qt wrapper for BlueZ 5 DBus API
Version:    5.112.0
Release:    1
License:    LGPLv2
URL:        https://github.com/sailfishos/kf5bluezqt
Source0:    %{name}-%{version}.tar.bz2
Provides:   kf5bluezqt

BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules >= 5.112.0
BuildRequires:  doxygen
BuildRequires:  qt5-qttools
BuildRequires:  qt5-qttools-qthelp-devel

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: bluez5
Requires: bluez5-obexd

Patch1:  0001-Expose-adapter.connected-property.-Contributes-to-JB.patch
Patch2:  0002-Add-filtering-options-to-DeclarativeDevicesModel.-Co.patch
Patch3:  0003-Add-support-for-KeyboardDisplay-type-agents.patch
Patch4:  0004-Add-Manager-pairWithDevice-QString-to-pair-with-unkn.patch
Patch5:  0005-Check-for-object-validity-in-macros.patch
Patch6:  0006-Fix-crash-after-unloading-the-obex-manager.-Fixes-JB.patch
Patch7:  0007-Add-some-missing-includes.patch
Patch8:  0008-Build-with-Qt-5.6.patch
Patch9:  0009-Revert-We-now-require-Qt-5.15.patch
Patch10: 0010-Avoid-QSharedPointer-assignments-comparisons-to-null.patch
Patch11: 0011-Revert-qt_add_dbus_interface-back-to-qt5_add_dbus_in.patch
Patch12: 0012-Revert-minimum-cmake-bump.patch
Patch13: 0013-Add-back-QtQml-include.patch
Patch14: 0014-Force-light-mode-in-Doxygen.patch
Patch15: 0015-Fix-qmlplugindump-crash.patch
Patch16: 0016-Add-plugins.qmltypes.patch
Patch17: 0017-Initialize-existing-batteries-in-QML-devices.patch

%description
This package contains the KF5BluezQt library.

%package declarative
Summary:    Declarative plugin for kf5bluezqt
Provides:   kf5bluezqt-declarative
Requires:   %{name} = %{version}-%{release}
Requires:   %{name} = %{version}

%description declarative
This package contains declarative plugin for kf5bluezqt

%package devel
Summary:    Development files for kf5bluezqt
Provides:   kf5bluezqt-devel
Requires:   %{name} = %{version}-%{release}
Requires:   %{name} = %{version}

%description devel
This package contains the development header files for kf5bluezqt

%package doc
Summary:    API documentation for %{name}
BuildArch:  noarch

%description doc
%{summary}.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%cmake -DBUILD_TESTING=FALSE -DBUILD_QCH=TRUE -DDOXYGEN_SKIP_DOT=TRUE .
%make_build

%install
%make_install

doxygen ../doc/Doxyfile
mkdir -p %{buildroot}/%{_docdir}/%{name}
mkdir -p %{buildroot}/%{_docdir}/%{name}/search
cp -r doc/html/* %{buildroot}/%{_docdir}/%{name}/
mv %{buildroot}/%{_docdir}/qt5/* %{buildroot}/%{_docdir}/%{name}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license LICENSES/LGPL-2.1-only.txt
%{_libdir}/libKF5BluezQt.so.*
%{_datadir}/qlogging-categories5/bluezqt.categories
%{_datadir}/qlogging-categories5/bluezqt.renamecategories
%exclude /lib/udev/rules.d/61-kde-bluetooth-rfkill.rules

%files declarative
%defattr(-,root,root,-)
%{_libdir}/qt5/qml/org/kde/bluezqt

%files devel
%defattr(-,root,root,-)
%{_libdir}/libKF5BluezQt.so
%{_libdir}/pkgconfig/KF5BluezQt.pc
%{_includedir}/KF5/BluezQt
%{_libdir}/cmake/KF5BluezQt
%exclude %{_datadir}/qt5/mkspecs/modules/qt_BluezQt.pri

%files doc
%defattr(-,root,root,-)
%{_docdir}/kf5bluezqt-bluez5/*
