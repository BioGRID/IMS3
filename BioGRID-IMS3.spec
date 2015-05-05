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
%{__install} -m 755 www/user.php $RPM_BUILD_ROOT%{ims_wwwdir}/user.php
%{__install} -m 755 www/commit.php $RPM_BUILD_ROOT%{ims_wwwdir}/commit.php
%{__install} -m 755 www/ims.js $RPM_BUILD_ROOT%{ims_wwwdir}/ims.js
%{__install} -m 755 www/Interaction.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction.js
%{__install} -m 755 www/Interaction_history.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_history.js
%{__install} -m 755 www/Interaction_participant.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_participant.js
%{__install} -m 755 www/Interaction_ontology.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_ontology.js
%{__install} -m 755 www/Interaction_ontology_qualifier.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_ontology_qualifier.js
%{__install} -m 755 www/Interaction_ontology_type.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_ontology_type.js
%{__install} -m 755 www/Interaction_source.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_source.js
%{__install} -m 755 www/Interaction_note.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_note.js
%{__install} -m 755 www/Interaction_type.js $RPM_BUILD_ROOT%{ims_wwwdir}/Interaction_type.js
%{__install} -m 755 www/Ontology.js $RPM_BUILD_ROOT%{ims_wwwdir}/Ontology.js
%{__install} -m 755 www/Ontology_term.js $RPM_BUILD_ROOT%{ims_wwwdir}/Ontology_term.js
%{__install} -m 755 www/Participant.js $RPM_BUILD_ROOT%{ims_wwwdir}/Participant.js
%{__install} -m 755 www/Participant_role.js $RPM_BUILD_ROOT%{ims_wwwdir}/Participant_role.js
%{__install} -m 755 www/Participant_type.js $RPM_BUILD_ROOT%{ims_wwwdir}/Participant_type.js
%{__install} -m 755 www/Project.js $RPM_BUILD_ROOT%{ims_wwwdir}/Project.js
%{__install} -m 755 www/Publication.js $RPM_BUILD_ROOT%{ims_wwwdir}/Publication.js
%{__install} -m 755 www/Quick_identifier.js $RPM_BUILD_ROOT%{ims_wwwdir}/Quick_identifier.js
%{__install} -m 755 www/Quick_identifier_type.js $RPM_BUILD_ROOT%{ims_wwwdir}/Quick_identifier_type.js
%{__install} -m 755 www/Quick_organism.js $RPM_BUILD_ROOT%{ims_wwwdir}/Quick_organism.js
%{__install} -m 755 www/Unknown_participant.js $RPM_BUILD_ROOT%{ims_wwwdir}/Unknown_participant.js
%{__install} -m 755 www/User.js $RPM_BUILD_ROOT%{ims_wwwdir}/User.js
%{__install} -m 755 www/ims.css $RPM_BUILD_ROOT%{ims_wwwdir}/ims.css
%{__install} -m 755 -d $RPM_BUILD_ROOT%{ims_phpdir}
%{__install} -m 755 www/ims/ims.php $RPM_BUILD_ROOT%{ims_phpdir}/ims.php
%{__install} -m 755 www/ims/Ontologies.php $RPM_BUILD_ROOT%{ims_phpdir}/Ontologies.php
%{__install} -m 755 www/ims/version.php $RPM_BUILD_ROOT%{ims_phpdir}/version.php
%{__install} -m 755 www/ims/pubmed.php $RPM_BUILD_ROOT%{ims_phpdir}/pubmed.php
%{__install} -m 755 -d $RPM_BUILD_ROOT%{ims_phpdir}/html
%{__install} -m 755 www/ims/html/interaction.htm $RPM_BUILD_ROOT%{ims_phpdir}/html/interaction.htm
%{__install} -m 755 www/ims/html/project.htm $RPM_BUILD_ROOT%{ims_phpdir}/html/project.htm
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
%{ims_wwwdir}/user.php
%{ims_wwwdir}/commit.php
%{ims_wwwdir}/ims.js
%{ims_wwwdir}/Interaction.js
%{ims_wwwdir}/Interaction_history.js
%{ims_wwwdir}/Interaction_participant.js
%{ims_wwwdir}/Interaction_ontology.js
%{ims_wwwdir}/Interaction_ontology_qualifier.js
%{ims_wwwdir}/Interaction_ontology_type.js
%{ims_wwwdir}/Interaction_source.js
%{ims_wwwdir}/Interaction_note.js
%{ims_wwwdir}/Interaction_type.js
%{ims_wwwdir}/Ontology.js
%{ims_wwwdir}/Ontology_term.js
%{ims_wwwdir}/Participant.js
%{ims_wwwdir}/Participant_role.js
%{ims_wwwdir}/Participant_type.js
%{ims_wwwdir}/Project.js
%{ims_wwwdir}/Publication.js
%{ims_wwwdir}/Quick_identifier.js
%{ims_wwwdir}/Quick_identifier_type.js
%{ims_wwwdir}/Quick_organism.js
%{ims_wwwdir}/Unknown_participant.js
%{ims_wwwdir}/User.js
%{ims_wwwdir}/ims.css
%{ims_phpdir}
%{ims_phpdir}/ims.php
%{ims_phpdir}/Ontologies.php
%{ims_phpdir}/version.php
%{ims_phpdir}/pubmed.php
%{ims_phpdir}/html
%{ims_phpdir}/html/interaction.htm
%{ims_phpdir}/html/project.htm

%defattr(-,root,root,-)
%doc


%changelog
* Mon May 05 2015 Sven Heinicke <heinicke@princeton.edu> - 0.23
- Can now enter Ontologies

* Mon Apr 13 2015 Sven Heinicke <sven@genomics.princeton.edu> - 0.22
- Has modification_type radio boxes.

* Mon Mar 30 2015 Sven Heinicke <sven@genomics.princeton.edu> - 0.21
- Now displays bait and hit items in Interaction table.

* Thu Mar 19 2015 Sven Heinicke <sven@genomics.princeton.edu> - 0.20
- Now displays interaction_ontologies_qualifiers.

* Wed Mar 04 2015 Sven Heinicke <sven@genomics.princeton.edu> - 0.19
- Now saves and displays interaction_notes.

* Thu Feb 27 2015 Sven Heinicke <sven@genomics.princeton.edu> - 0.18
- A little less ugly.
- Recordes user with both experimental systems and throught.

* Mon Feb 23 2015 Sven Heinicke <sven@genomics.princeton.edu> - 0.17
- Though ugly, both experimental systems and throughtput can be input.

* Fri Feb 13 2015 Sven Heinicke <sven@genomics.princeton.edu> - 0.16
- Input of experimental systems should now work.
- Some logic is now used if multiple quick identifiers are found to
  picke one.

* Fri Feb 06 2015 Sven Heinicke <sven@genomics.princeton.edu> - 0.15
- Fixed up displaying interaciton_ontology_types.

* Wed Jan 28 2015 Sven Heinicke <sven@genomics.princeton.edu> - 0.14
- Added first ontology viewer.

* Thu Dec 18 2014 Sven Heinicke <sven@genomics.princeton.edu> - 0.13
- Now install in /usr/share/ims/html, you provide apache access.

* Mon Nov 17 2014 Sven Heinicke <sven@genomics.princeton.edu> - 0.12
- Added project page.

* Thu Nov 12 2014 Sven Heinicke <sven@genomics.princeton.edu> - 0.11
- Commits created interactions to the database
