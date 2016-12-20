Name: tendrl-api
Version: 0.0.1
Release: 1%{?dist}
Summary: Collection of tendrl api extensions
Group: Development/Languages
License: LGPLv2+
URL: https://github.com/Tendrl/tendrl-api
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: ruby
BuildRequires: systemd-units

Requires: ruby >= 2.0.0
Requires: rubygem-i18n >= 0.7.0
Requires: rubygem-json
Requires: rubygem-minitest >= 5.9.1
Requires: rubygem-thread_safe >= 0.3.5
Requires: rubygem-mixlib-log >= 1.7.1
Requires: rubygem-puma >= 3.6.0
Requires: rubygem-rake >= 0.9.6
Requires: rubygem-rack >= 1.6.4
Requires: rubygem-tilt >= 1.4.1
Requires: rubygem-bundler >= 1.13.6
Requires: rubygem-tzinfo >= 1.2.2
Requires: rubygem-etcd
Requires: rubygem-rack-protection >= 1.5.3
Requires: rubygem-activesupport >= 4.2.6
Requires: rubygem-sinatra >= 1.4.5

%description
Collection of tendrl api.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%package httpd
Summary: Tendrl api httpd
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
Requires: httpd

%description httpd
Tendrl API httpd configuration.

%prep
%setup

%install
install -dm 0755 --directory $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/tendrl/errors
install -dm 0755 --directory $RPM_BUILD_ROOT%{_datadir}/doc/tendrl/config
install -dm 0755 --directory $RPM_BUILD_ROOT%{_datadir}/%{name}/public
install -dm 0755 --directory $RPM_BUILD_ROOT%{_datadir}/%{name}/.deploy
install -Dm 0644 *.ru *.rb Gemfile* $RPM_BUILD_ROOT%{_datadir}/%{name}
install -Dm 0644 lib/*.rb $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/
install -Dm 0644 lib/tendrl/*.rb $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/tendrl/
install -Dm 0644 lib/tendrl/errors/*.rb $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/tendrl/errors/
install -Dm 0644 tendrl-api.service $RPM_BUILD_ROOT%{_unitdir}/tendrl-api.service
install -Dm 0644 config/etcd.sample.yml $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/etcd.yml
install -Dm 0644 README.adoc Rakefile $RPM_BUILD_ROOT%{_datadir}/doc/tendrl
install -Dm 0644 config/apache.vhost.sample $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/tendrl.conf
install -Dm 0644 config/*.* $RPM_BUILD_ROOT%{_datadir}/doc/tendrl/config/

%post httpd
setsebool -P httpd_can_network_connect 1

%files
%dir %{_sysconfdir}/tendrl
%{_datadir}/%{name}/
%{_unitdir}/tendrl-api.service
%{_sysconfdir}/tendrl/etcd.yml

%files doc
%dir %{_datadir}/doc/tendrl/config
%doc %{_datadir}/doc/tendrl/README.adoc
%{_datadir}/doc/tendrl/config/
%{_datadir}/doc/tendrl/Rakefile

%files httpd
%{_sysconfdir}/httpd/conf.d/tendrl.conf

%changelog
* Wed Nov 16 2016 Tim <tim.gluster@gmail.com> - 0.0.1-1
- Initial package
