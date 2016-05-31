function something(){
    1 + non_existant_var;
}

function test_error() {
    try {
        something();
    } catch (exc) {
        AppEnlight.grabError(exc);
    }
    AppEnlight.log('error', "some error message - from JS client");
    AppEnlight.log('info', "some info message - from JS client");
    AppEnlight.log('warning', "some warn message - from JS client");
}