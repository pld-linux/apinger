Summary:	Alarm Pinger - network monitor with mail notification
Summary(pl.UTF-8):	Alarm Pinger - monitor sieci z powiadamianiem pocztą
Name:		apinger
Version:	0.6.1
Release:	7
License:	GPL
Group:		Networking/Utilities
Source0:	https://github.com/downloads/Jajcus/apinger/%{name}-%{version}.tar.gz
# Source0-md5:	3505e6503ec06363613f16713501bb33
Source1:	%{name}.init
Source2:	%{name}.sysconf
Patch0:		%{name}-user.patch
Patch1:		%{name}-avg_delay.patch
Patch2:		%{name}-config_overwrite_fix.patch
Patch3:		%{name}-rrd_timestamp.patch
Patch4:		%{name}-ac.patch
Patch5:		%{name}-no_exit.patch
Patch6:		%{name}-no_forked_receiver.patch
Patch7:		%{name}-srcip.patch
Patch8:		%{name}-status.patch
URL:		https://github.com/Jajcus/apinger/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Alarm Pinger is a little tool which monitors various IP devices by
simple ICMP echo requests. There are various other tools, that can do
this, but most of them are shell or Perl scripts, spawning many
processes, thus much CPU-expensive, especially when one wants
continuous monitoring and fast response on target failure. Alarm
Pinger is a single process written in C, so it doesn't need much CPU
power even when monitoring many targets with frequent probes. Alarm
Pinger supports both IPv4 and IPv6.

%description -l pl.UTF-8
Alarm Pinger to małe narzędzie monitorujące różne urządzenia IP
wykorzystując pakiety ICMP echo request/reply (tzw. ping). Są różne
inne narzędzia, które to potrafią, ale większość z nich to skrypty
shella lub Perla uruchamiające wiele procesów, przez co mocno
obciążające maszynę, szczególnie gdy ktoś chce ciągłego monitorowania
i szybkiej informacji o awarii. Alarm Pinger to pojedynczy proces
napisany w C, więc nie wymaga wielkiej mocy obliczeniowej, nawet gdy
bada wiele urządzeń częstymi pingami. Alarm Pinger obsługuje zarówno
IPv4 jak i IPv6.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install src/%{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add apinger
%service apinger restart

%preun
if [ "$1" = "0" ]; then
	%service apinger stop
	/sbin/chkconfig --del apinger
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS TODO README doc/FAQ.html
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) %config(noreplace) /etc/rc.d/init.d/apinger
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/apinger
%attr(640,root,daemon) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
