function CallWX(jsapi_name, data) {
    Java.perform(function () {
        let I = 1;
        Java.choose('com.tencent.mm.appbrand.commonjni.AppBrandCommonBindingJni', {
            onMatch: function (instance) {
                // console.log(I, JSON.stringify(instance.mAppBrandDelegate))
                instance.nativeInvokeHandler(jsapi_name, data, '{}', I++, true)
                // instance.nativeInvokeHandler('login', '{"requestInQueue":false}', '{}', I++, true)
            },
            onComplete: function () {
            }
        })
    })
}

function Main() {

    Java.perform(function () {

            let AppBrandCommonBindingJni = Java.use("com.tencent.mm.appbrand.commonjni.AppBrandCommonBindingJni");
            AppBrandCommonBindingJni["nativeInvokeHandler"].implementation = function (jsapi_name, data, str3, asyncRequestCounter, z15) {
                console.log(`[${asyncRequestCounter}] == \x1b[36m[requests]\x1b[0m: jsapi_name=${jsapi_name}, data=${data}, str3=${str3}, z15=${z15}`);
                return this["nativeInvokeHandler"](jsapi_name, data, str3, asyncRequestCounter, z15);
            };

            let AppBrandJsBridgeBinding = Java.use('com.tencent.mm.appbrand.commonjni.AppBrandJsBridgeBinding');
            AppBrandJsBridgeBinding['invokeCallbackHandler'].implementation = function (asyncRequestCounter, res) {
                console.log(`[${asyncRequestCounter}] == \x1b[32m[response]\x1b[0m: ${res}`)
                this['invokeCallbackHandler'](asyncRequestCounter, res)
            }

        }
    )
}

setTimeout(Main, 500)

//  frida -U -l Hook_WeChat_FaaS.js com.tencent.mm --no-pause