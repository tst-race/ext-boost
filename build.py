#!/usr/bin/env python3

#
# Copyright 2023 Two Six Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Script to build Boost for RACE
"""

import logging
import os
import race_ext_builder as builder


def get_cli_arguments():
    """Parse command-line arguments to the script"""
    parser = builder.get_arg_parser("boost", "1.73.0", 1, __file__)
    return builder.normalize_args(parser.parse_args())


if __name__ == "__main__":
    args = get_cli_arguments()
    builder.make_dirs(args)
    builder.setup_logger(args)

    builder.fetch_source(
        args=args,
        source=f"https://boostorg.jfrog.io/artifactory/main/release/{args.version}/source/boost_{args.version.replace('.', '_')}.tar.gz",
        extract="tar.gz",
    )

    source_dir = os.path.join(args.source_dir, f"boost_{args.version.replace('.', '_')}")

    logging.root.info("Running bootstrap.sh")
    builder.execute(args, [
        "./bootstrap.sh",
        f"--prefix={args.install_dir}",
        "--with-libraries=headers,random,system,thread,filesystem,chrono,atomic,date_time,regex"
    ], cwd=source_dir)

    logging.root.info("Running b2")
    if args.target == "linux-x86_64":
        builder.execute(args, [
            "./b2",
            "-j",
            args.num_threads,
            f"--prefix={args.install_dir}",
            f"--build-dir={args.build_dir}",
            "install",
        ], cwd=source_dir)
    if args.target == "linux-arm64-v8a":
        builder.execute(args, [
            "./b2",
            "-j",
            args.num_threads,
            f"--prefix={args.install_dir}",
            f"--build-dir={args.build_dir}",
            "architecture=arm",
            "address-model=64",
            "install",
        ], cwd=source_dir)
    if args.target == "android-x86_64":
        builder.copy(
            args,
            os.path.join(args.code_dir, "android-user-x86_64-config.jam"),
            os.path.join(source_dir, "user-config.jam"),
        )
        builder.execute(args, [
            "./b2",
            "-j",
            args.num_threads,
            f"--prefix={args.install_dir}",
            f"--build-dir={args.build_dir}",
            "--user-config=user-config.jam",
            "toolset=clang-android",
            "architecture=x86",
            "address-model=64",
            "variant=release",
            "target-os=android",
            "threading=multi",
            "link=shared",
            "install",
        ], cwd=source_dir)
    if args.target == "android-arm64-v8a":
        builder.copy(
            args,
            os.path.join(args.code_dir, "android-user-arm64-v8a-config.jam"),
            os.path.join(source_dir, "user-config.jam"),
        )
        builder.execute(args, [
            "./b2",
            "-j",
            args.num_threads,
            f"--prefix={args.install_dir}",
            f"--build-dir={args.build_dir}",
            "--user-config=user-config.jam",
            "toolset=clang-android",
            "architecture=arm",
            "address-model=64",
            "variant=release",
            "target-os=android",
            "threading=multi",
            "link=shared",
            "install",
        ], cwd=source_dir)

    builder.create_package(args)
