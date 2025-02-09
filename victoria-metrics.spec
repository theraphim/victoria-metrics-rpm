%define debug_package %{nil}
%define __strip /bin/true

%global forgeurl https://github.com/VictoriaMetrics/VictoriaMetrics
Name:     VictoriaMetrics
Version:  1.108.1
%forgemeta
Release:  %autorelease
Summary:  High-performance, cost-effective and scalable time series database
License:  Proprietary
URL:      https://victoriametrics.com/
Source:  %{forgesource}
Source100: victoria-metrics.service
Source101: victoria-logs.service
Source200: victoria-metrics.sysusers
Source201: victoria-logs.sysusers
Source300: victoria-metrics.sysconfig
Source301: victoria-logs.sysconfig
Source400: victoria-metrics-scrape.yml
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}

%description
High-performance, cost-effective and scalable time series database and logs storage.

%package -n VictoriaLogs
Summary: High-performance, cost-effective and scalable logs storage

%description -n VictoriaLogs
High-performance, cost-effective and scalable logs storage.

%prep
%forgesetup

%build
make BUILDINFO_TAG=%{version} victoria-metrics victoria-logs vlogscli vmagent vmalert vmalert-tool vmauth vmbackup vmrestore vmctl

%pre
%sysusers_create_compat %{SOURCE200}

%pre -n VictoriaLogs
%sysusers_create_compat %{SOURCE201}

%post
%systemd_post victoria-metrics.service

%preun
%systemd_preun victoria-metrics.service

%postun
%systemd_postun_with_restart victoria-metrics.service

%post -n VictoriaLogs
%systemd_post victoria-logs.service

%preun -n VictoriaLogs
%systemd_preun victoria-logs.service

%postun -n VictoriaLogs
%systemd_postun_with_restart victoria-logs.service

%install
%{__install} -v -D -t $RPM_BUILD_ROOT%{_unitdir} %{SOURCE100}
%{__install} -v -D -t $RPM_BUILD_ROOT%{_unitdir} %{SOURCE101}

%{__install} -m 0755 -v -D -t %{buildroot}%{_bindir} bin/victoria-metrics bin/victoria-logs bin/vlogscli bin/vmagent bin/vmalert bin/vmalert-tool bin/vmauth bin/vmbackup bin/vmrestore bin/vmctl
%{__install} -p -D -m 0644 %{SOURCE200} %{buildroot}%{_sysusersdir}/victoria-metrics.conf
%{__install} -p -D -m 0644 %{SOURCE201} %{buildroot}%{_sysusersdir}/victoria-logs.conf

%{__install} -d -m 0755 %{buildroot}%{_sharedstatedir}/victoria-metrics
%{__install} -d -m 0755 %{buildroot}%{_sharedstatedir}/victoria-logs

%{__install} -p -D -m 644 %{SOURCE301} %{buildroot}%{_sysconfdir}/sysconfig/victoria-logs
%{__install} -p -D -m 644 %{SOURCE300} %{buildroot}%{_sysconfdir}/sysconfig/victoria-metrics

%{__install} -d %{buildroot}%{_sysconfdir}/victoria-metrics
%{__install} -p -D -m 0644 %{SOURCE400} %{buildroot}%{_sysconfdir}/victoria-metrics/scrape.yml

%files
%config(noreplace) %{_sysconfdir}/victoria-metrics
%config(noreplace) %{_sysconfdir}/victoria-metrics/scrape.yml
%{_sysusersdir}/victoria-metrics.conf
%{_unitdir}/victoria-metrics.service
%{_bindir}/victoria-metrics
%{_bindir}/vmagent
%{_bindir}/vmalert
%{_bindir}/vmalert-tool
%{_bindir}/vmauth
%{_bindir}/vmbackup
%{_bindir}/vmrestore
%{_bindir}/vmctl
%dir %attr(-,victoria-metrics,victoria-metrics) %{_sharedstatedir}/victoria-metrics

%files -n VictoriaLogs
%{_sysusersdir}/victoria-logs.conf
%{_unitdir}/victoria-logs.service
%{_bindir}/victoria-logs
%{_bindir}/vlogscli
%dir %attr(-,victoria-logs,victoria-logs) %{_sharedstatedir}/victoria-logs
%config(noreplace) %{_sysconfdir}/sysconfig/victoria-logs

%license 
%doc 

%changelog
%autochangelog
