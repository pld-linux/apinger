Summary:	Alarm Pinger - network monitor with mail notification
Summary(pl):	Alarm Pinger - monitor sieci z powiadamianiem poczt±
Name:		apinger
Version:	0.6.1
Release:	5
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.bnet.pl/~jajcus/apinger/%{name}-%{version}.tar.gz
# Source0-md5:	3505e6503ec06363613f16713501bb33
Source1:	%{name}.init
Source2:	%{name}.sysconf
Patch0:		%{name}-user.patch
Patch1:		%{name}-avg_delay.patch
Patch2:		%{name}-config_overwrite_fix.patch
Patch3:		%{name}-rrd_timestamp.patch
URL:		http://www.bnet.pl/~jajcus/
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

%description -l pl
Alarm Pinger to ma³e narzêdzie monitoruj±ce ró¿ne urz±dzenia IP
wykorzystuj±c pakiety ICMP echo request/reply (tzw. ping). S± ró¿ne
inne narzêdzia, które to potrafi±, ale wiêkszo¶æ z nich to skrypty
shella lub Perla uruchamiaj±ce wiele procesów, przez co mocno
obci±¿aj±ce maszynê, szczególnie gdy kto¶ chce ci±g³ego monitorowania
i szybkiej informacji o awarii. Alarm Pinger to pojedynczy proces
napisany w C, wiêc nie wymaga wielkiej mocy obliczeniowej, nawet gdy
bada wiele urz±dzeñ czêstymi pingami. Alarm Pinger obs³uguje zarówno
IPv4 jak i IPv6.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure
%{__make}

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
