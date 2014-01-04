
%undefine _compress
%undefine _extension
%global _duplicate_files_terminate_build 0
%global _files_listed_twice_terminate_build 0
%global _unpackaged_files_terminate_build 0
%global _nonzero_exit_pkgcheck_terminate_build 0
%global _use_internal_dependency_generator 0
%global __find_requires /bin/sed -e 's/.*//'
%global __find_provides /bin/sed -e 's/.*//'

Name:		maven-eclipse-plugin
Version:	2.9
Release:	9.0
Summary:	javapackages-bootstrap packages
License:	GPLv3+
Source0:	maven-eclipse-plugin-2.9-9.0-omv2014.0.noarch.rpm
URL:		https://abf.rosalinux.ru/openmandriva/maven-eclipse-plugin
Summary:	maven-eclipse-plugin bootstrap version
Requires:	javapackages-bootstrap
Requires:	jpackage-utils
Requires:	mvn(biz.aQute:bndlib)
Requires:	mvn(commons-io:commons-io)
Requires:	mvn(org.apache.maven.shared:maven-osgi)
Requires:	mvn(org.apache.maven.wagon:wagon-provider-api)
Requires:	mvn(org.apache.maven:maven-archiver)
Requires:	mvn(org.apache.maven:maven-artifact-manager)
Requires:	mvn(org.apache.maven:maven-artifact:2.0.8)
Requires:	mvn(org.apache.maven:maven-compat)
Requires:	mvn(org.apache.maven:maven-core)
Requires:	mvn(org.apache.maven:maven-model:2.0.8)
Requires:	mvn(org.apache.maven:maven-plugin-api)
Requires:	mvn(org.apache.maven:maven-project)
Requires:	mvn(org.apache.maven:maven-settings:2.0.8)
Requires:	mvn(org.codehaus.plexus:plexus-archiver)
Requires:	mvn(org.codehaus.plexus:plexus-interactivity-jline)
Requires:	mvn(org.codehaus.plexus:plexus-resources)
Requires:	mvn(org.codehaus.plexus:plexus-utils)
Provides:	maven-eclipse-plugin = 2.9-9.0:2014.0
Provides:	maven2-plugin-eclipse = 0:2.9-9.0
Provides:	mvn(org.apache.maven.plugins:maven-eclipse-plugin) = 2.9
Obsoletes:	maven2-plugin-eclipse <= 0:2.0.8

%description
maven-eclipse-plugin bootstrap version.

%files		-n maven-eclipse-plugin
/usr/share/doc/maven-eclipse-plugin
/usr/share/doc/maven-eclipse-plugin/DEPENDENCIES
/usr/share/doc/maven-eclipse-plugin/LICENSE
/usr/share/doc/maven-eclipse-plugin/NOTICE
/usr/share/doc/maven-eclipse-plugin/README-testing.txt
/usr/share/java/maven-eclipse-plugin/maven-eclipse-plugin.jar
/usr/share/maven-effective-poms/JPP.maven-eclipse-plugin-maven-eclipse-plugin.pom
/usr/share/maven-fragments/maven-eclipse-plugin.xml
/usr/share/maven-poms/JPP.maven-eclipse-plugin-maven-eclipse-plugin.pom

#------------------------------------------------------------------------
%prep

%build

%install
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -id
