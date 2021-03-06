import os
from distutils.spawn import find_executable
from conans import AutoToolsBuildEnvironment, ConanFile, tools, VisualStudioBuildEnvironment
from conans.tools import cpu_count, os_info, SystemPackageTool

def which(program):
    """
    Locate a command.
    """
    def is_exe(fpath):
        """
        Check if a path is executable.
        """
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

class QtConan(ConanFile):
    """ Qt Conan package """

    name = "Qt"
    version = "5.9.1"
    description = "Conan.io package for Qt library."
    source_dir = "qt5"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "opengl": ["desktop", "dynamic"],
        "openssl": ["no", "yes", "linked"],
        "commercial": [True, False]
    }
    default_options = "shared=True\nopengl=desktop\nopenssl=no\ncommercial=False\n"
    module_options = {
        "qt3d": [True, False],
        "canvas3d": [True, False],
        "charts": [True, False],
        "cloudmessaging": [True, False],
        "datavis3d": [True, False],
        "declarative": [True, False],
        "feedback": [True, False],
        "gamepad": [True, False],
        "graphicaleffects": [True, False],
        "imageformats": [True, False],
        "location": [True, False],
        "modelling": [True, False],
        "multimedia": [True, False],
        "networkauth": [True, False],
        "osextras": [True, False],
        "pim": [True, False],
        "purchasing": [True, False],
        "quickcontrols": [True, False],
        "quickcontrols2": [True, False],
        "script": [True, False],
        "scxml": [True, False],
        "sensors": [True, False],
        "serialbus": [True, False],
        "serialport": [True, False],
        "speech": [True, False],
        "svg": [True, False],
        "styleplugins": [True, False],
        "systems": [True, False],
        "tools": [True, False],
        "virtualkeyboard": [True, False],
        "webchannel": [True, False],
        "webengine": [True, False],
        "websockets": [True, False],
        "webview": [True, False],
        "xmlpatterns": [True, False]
    }
    default_module_options = "=False\n".join(module_options.keys()) + "=False"
    options.update(module_options)
    default_options += default_module_options

    url = "http://github.com/cinderblocks/conan-qt"
    license = "http://doc.qt.io/qt-5/lgpl.html"
    short_paths = True

    def system_requirements(self):
        pack_names = None
        if os_info.linux_distro == "ubuntu":
            pack_names = ["libgl1-mesa-dev", "libxcb1", "libxcb1-dev",
                          "libx11-xcb1", "libx11-xcb-dev", "libxcb-keysyms1",
                          "libxcb-keysyms1-dev", "libxcb-image0", "libxcb-image0-dev",
                          "libxcb-shm0", "libxcb-shm0-dev", "libxcb-icccm4",
                          "libxcb-icccm4-dev", "libxcb-sync1", "libxcb-sync-dev",
                          "libxcb-xfixes0-dev", "libxrender-dev", "libxcb-shape0-dev",
                          "libxcb-randr0-dev", "libxcb-render-util0", "libxcb-render-util0-dev",
                          "libxcb-glx0-dev", "libxcb-xinerama0", "libxcb-xinerama0-dev"]

            if self.settings.arch == "x86":
                full_pack_names = []
                for pack_name in pack_names:
                    full_pack_names += [pack_name + ":i386"]
                pack_names = full_pack_names

        if pack_names:
            installer = SystemPackageTool()
            installer.update() # Update the package database
            installer.install(" ".join(pack_names)) # Install the package

    def config_options(self):
        if self.settings.os != "Windows":
            del self.options.opengl
            del self.options.openssl

    def requirements(self):
        if self.settings.os == "Windows":
            if self.options.openssl == "yes":
                self.requires("OpenSSL/1.0.2l@conan/stable")
            elif self.options.openssl == "linked":
                self.requires("OpenSSL/1.0.2l@conan/stable")

    def source(self):
        submodules = ["qtbase"]

        if self.options.qt3d:
            submodules.append("qt3d")
        if self.options.canvas3d:
            submodules.append("qtcanvas3d")
        if self.options.charts:
            submodules.append("qtcharts")
        if self.options.cloudmessaging:
            submodules.append("qtcloudmessaging")
        if self.options.datavis3d:
            submodules.append("qtdatavis3d")
        if self.options.declarative:
            submodules.append("qtdeclarative")
        if self.options.feedback:
            submodules.append("qtfeedback")
        if self.options.gamepad:
            submodules.append("qtgamepad")
        if self.options.graphicaleffects:
            submodules.append("qtgraphicaleffects")
        if self.options.imageformats:
            submodules.append("qtimageformats")
        if self.options.location:
            submodules.append("qtlocation")
        if self.options.modelling:
            submodules.append("qtmodelling")
        if self.options.multimedia:
            submodules.append("qtmultimedia")
        if self.options.networkauth:
            submodules.append("qtnetworkauth")
        if self.options.pim:
            submodules.append("qtpim")
        if self.options.purchasing:
            submodules.append("qtpurchasing")
        if self.options.quickcontrols:
            submodules.append("qtquickcontrols")
        if self.options.quickcontrols2:
            submodules.append("qtquickcontrols2")
        if self.options.script:
            submodules.append("qtscript")
        if self.options.scxml:
            submodules.append("qtscxml")
        if self.options.sensors:
            submodules.append("qtsensors")
        if self.options.serialbus:
            submodules.append("qtserialbus")
        if self.options.serialport:
            submodules.append("qtserialport")
        if self.options.speech:
            submodules.append("qtspeech")
        if self.options.svg:
            submodules.append("qtsvg")
        if self.options.styleplugins:
            submodules.append("qtstyleplugins")
        if self.options.systems:
            submodules.append("qtsystems")
        if self.options.tools:
            submodules.append("qttools")
        if self.options.virtualkeyboard:
            submodules.append("qtvirtualkeyboard")
        if self.options.webchannel:
            submodules.append("qtwebchannel")
        if self.options.webengine:
            submodules.append("qtwebengine")
        if self.options.websockets:
            submodules.append("qtwebsockets")
        if self.options.webview:
            submodules.append("qtwebview")
        if self.options.xmlpatterns:
            submodules.append("qtxmlpatterns")
        if self.options.osextras:
            if self.settings.os == "Windows":
                submodules.append("qtwinextras")
            elif self.settings.os == "Linux":
                submodules.append("qtx11extras")
            elif self.settings.os == "Macos":
                submodules.append("qtmacextras")
            

        major = ".".join(self.version.split(".")[:2])
        self.run("git clone https://code.qt.io/qt/qt5.git")
        self.run("cd %s && git checkout %s" % (self.source_dir, major))
        self.run("cd %s && perl init-repository --no-update --module-subset=%s"
                 % (self.source_dir, ",".join(submodules)))
        self.run("cd %s && git checkout v%s && git submodule update"
                 % (self.source_dir, self.version))

        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.source_dir)
        else:
            # Fix issue with sh.exe and cmake on Windows
            # This solution isn't good at all but I cannot find anything else
            sh_path = which("sh.exe")
            if sh_path:
                fpath, _ = os.path.split(sh_path)
                self.run("ren \"%s\" _sh.exe" % os.path.join(fpath, "sh.exe"))

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        args = ["-confirm-license", "-nomake examples", "-nomake tests",
                "-prefix %s" % self.package_folder]
        if not self.options.commercial:
            args.insert(0, "-opensource")
        else:
            args.insert(0, "-commercial")
        if not self.options.shared:
            args.insert(0, "-static")
        if self.settings.build_type == "Debug":
            args.append("-debug")
        else:
            args.append("-release")

        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self._build_msvc(args)
            else:
                self._build_mingw(args)
        else:
            self._build_unix(args)

    def _build_msvc(self, args):
        build_command = find_executable("jom.exe")
        if build_command:
            build_args = ["-j", str(cpu_count())]
        else:
            build_command = "nmake.exe"
            build_args = []
        self.output.info("Using '%s %s' to build" % (build_command, " ".join(build_args)))

        env = {}
        env.update({'PATH': ['%s/qtbase/bin' % self.conanfile_directory,
                             '%s/gnuwin32/bin' % self.conanfile_directory,
                             '%s/qtrepotools/bin' % self.conanfile_directory]})
        # it seems not enough to set the vcvars for older versions
        if self.settings.compiler == "Visual Studio":
            if self.settings.compiler.version == "15":
                env.update({'QMAKESPEC': 'win32-msvc2017'})
            if self.settings.compiler.version == "14":
                env.update({'QMAKESPEC': 'win32-msvc2015'})
                args += ["-platform win32-msvc2015"]
            if self.settings.compiler.version == "12":
                env.update({'QMAKESPEC': 'win32-msvc2013'})
                args += ["-platform win32-msvc2013"]
            if self.settings.compiler.version == "11":
                env.update({'QMAKESPEC': 'win32-msvc2012'})
                args += ["-platform win32-msvc2012"]
            if self.settings.compiler.version == "10":
                env.update({'QMAKESPEC': 'win32-msvc2010'})
                args += ["-platform win32-msvc2010"]

        env_build = VisualStudioBuildEnvironment(self)
        env.update(env_build.vars)

        vcvars = tools.vcvars_command(self.settings)

        args += ["-opengl %s" % self.options.opengl]

        if self.options.openssl == "no":
            args += ["-no-openssl"]
        elif self.options.openssl == "yes":
            openssl_info = self.deps_cpp_info["OpenSSL"]
            args += [("-openssl OPENSSL_LIBS=\"-lssleay32 -llibeay32\" -I\"%s\" -L\"%s\"" % (openssl_info.include_paths[0], openssl_info.lib_paths[0]))]
        else:
            openssl_info = self.deps_cpp_info["OpenSSL"]
            args += [("-openssl-linked OPENSSL_LIBS=\"-lssleay32 -llibeay32\" -I\"%s\" -L\"%s\"" % (openssl_info.include_paths[0], openssl_info.lib_paths[0]))]

        self.run("cd %s && %s && set" % (self.source_dir, vcvars))
        self.run("cd %s && %s && configure -v %s"
                 % (self.source_dir, vcvars, " ".join(args)))
        self.run("cd %s && %s && %s %s"
                 % (self.source_dir, vcvars, build_command, " ".join(build_args)))
        self.run("cd %s && %s && %s install" % (self.source_dir, vcvars, build_command))

    def _build_mingw(self, args):
        env_build = AutoToolsBuildEnvironment(self)
        env = {'PATH': ['%s/bin' % self.conanfile_directory,
                        '%s/qtbase/bin' % self.conanfile_directory,
                        '%s/gnuwin32/bin' % self.conanfile_directory,
                        '%s/qtrepotools/bin' % self.conanfile_directory],
               'QMAKESPEC': 'win32-g++'}
        env.update(env_build.vars)
        with tools.environment_append(env):
            # Workaround for configure using clang first if in the path
            new_path = []
            for item in os.environ['PATH'].split(';'):
                if item != 'C:\\Program Files\\LLVM\\bin':
                    new_path.append(item)
            os.environ['PATH'] = ';'.join(new_path)
            # end workaround
            args += ["-developer-build",
                     "-opengl %s" % self.options.opengl,
                     "-platform win32-g++"]

            self.output.info("Using '%s' threads" % str(cpu_count()))
            self.run("cd %s && configure.bat %s"
                     % (self.source_dir, " ".join(args)))
            self.run("cd %s && mingw32-make -j %s"
                     % (self.source_dir, str(cpu_count())))
            self.run("cd %s && mingw32-make install" % (self.source_dir))

    def _build_unix(self, args):
        if self.settings.os == "Linux":
            args += ["-silent", "-xcb"]
            if self.settings.arch == "x86":
                args += ["-platform linux-g++-32"]
        else:
            args += ["-silent", "-no-framework"]
            if self.settings.arch == "x86":
                args += ["-platform macx-clang-32"]

        self.output.info("Using '%s' threads" % str(cpu_count()))
        self.run("cd %s && ./configure %s" % (self.source_dir, " ".join(args)))
        self.run("cd %s && make -j %s" % (self.source_dir, str(cpu_count())))
        self.run("cd %s && make install" % (self.source_dir))

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        libs = ['Concurrent', 'Core', 'DBus',
                'Gui', 'Network', 'OpenGL',
                'Sql', 'Test', 'Widgets', 'Xml']

        self.cpp_info.libs = []
        self.cpp_info.includedirs = ["include"]
        for lib in libs:
            if self.settings.os == "Windows" and self.settings.build_type == "Debug":
                suffix = "d"
            elif self.settings.os == "Macos" and self.settings.build_type == "Debug":
                suffix = "_debug"
            else:
                suffix = ""
            self.cpp_info.libs += ["Qt5%s%s" % (lib, suffix)]
            self.cpp_info.includedirs += ["include/Qt%s" % lib]

        if self.settings.os == "Windows":
            # Some missing shared libs inside QML and others, but for the test it works
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
