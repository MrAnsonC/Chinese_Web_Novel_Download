https://github.com/mozilla/geckodriver/releases

0.35.0 Latest
0.35.0 (2024-08-06, 9f0a0036bea4)
Known problems
Startup hang with Firefox running in a container (e.g. snap, flatpak):

When Firefox is packaged inside a container (like the default Firefox browser
shipped with Ubuntu 22.04), it may see a different filesystem to the host.
This can affect access to the generated profile directory, which may result
in a hang when starting Firefox. Workarounds are listed in the geckodriver
usage documentation.

Added
Support for Permissions that allow controlling permission prompts
within the browser. This enables automated tests to handle scenarios
involving permissions like geolocation, notifications, and more.

The command line flag --enable-crash-reporter has been added, to allow
the crash reporter in Firefox to automatically submit crash reports to
Mozilla's crash reporting system if a tab or the browser itself crashes.

Note that this feature is disabled by default and should only be used when a
crash situation needs to be investigated. See our documentation for
crash reports in how to share these with us.

Implemented by Razvan Cojocaru.

Changed
The validation of the unhandledPromptBehavior capability has been enhanced
to support finer configuration options for the User Prompt Handler which
are particularly used by WebDriver BiDi.
Fixed
The Switch To Frame command now correctly raises an "invalid argument"
error when the id parameter is missing.

Implemented by James Hendry.

Removed
Removed support for session negotiation using the deprecated
desiredCapabilities and requiredCapabilities.

Implemented by James Hendry.

Removed support for the moz:useNonSpecCompliantPointerOrigin capability,
which has not bee supported since Firefox 116.