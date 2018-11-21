module.exports.log_execution_time = function log_execution_time(func) {
    var wrapper = function() {
        start = (new Date()).getTime()
        return_value = func.apply(this, arguments);
        message = 'Calculation took ' + ((new Date()).getTime() - start) / 1000
            + " seconds";
        console.log(message);
        return return_value;
    };
    return wrapper;
};