Summary: BioGRID's Interaction Management System
Name: BioGRID-IMS3
Version: %{version}
Release: %{release}
License: GPLv2+
URL: http://wiki.thebiogrid.org/doku.php/interaction_management_system
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php-mysql

%description

%prep
%setup -q

%build

%install
%{__install} -m 755 -d $RPM_BUILD_ROOT%{ims_wwwdir}
%{__install} -m 755 www/home.php $RPM_BUILD_ROOT%{ims_wwwdir}/home.php
%{__install} -m 755 www/query.php $RPM_BUILD_ROOT%{ims_wwwdir}/query.php
%{__install} -m 755 www/ims.js $RPM_BUILD_ROOT%{ims_wwwdir}/ims.js
%{__install} -m 755 www/Interaction.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction.js
%{__install} -m 755 www/Interaction_source.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_source.js
%{__install} -m 755 www/Interaction_type.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_type.js
%{__install} -m 755 www/Publication.js $RPM_BUILD_ROOT%{ims_wwwdir}/Publication.js
%{__install} -m 755 www/ims.css $RPM_BUILD_ROOT%{ims_wwwdir}/ims.css
%{__install} -m 755 www/solarized.css $RPM_BUILD_ROOT%{ims_wwwdir}/solarized.css
%{__install} -m 755 -d $RPM_BUILD_ROOT%{ims_phpdir}
%{__install} -m 755 www/ims/ims.php $RPM_BUILD_ROOT%{ims_phpdir}/ims.php
%{__install} -m 755 www/ims/version.php $RPM_BUILD_ROOT%{ims_phpdir}/version.php
%{__install} -m 755 www/ims/pubmed.php $RPM_BUILD_ROOT%{ims_phpdir}/pubmed.php
%{__install} -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}
%{__install} -m 755 ims.json-template $RPM_BUILD_ROOT%{_sysconfdir}/ims.json

%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc README
%config %{_sysconfdir}/ims.json
%{ims_wwwdir}
%{ims_wwwdir}/home.php
%{ims_wwwdir}/query.php
%{ims_wwwdir}/ims.js
%{ims_wwwdir}/Interaction.js
%{ims_wwwdir}/Interaction_source.js
%{ims_wwwdir}/Interaction_type.js
%{ims_wwwdir}/Publication.js
%{ims_wwwdir}/ims.css
%{ims_wwwdir}/solarized.css
%{ims_phpdir}
%{ims_phpdir}/ims.php
%{ims_phpdir}/version.php
%{ims_phpdir}/pubmed.php

%defattr(-,root,root,-)
%doc


%changelog
* Tue Jun 24 2014 Sven Heinicke <sven@tyersdev.tyerslab.com> - 0.1-1
- Now fetches interaction_type and intering_sources.

* Thu Jun 19 2014 Sven Heinicke <sven@genomics.princeton.edu> - 0.0-1
- Initial build.

