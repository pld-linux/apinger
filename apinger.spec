Summary:	Alarm Pinger - network monitor with mail notification
Summary(pl):	Alarm Pinger - monitor sieci z powiadamianiem poczt�
Name:		apinger
Version:	0.6.1
Release:	2
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.bnet.pl/~jajcus/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconf
Patch0:		%{name}-user.patch
URL:		http://www.bnet.pl/~jajcus/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Alarm Pinger is a little tool which monitors various IP devices by
simple ICMP echo requests. There are various other tools, that can do
this, but most of them are shell or perl scripts, spawning many
processes, thus much CPU-expensive, especially when one wants
continuous monitoring and fast response on target failure. Alarm
Pinger is a single process written in C, so it doesn't need much CPU
power even when monitoring many targets with frequent probes. Alarm
Pinger supports both IPv4 and IPv6.

%description -l pl
Alarm Pinger to ma�e narz�dzie monitoruj�ce r�ne urz�dzenia IP
wykorzystuj�c pakiety ICMP echo request/reply (tzw. ping). S� r�ne
inne narz�dzia, kt�re to potrafi�, ale wi�kszo�� z nich to skrypty
shella lub perla uruchamiaj�ce wiele proces�w, przez co mocno
obci��aj�ce maszyn�, szczeg�lnie gdy kto� chce ci�g�ego monitorowania
i szybkiej informacji o awarii. Alarm Pinger to pojedynczy proces
napisany w C, wi�c nie wymaga wielkiej mocy obliczeniowej, nawet gdy
bada wiele urz�dze� cz�stymi pingami. Alarm Pinger obs�uguje zar�wno
IPv4 jak i IPv6.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install DESTDIR=$RPM_BUILD_ROOT
install src/%{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add apinger

if [ -f /var/lock/subsys/apinger ]; then
	/etc/rc.d/init.d/apinger restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/apinger start\" to start apinger" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apinger ]; then
		/etc/rc.d/init.d/apinger stop 1>&2
	fi
	/sbin/chkconfig --del apinger
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS TODO README doc/FAQ.html
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) %config(noreplace) /etc/rc.d/init.d/apinger
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/apinger
%attr(640,root,daemon) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
