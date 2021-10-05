# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import pathlib
import datetime
import Functions


class Config():
    def __init__(self):
        # Main
        self.__dict__ = Functions.config()
        self.os = Functions.osName()

        # Application
        self.app_version = self.__dict__['tool']['poetry']['version']
        self.app_name = self.__dict__['release']['app_name']
        self.app_file_ext = self.__dict__['ci']['app']['setup']['file_ext'][self.os]
        self.app_full_name = f'{self.app_name}{self.app_file_ext}'

        # Directories
        self.scripts_dir = os.path.normpath(self.__dict__['ci']['project']['subdirs']['scripts'])
        self.build_dir = os.path.normpath(self.__dict__['ci']['project']['subdirs']['build'])
        self.dist_dir = os.path.normpath(self.__dict__['ci']['project']['subdirs']['distribution'])
        self.download_dir = os.path.normpath(self.__dict__['ci']['project']['subdirs']['download'])
        self.screenshots_dir = os.path.normpath(self.__dict__['ci']['project']['subdirs']['screenshots'])
        self.tutorials_dir = os.path.normpath(self.__dict__['ci']['project']['subdirs']['tutorials'])
        self.installation_dir = self.installationDir()
        self.installation_dir_for_qtifw = self.installationDirForQtifw()

        # Application setup
        self.setup_os = self.__dict__['ci']['app']['setup']['os'][self.os]
        self.setup_arch = self.__dict__['ci']['app']['setup']['arch'][self.os]
        self.setup_name_suffix = f'_{self.setup_os}_{self.setup_arch}_v{self.app_version}'
        self.setup_name = f'{self.app_name}{self.setup_name_suffix}'
        self.setup_file_ext = self.__dict__['ci']['app']['setup']['file_ext'][self.os]
        self.setup_full_name = f'{self.setup_name}{self.setup_file_ext}'
        self.setup_exe_path = os.path.join(self.dist_dir, self.setup_full_name)
        self.maintenancetool_file = os.path.join(self.__dict__['ci']['project']['subdirs']['certificates_path'],
                                                 self.__dict__['ci']['app']['setup']['maintenance_file'])

        # Application repository
        self.repository_dir_suffix = self.__dict__['ci']['app']['setup']['repository_dir_suffix']

        # Release
        self.release_date = self.__dict__['ci']['app']['info']['build_date']
        self.release_tag = self.__dict__['release']['tag_template'].replace('{VERSION}', self.app_version)
        self.release_title = self.__dict__['release']['title_template'].replace('{VERSION}', self.app_version).replace('{DATE}', self.release_date)

        # Project
        self.package_name = f'{self.app_name}App'
        self.license_file = self.__dict__['ci']['project']['license_file']

        # Certificates
        self.certificate_path = os.path.join(self.__dict__['ci']['project']['subdirs']['certificates_path'],
                                             self.__dict__['ci']['scripts']['certificate_name'] + "_" +
                                             Functions.osName()[0:3])
        self.certificate_zip_path = os.path.join(self.__dict__['ci']['project']['subdirs']['certificates_path'],
                                                 'Codesigning.zip')

    def __getitem__(self, key):
        return self.__dict__[key]

    # https://doc.qt.io/qtinstallerframework/scripting.html
    def installationDir(self):
        dirs = {
            'macos': {
                '@HomeDir@': str(pathlib.Path.home()),
                '@ApplicationsDir@': '/Applications',
                '@ApplicationsDirUser@': str(pathlib.Path.home().joinpath('Applications'))
            },
            'ubuntu': {
                '@HomeDir@': str(pathlib.Path.home()),
                '@ApplicationsDir@': '/opt'
            },
            'windows': {
                '@HomeDir@': str(pathlib.Path.home()),
                '@ApplicationsDir@': os.getenv('ProgramFiles'),
                '@ApplicationsDirX86@': os.getenv('ProgramFiles(x86)')
            }
        }
        dir_shortcut = self.__dict__['ci']['app']['setup']['installation_dir_shortcut'][self.os]
        dir = os.path.join(dirs[self.os][dir_shortcut], self.app_name)
        return dir

    def installationDirForQtifw(self):
        dir_shortcut = self.__dict__['ci']['app']['setup']['installation_dir_shortcut'][self.os]
        if self.os == 'macos' and dir_shortcut == '@ApplicationsDir@':
            dir_shortcut = '/Applications'  # @ApplicationsDir@ = @ApplicationsDirUser@ [BUG in QTIFW?]
        dir = os.path.join(dir_shortcut, self.app_name)
        return dir

if __name__ == "__main__":
    Config()
