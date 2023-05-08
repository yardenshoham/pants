# Copyright 2023 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import annotations

from pants.backend.nfpm.fields.all import (
    NfpmArchField,
    NfpmDependencies,
    NfpmHomepageField,
    NfpmLicenseField,
    NfpmPackageNameField,
    NfpmPlatformField,
)
from pants.backend.nfpm.fields.apk import (
    NfpmApkDependsField,
    NfpmApkMaintainerField,
    NfpmApkProvidesField,
    NfpmApkReplacesField,
)
from pants.backend.nfpm.fields.archlinux import (
    NfpmArchlinuxConflictsField,
    NfpmArchlinuxDependsField,
    NfpmArchlinuxPackagerField,
    NfpmArchlinuxPkgbaseField,
    NfpmArchlinuxProvidesField,
    NfpmArchlinuxReplacesField,
)
from pants.backend.nfpm.fields.deb import (
    NfpmDebBreaksField,
    NfpmDebCompressionField,
    NfpmDebConflictsField,
    NfpmDebDependsField,
    NfpmDebMaintainerField,
    NfpmDebPriorityField,
    NfpmDebProvidesField,
    NfpmDebRecommendsField,
    NfpmDebReplacesField,
    NfpmDebSectionField,
    NfpmDebSuggestsField,
)
from pants.backend.nfpm.fields.rpm import (
    NfpmRpmCompressionField,
    NfpmRpmConflictsField,
    NfpmRpmDependsField,
    NfpmRpmGroupField,
    NfpmRpmPackagerField,
    NfpmRpmProvidesField,
    NfpmRpmRecommendsField,
    NfpmRpmReplacesField,
    NfpmRpmSuggestsField,
    NfpmRpmSummaryField,
    NfpmRpmVendorField,
)
from pants.backend.nfpm.fields.version import (
    NfpmVersionEpochField,
    NfpmVersionField,
    NfpmVersionMetadataField,
    NfpmVersionPrereleaseField,
    NfpmVersionReleaseField,
    NfpmVersionSchemaField,
)
from pants.core.goals.package import OutputPathField
from pants.engine.target import COMMON_TARGET_FIELDS, Target
from pants.util.docutil import doc_url
from pants.util.strutil import help_text

APK_FIELDS = (
    NfpmPackageNameField,
    NfpmArchField,
    # version fields (apk does NOT get: version_metadata or epoch)
    NfpmVersionField,
    NfpmVersionSchemaField,
    NfpmVersionPrereleaseField,
    NfpmVersionReleaseField,
    # other package metadata fields
    NfpmHomepageField,
    NfpmLicenseField,
    NfpmApkMaintainerField,
    # package relationships
    NfpmApkReplacesField,
    NfpmApkProvidesField,
    NfpmApkDependsField,
)


class NfpmApkPackage(Target):
    alias = "nfpm_apk_package"
    core_fields = (
        *COMMON_TARGET_FIELDS,  # tags, description
        OutputPathField,
        NfpmDependencies,
        *APK_FIELDS,
    )
    help = help_text(
        f""""
        An APK system package (Alpine Package Keeper) built by nFPM.

        This will not install the package, only create an .apk file
        that you can then distribute and install, e.g. via pkg.

        See {doc_url('nfpm-apk-package')}.
        """
    )


ARCHLINUX_FIELDS = (
    NfpmPackageNameField,
    NfpmArchField,
    # version fields (archlinux does NOT get: version_metadata)
    NfpmVersionField,
    NfpmVersionSchemaField,
    NfpmVersionPrereleaseField,
    NfpmVersionReleaseField,
    NfpmVersionEpochField,
    # other package metadata fields
    NfpmHomepageField,
    NfpmLicenseField,
    NfpmArchlinuxPackagerField,
    NfpmArchlinuxPkgbaseField,
    # package relationships
    NfpmArchlinuxReplacesField,
    NfpmArchlinuxProvidesField,
    NfpmArchlinuxDependsField,
    NfpmArchlinuxConflictsField,
)


class NfpmArchlinuxPackage(Target):
    alias = "nfpm_archlinux_package"
    core_fields = (
        *COMMON_TARGET_FIELDS,
        OutputPathField,
        NfpmDependencies,
        *ARCHLINUX_FIELDS,
    )
    help = help_text(
        f""""
        An Archlinux system package built by nFPM.

        This will not install the package, only create an .tar.zst file
        that you can then distribute and install, e.g. via pkg.

        See {doc_url('nfpm-archlinux-package')}.
        """
    )


DEB_FIELDS = (
    NfpmPackageNameField,
    NfpmArchField,
    NfpmPlatformField,
    # version fields
    NfpmVersionField,
    NfpmVersionSchemaField,
    NfpmVersionPrereleaseField,
    NfpmVersionMetadataField,
    NfpmVersionReleaseField,
    NfpmVersionEpochField,
    # other package metadata fields
    NfpmHomepageField,
    NfpmLicenseField,  # not used by nFPM yet.
    NfpmDebMaintainerField,
    NfpmDebSectionField,
    NfpmDebPriorityField,
    # package relationships
    NfpmDebReplacesField,
    NfpmDebProvidesField,
    NfpmDebDependsField,
    NfpmDebRecommendsField,
    NfpmDebSuggestsField,
    NfpmDebConflictsField,
    NfpmDebBreaksField,
    # how to build the package
    NfpmDebCompressionField,
)


class NfpmDebPackage(Target):
    alias = "nfpm_deb_package"
    core_fields = (
        *COMMON_TARGET_FIELDS,
        OutputPathField,
        NfpmDependencies,
        *DEB_FIELDS,
    )
    help = help_text(
        f""""
        A Debian system package built by nFPM.

        This will not install the package, only create a .deb file
        that you can then distribute and install, e.g. via pkg.

        See {doc_url('nfpm-deb-package')}.
        """
    )


RPM_FIELDS = (
    NfpmPackageNameField,
    NfpmArchField,
    NfpmPlatformField,
    # version fields
    NfpmVersionField,
    NfpmVersionSchemaField,
    NfpmVersionPrereleaseField,
    NfpmVersionMetadataField,
    NfpmVersionReleaseField,
    NfpmVersionEpochField,
    # other package metadata fields
    NfpmHomepageField,
    NfpmLicenseField,
    NfpmRpmPackagerField,
    NfpmRpmVendorField,
    NfpmRpmGroupField,
    NfpmRpmSummaryField,
    # package relationships
    NfpmRpmReplacesField,
    NfpmRpmProvidesField,
    NfpmRpmDependsField,
    NfpmRpmRecommendsField,
    NfpmRpmSuggestsField,
    NfpmRpmConflictsField,
    # how to build the package
    NfpmRpmCompressionField,
)


class NfpmRpmPackage(Target):
    alias = "nfpm_rpm_package"
    core_fields = (
        *COMMON_TARGET_FIELDS,
        OutputPathField,
        NfpmDependencies,
        *RPM_FIELDS,
    )
    help = help_text(
        f""""
        An RPM system package built by nFPM.

        This will not install the package, only create an .rpm file
        that you can then distribute and install, e.g. via pkg.

        See {doc_url('nfpm-rpm-package')}.
        """
    )
