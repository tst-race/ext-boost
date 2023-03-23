# Boost for RACE

This repo provides scripts to custom-build the
[Boost library](https://boost.org) for RACE.

## License

The Boost library is licensed by the Boost Software License 1.0.

Only the build scripts in this repo are licensed under Apache 2.0.

## Dependencies

Boost has no dependencies on any custom-built libraries.

## How To Build

The [ext-builder](https://github.com/tst-race/ext-builder) image is used to build Boost.

```
git clone https://github.com/tst-race/ext-builder.git
git clone https://github.com/tst-race/ext-boost.git
./ext-builder/build.py \
    --target linux-x86_64 \
    ./ext-boost
```

## Platforms

Boost is built for the following platforms:

* `linux-x86_64`
* `linux-arm64-v8a`
* `android-x86_64`
* `android-arm64-v8a`

## How It Is Used

Boost is used directly by the RACE core. It is also a dependency for other
libraries.
