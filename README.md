OPF-mvn-repo
============

Maven repository for OPF projects dependencies.

```
repositories {
    maven {
        url 'https://raw.githubusercontent.com/onepf/OPF-mvn-repo/master/'
    }
}
```

```
dependencies {
    // Amazon billing
    compile 'com.amazon:in-app-purchasing:2.0.1'
    // Fortumo billing
    compile 'com.braintree:fortumo-in-app:9.1.2'
    // Samsung billing
    compile 'com.sec.android.iap:lib:2.0.1@aar'

    // Amazon push
    compile 'com.amazon:amazon-device-messaging:1.0.1'
    // Nokia push
    compile 'com.nokia:push:1.0'
    
    // Stub FindBug annotations
    compile 'org.onepf.findbugs:annotations:1.0'
}
```
