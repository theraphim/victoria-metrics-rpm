%define debug_package %{nil}
%define __strip /bin/true

%global forgeurl https://github.com/VictoriaMetrics/VictoriaMetrics
Name:     VictoriaMetrics
Version:  1.140.0
%forgemeta
Release:  %autorelease
Summary:  High-performance, cost-effective and scalable time series database
License:  Proprietary
URL:      https://victoriametrics.com/
Source:  %{forgesource}
Source100: victoria-metrics.service
Source200: victoria-metrics.sysusers
Source300: victoria-metrics.sysconfig
Source400: victoria-metrics-scrape.yml
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}

%description
High-performance, cost-effective and scalable time series database.

%prep
%forgesetup

%build
make BUILDINFO_TAG=%{version} victoria-metrics vmagent vmalert vmalert-tool vmauth vmbackup vmrestore vmctl

%pre
%sysusers_create_compat %{SOURCE200}

%post
%systemd_post victoria-metrics.service

%preun
%systemd_preun victoria-metrics.service

%postun
%systemd_postun_with_restart victoria-metrics.service

%install
%{__install} -v -D -t $RPM_BUILD_ROOT%{_unitdir} %{SOURCE100}

%{__install} -m 0755 -v -D -t %{buildroot}%{_bindir} bin/victoria-metrics bin/vmagent bin/vmalert bin/vmalert-tool bin/vmauth bin/vmbackup bin/vmrestore bin/vmctl
%{__install} -p -D -m 0644 %{SOURCE200} %{buildroot}%{_sysusersdir}/victoria-metrics.conf

%{__install} -d -m 0755 %{buildroot}%{_sharedstatedir}/victoria-metrics

%{__install} -p -D -m 644 %{SOURCE300} %{buildroot}%{_sysconfdir}/sysconfig/victoria-metrics

%{__install} -d %{buildroot}%{_sysconfdir}/victoria-metrics
%{__install} -p -D -m 0644 %{SOURCE400} %{buildroot}%{_sysconfdir}/victoria-metrics/scrape.yml

%files
%config(noreplace) %{_sysconfdir}/victoria-metrics
%config(noreplace) %{_sysconfdir}/sysconfig/victoria-metrics
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

%license 
%doc 

%changelog
%autochangelog
