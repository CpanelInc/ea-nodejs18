Name:    ea-nodejs18
Vendor:  cPanel, Inc.
Summary: Node.js 18
Version: 18.20.3
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: MIT
Group:   Development/Languages
URL:  https://nodejs.org
Source0: https://nodejs.org/dist/v%{version}/node-v%{version}-linux-x64.tar.gz

Provides: ea4-nodejs
Conflicts: ea4-nodejs
# Because old ea-nodejs10 does not have ^^^ and DNF wants to solve ^^^ by downgrading ea-nodejs10
Conflicts: ea-nodejs10

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.

%prep
%setup -qn node-v%{version}-linux-x64

%build

# nodejs now has support for Microsoft Powershell, since that is not relevant
# to any of our deployed systems, I am removing them so they do not
# automatically require powershell, causing a dependency issue

cat > remove_pwsh.pl <<EOF
use strict;
use warnings;

my @files = split (/\n/, \`find . -type f -print\`);

foreach my \$file (@files) {
    my \$first_line = \`head -n 1 \$file\`;
    if (\$first_line =~ m/env\s+pwsh/) {
        print "Removing file \$file\n";
        unlink \$file;
    }
}
EOF

/usr/bin/perl remove_pwsh.pl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs18
cp -r ./* $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs18

cd $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs18
for file in `find . -type f -print | xargs grep -l '^#![ \t]*/usr/bin/env node'`
do
    echo "Changing Shebang (env) for" $file
    sed -i '1s:^#![ \t]*/usr/bin/env node:#!/opt/cpanel/ea-nodejs18/bin/node:' $file
done

mkdir -p %{buildroot}/etc/cpanel/ea4
echo -n /opt/cpanel/ea-nodejs18/bin/node > %{buildroot}/etc/cpanel/ea4/passenger.nodejs

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
/opt/cpanel/ea-nodejs18
/etc/cpanel/ea4/passenger.nodejs
%attr(0755,root,root) /opt/cpanel/ea-nodejs18/bin/*


%changelog
* Tue May 21 2024 Cory McIntire <cory@cpanel.net> - 18.20.3-1
- EA-12166: Update ea-nodejs18 from v18.20.2 to v18.20.3

* Wed Apr 10 2024 Cory McIntire <cory@cpanel.net> - 18.20.2-1
- EA-12082: Update ea-nodejs18 from v18.20.1 to v18.20.2
- Command injection via args parameter of child_process.spawn without shell option enabled on Windows (CVE-2024-27980) - (HIGH)

* Wed Apr 03 2024 Cory McIntire <cory@cpanel.net> - 18.20.1-1
- EA-12067: Update ea-nodejs18 from v18.20.0 to v18.20.1
- CVE-2024-27983 - Assertion failed in node::http2::Http2Session::~Http2Session() leads to HTTP/2 server crash- (High)
- CVE-2024-27982 - HTTP Request Smuggling via Content Length Obfuscation - (Medium)

* Tue Mar 26 2024 Cory McIntire <cory@cpanel.net> - 18.20.0-1
- EA-12049: Update ea-nodejs18 from v18.19.1 to v18.20.0

* Wed Feb 14 2024 Cory McIntire <cory@cpanel.net> - 18.19.1-1
- EA-11974: Update ea-nodejs18 from v18.19.0 to v18.19.1
- CVE-2024-21892 - Code injection and privilege escalation through Linux capabilities- (High)
- CVE-2024-22019 - http: Reading unprocessed HTTP request with unbounded chunk extension allows DoS attacks- (High)
- CVE-2023-46809 - Node.js is vulnerable to the Marvin Attack (timing variant of the Bleichenbacher attack against PKCS#1 v1.5 padding) - (Medium)
- CVE-2024-22025 - Denial of Service by resource exhaustion in fetch() brotli decoding - (Medium)

* Thu Nov 30 2023 Cory McIntire <cory@cpanel.net> - 18.19.0-1
- EA-11839: Update ea-nodejs18 from v18.18.2 to v18.19.0

* Mon Oct 16 2023 Cory McIntire <cory@cpanel.net> - 18.18.2-1
- EA-11746: Update ea-nodejs18 from v18.18.0 to v18.18.2
	undici - Cookie headers are not cleared in cross-domain redirect in undici-fetch (High) - (CVE-2023-45143)
	nghttp2 - HTTP/2 Rapid Reset (High) - (CVE-2023-44487)
	Permission model improperly protects against path traversal (High) - (CVE-2023-39331)
	Path traversal through path stored in Uint8Array (High) - (CVE-2023-39332)
	Integrity checks according to policies can be circumvented (Medium) - (CVE-2023-38552)
	Code injection via WebAssembly export names (Low) - (CVE-2023-39333)


* Wed Sep 20 2023 Travis Holloway <t.holloway@cpanel.net> - 18.18.0-1
- EA-11697: Update ea-nodejs18 from v18.17.1 to v18.18.0

* Mon Aug 14 2023 Julian Brown <julian.brown@cpanel.net> - 18.17.1-1
- ZC-11124: Initial build

