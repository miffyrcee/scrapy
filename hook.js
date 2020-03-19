setTimeout(function() {
  Java.perform(function() {
    var pinner = Java.use('okhttp3.CertificatePinner');
    pinner.check.overload(
      'java.lang.String',
      'java.util.List'
    ).implementation = function(str, list) {
      console.log(str);
      const host = Java.use('java.lang.String').$new('192.168.0.105');
      const port = 8080;
      const ProxyClz = Java.use('java.net.Proxy');
      const InetSocketAddressClz = Java.use('java.net.InetSocketAddress');
      const addr = InetSocketAddressClz.$new
        .overload('java.lang.String', 'int')
        .call(InetSocketAddressClz, host, port);
      const HTTP = Java.use('java.net.Proxy$Type').class.getEnumConstants()[1];
      console.log(addr);
      console.log(HTTP);
      const mProxy = ProxyClz.$new
        .overload('java.net.Proxy$Type', 'java.net.SocketAddress')
        .call(ProxyClz, HTTP, addr);
      console.log(mProxy);

      console.log(Java.use('okhttp3.OkHttpClient')['proxy']);
      Java.use('okhttp3.OkHttpClient')[
        'proxy'
      ].overload().implementation = function() {
        console.log('[OkHttpClient][proxy]');
        return mProxy;
      };
    };
  });
}, 0);
